#include <stdio.h>
#include <unistd.h>
#include <math.h>
#include <stdlib.h>
#include <string.h>
#include <time.h>
#include <stdint.h>
#include <inttypes.h>
#ifdef HAVE_CONFIG_H
#include "config.h"
#endif
#include "prophyle_query.h"
#include "bwtaln.h"
#include "bwtgap.h"
#include "utils.h"
#include "bwa.h"
#include "bwase.h"
#include "kstring.h"
#include "klcp.h"
#include "bwa_utils.h"
#include "contig_node_translator.h"

#ifndef PACKAGE_VERSION
#define PACKAGE_VERSION "0.0.1"
#endif

#ifdef HAVE_PTHREAD
#include <pthread.h>
#endif

#ifdef USE_MALLOC_WRAPPERS
#  include "malloc_wrap.h"
#endif

#define MAX_POSSIBLE_SA_POSITIONS 1000000
#define MAX_STREAK_LENGTH 10000000
#define MAX_SOFT_STREAK_LENGTH 9000000

exk_opt_t *exk_init_opt()
{
	exk_opt_t *o;
	o = (exk_opt_t*)calloc(1, sizeof(exk_opt_t));
	o->mode = BWA_MODE_GAPE | BWA_MODE_COMPREAD;
	o->n_threads = 1;
	o->trim_qual = 0;
	o->kmer_length = 14;
	o->use_klcp = 0;
	o->output = 1;
	o->output_read_qual = 0;
	o->output_old = 0;
	o->skip_positions_on_border = 1;
	o->construct_sa_parallel = 0;
	o->need_log = 0;
	o->log_file_name = NULL;
	return o;
}

int bwt_cal_sa_coord(const bwt_t *bwt, int len, const ubyte_t *str, uint64_t* k, uint64_t* l, int start_pos)
{
	bwtint_t ok, ol;
	int i;
	*k = 0; *l = bwt->seq_len;

	//fprintf(stderr, "start k = %d, l = %d\n", *k, *l);
	for (i = start_pos; i < start_pos + len; ++i) {
		ubyte_t c = str[i];
		if (c > 3) {
			*k = 1;
			*l = 0;
			return i - start_pos;
		}
		if (c < 4) {
			bwt_2occ(bwt, *k - 1, *l, c, &ok, &ol);
			*k = bwt->L2[c] + ok + 1;
			*l = bwt->L2[c] + ol;
			//fprintf(stderr, "after i = %d character, cur k = %d, l = %d\n", i, *k, *l);
		}
		if (*k > *l) { // then restart
			return i - start_pos;
		}
	}
	return len;
}

int bwt_cal_sa_coord_continue(const bwt_t *bwt, int len, const ubyte_t *str,
															uint64_t* k, uint64_t* l,
															uint64_t* decreased_k, uint64_t* increased_l,
															int start_pos, klcp_t* klcp)
{
	bwtint_t ok, ol;
	int i;
	*k = decrease_k(klcp, *k);
	*decreased_k = *k;
	*l = increase_l(klcp, *l);
	*increased_l = *l;

	//fprintf(stderr, "increased k = %d, l = %d\n", *k, *l);

	//fprintf(stderr, "start k = %d, l = %d\n", *k, *l);
	for (i = start_pos; i < start_pos + len; ++i) {
		ubyte_t c = str[i];
		if (c > 3) { // then restart
			*k = 1;
			*l = 0;
			return i - start_pos;
		}
		if (c < 4) {
			bwt_2occ(bwt, *k - 1, *l, c, &ok, &ol);
			*k = bwt->L2[c] + ok + 1;
			*l = bwt->L2[c] + ol;
			//fprintf(stderr, "after i = %d character, cur k = %d, l = %d\n", i, *k, *l);
		}
		if (*k > *l) { // then restart
			return i - start_pos;
		}
	}
	return len;
}

size_t get_positions(const bwaidx_t* idx, bwt_position_t* positions, const int query_length,
										 const uint64_t k, const uint64_t l) {
	uint64_t t;
	for(t = k; t <= l; ++t) {
		if (t - k >= MAX_POSSIBLE_SA_POSITIONS) {
			fprintf(stderr, "translation from SA-pos to seq-pos is truncated, too many (%llu) positions\n", l - k + 1);
			break;
		}
		int strand;
		uint64_t pos = bwa_sa2pos(idx->bns, idx->bwt, t, query_length, &strand);//bwt_sa(bwt, t);
		positions[t - k].position = pos;
		positions[t - k].strand = strand;
		positions[t - k].rid = -1;
		//fprintf(stdout, "%llu(%d) ", (*positions)[t - k], strand);
	}
	//fprintf(stdout, "\n");
	return (l - k + 1 < MAX_POSSIBLE_SA_POSITIONS ? l - k + 1 : MAX_POSSIBLE_SA_POSITIONS);
}

int position_on_border(const bwaidx_t* idx, bwt_position_t* position, int query_length) {
	//fprintf(stdout, "%llu %d %llu\n", position->position, query_length, idx->bns->l_pac);
	//fprintf(stdout, "%d %d\n", position->rid, idx->bns->n_seqs);
	return (position->position + query_length > idx->bns->l_pac
		|| (position->rid + 1 < idx->bns->n_seqs && position->position + query_length > idx->bns->anns[position->rid + 1].offset)
		|| position->position < idx->bns->anns[position->rid].offset);
}

void sort(int count, int** array) {
	int i;
	for(i = 1; i < count; ++i) {
		int x = (*array)[i];
		int j = i - 1;
		while (j >= 0 && (*array)[j] > x) {
			(*array)[j + 1] = (*array)[j];
			j--;
		}
		(*array)[j + 1] = x;
	}
}

size_t get_nodes_from_positions(const bwaidx_t* idx, const int query_length,
																const int positions_cnt, bwt_position_t* positions, int32_t* seen_nodes,
																int8_t** seen_nodes_marks, int skip_positions_on_border) {
	size_t nodes_cnt = 0;
	int i;
	for(i = 0; i < positions_cnt; ++i) {
		uint64_t pos = positions[i].position;
		//fprintf(stdout, "%llu\n", pos);
		if (pos == (uint64_t)-1) {
			continue;
		}
		int rid = positions[i].rid;
		if (rid == -1 || position_on_border(idx, &(positions[i]), query_length)) {
			rid = bns_pos2rid(idx->bns, pos);
			positions[i].rid = rid;
		}
		int node = get_node_from_contig(rid);
		positions[i].node = node;
		int seen = (*seen_nodes_marks)[node];
		//fprintf(stdout, "position = %llu, rid = %d, offset[rid] = %llu, offset[rid + 1] = %llu\n",
		// 	pos, rid, idx->bns->anns[rid].offset, idx->bns->anns[rid + 1].offset);
		if (!seen && node != -1 && (!skip_positions_on_border || !position_on_border(idx, &(positions[i]), query_length))) {
			seen_nodes[nodes_cnt] = node;
			++nodes_cnt;
			(*seen_nodes_marks)[node] = 1;
			//fprintf(stderr, "t = %d, pos = %d, rid = %d\n", t, pos, rid);
		}
	}
	int r;
	for(r = 0; r < nodes_cnt; ++r) {
		(*seen_nodes_marks)[seen_nodes[r]] = 0;
	}
	sort(nodes_cnt, &seen_nodes);
	return nodes_cnt;
}

void output_old(int* seen_nodes, const int nodes_cnt) {
	fprintf(stdout, "%d ", nodes_cnt);
	int r;
	for(r = 0; r < nodes_cnt; ++r) {
		fprintf(stdout, "%s ", get_node_name(seen_nodes[r]));
	}
	fprintf(stdout, "\n");
}

void strncat_with_check(char* str, char* str_to_append, int* str_length,
	int str_to_append_length, int length_limit) {
	if (*str_length >= length_limit) {
		fprintf(stderr, "too long output string, more than %d symbols\n", length_limit);
	} else {
		strncat(str, str_to_append, length_limit - str_to_append_length);
		*str_length += str_to_append_length;
		if (*str_length > length_limit) {
			*str_length = length_limit;
		}
	}
}

void construct_streaks(char** all_streaks, char** current_streak, int* seen_nodes, const int nodes_cnt, int streak_size,
	int is_ambiguous_streak, int is_first_streak) {
	if (is_first_streak) {
		*all_streaks[0] = '\0';
	}
	*current_streak[0] = '\0';
	int current_streak_approximate_length = 0;
	if (is_ambiguous_streak) {
		strcat(*current_streak, "A:");
		current_streak_approximate_length += 2;
	} else if (nodes_cnt > 0) {
		int r;
		for(r = 0; r < nodes_cnt - 1; ++r) {
			strncat_with_check(*current_streak, get_node_name(seen_nodes[r]), &current_streak_approximate_length, get_node_name_length(seen_nodes[r]), MAX_SOFT_STREAK_LENGTH);
			strncat_with_check(*current_streak, ",", &current_streak_approximate_length, 1, MAX_SOFT_STREAK_LENGTH);
		}
		strncat_with_check(*current_streak, get_node_name(seen_nodes[nodes_cnt - 1]), &current_streak_approximate_length, get_node_name_length(seen_nodes[nodes_cnt - 1]), MAX_SOFT_STREAK_LENGTH);
		strncat_with_check(*current_streak, ":", &current_streak_approximate_length, 1, MAX_SOFT_STREAK_LENGTH);
	} else {
		strncat_with_check(*current_streak, "0:", &current_streak_approximate_length, 2, MAX_SOFT_STREAK_LENGTH);
	}
	sprintf(*current_streak + strlen(*current_streak), "%d", streak_size);
	current_streak_approximate_length += 3;
	if (is_first_streak) {
		if (current_streak_approximate_length <= MAX_STREAK_LENGTH) {
			strcpy(*all_streaks, *current_streak);
		} else {
			strncpy(*all_streaks, *current_streak, MAX_STREAK_LENGTH);
		}
	} else {
		strncat_with_check(*current_streak, " ", &current_streak_approximate_length, 1, MAX_SOFT_STREAK_LENGTH);
		strncat_with_check(*current_streak, *all_streaks, &current_streak_approximate_length, strlen(*all_streaks), MAX_SOFT_STREAK_LENGTH);
		char* tmp = *all_streaks;
		*all_streaks = *current_streak;
		*current_streak = tmp;
	}
}

void print_streaks(char* streaks) {
	fprintf(stdout, "%s", streaks);
}

void shift_positions_by_one(bwaidx_t* idx, int positions_cnt, bwt_position_t* positions,
														const int query_length, const uint64_t k, const uint64_t l) {
	int i;
	for(i = 0; i < positions_cnt; ++i) {
		if (positions[i].position == (uint64_t)-1) {
			continue;
		}
		if (positions[i].strand == 0) {
			positions[i].position++;
		} else {
				positions[i].position--;
		}
	}
}

int equal(int a_cnt, int* a, int b_cnt, int* b) {
	if (a_cnt != b_cnt) {
		return 0;
	}
	int i;
	for(i = 0; i < a_cnt; ++i) {
		if (a[i] != b[i]) {
			return 0;
		}
	}
	return 1;
}

void print_read(bwa_seq_t* p) {
	int j;
	for(j = (int)p->len - 1; j>= 0; j--) {
		fprintf(stdout, "%c", "ACGTN"[p->seq[j]]);
	}
}

void print_read_qual(bwa_seq_t* p) {
	if (p->qual) {
		int j;
		for(j = 0; j < (int)p->len; j++) {
			fprintf(stdout, "%c", p->qual[j]);
		}
	} else {
		fprintf(stdout, "*");
	}
}

typedef struct {
	bwt_position_t* positions;
	char* all_streaks;
	char* current_streak;
	int32_t* seen_nodes;
	int32_t* prev_seen_nodes;
	int8_t* seen_nodes_marks;
	int rids_computations;
	int using_prev_rids;
} prophyle_query_aux_t;

typedef struct {
	bwaidx_t* idx;
	klcp_t* klcp;
	const exk_opt_t *opt;
	bwa_seq_t *seqs;
	prophyle_query_aux_t* aux_data;
	int32_t seqs_cnt;
	char** output;
} prophyle_worker_t;

prophyle_worker_t* prophyle_worker_init(bwaidx_t* idx, int32_t seqs_cnt, bwa_seq_t *seqs,
		const exk_opt_t *opt, klcp_t* klcp) {
	prophyle_worker_t* prophyle_worker_data = malloc(1 * sizeof(prophyle_worker_t));
	prophyle_worker_data->idx = idx;
	prophyle_worker_data->seqs = seqs;
	prophyle_worker_data->opt = opt;
	prophyle_worker_data->klcp = klcp;
	prophyle_worker_data->aux_data = malloc(opt->n_threads * sizeof(prophyle_query_aux_t));
	int tid;
	for (tid = 0; tid < opt->n_threads; ++tid) {
		prophyle_worker_data->aux_data[tid].positions = malloc(MAX_POSSIBLE_SA_POSITIONS * sizeof(bwt_position_t));
		prophyle_worker_data->aux_data[tid].all_streaks = malloc(MAX_STREAK_LENGTH * sizeof(char));
		prophyle_worker_data->aux_data[tid].current_streak = malloc(MAX_STREAK_LENGTH * sizeof(char));
		prophyle_worker_data->aux_data[tid].seen_nodes = malloc(MAX_POSSIBLE_SA_POSITIONS * sizeof(int32_t));
		prophyle_worker_data->aux_data[tid].prev_seen_nodes = malloc(MAX_POSSIBLE_SA_POSITIONS * sizeof(int32_t));
		prophyle_worker_data->aux_data[tid].seen_nodes_marks = malloc(idx->bns->n_seqs * sizeof(int8_t));
		int index;
		for(index = 0; index < idx->bns->n_seqs; ++index) {
			prophyle_worker_data->aux_data[tid].seen_nodes_marks[index] = 0;
		}
		prophyle_worker_data->aux_data[tid].rids_computations = 0;
		prophyle_worker_data->aux_data[tid].using_prev_rids = 0;
	}
	prophyle_worker_data->seqs_cnt = seqs_cnt;
	prophyle_worker_data->output = malloc(seqs_cnt * sizeof(char*));
	int i = 0;
	for (i = 0; i < seqs_cnt; ++i) {
		prophyle_worker_data->output[i] = NULL;
	}
	return prophyle_worker_data;
}

void prophyle_aux_data_destroy(prophyle_query_aux_t* prophyle_query_aux_data) {
	if (prophyle_query_aux_data->positions) {
		free(prophyle_query_aux_data->positions);
	}
	if (prophyle_query_aux_data->all_streaks) {
		free(prophyle_query_aux_data->all_streaks);
	}
	if (prophyle_query_aux_data->current_streak) {
		free(prophyle_query_aux_data->current_streak);
	}
	if (prophyle_query_aux_data->seen_nodes) {
		free(prophyle_query_aux_data->seen_nodes);
	}
	if (prophyle_query_aux_data->prev_seen_nodes) {
		free(prophyle_query_aux_data->prev_seen_nodes);
	}
	if (prophyle_query_aux_data->seen_nodes_marks) {
		free(prophyle_query_aux_data->seen_nodes_marks);
	}
}

void prophyle_worker_destroy(prophyle_worker_t* prophyle_worker_data) {
	if (!prophyle_worker_data) {
		return;
	}
	int i;
	for (i = 0; i < prophyle_worker_data->opt->n_threads; ++i) {
		prophyle_aux_data_destroy(&prophyle_worker_data->aux_data[i]);
	}
	if (prophyle_worker_data->aux_data) {
		free(prophyle_worker_data->aux_data);
	}
	if (prophyle_worker_data->output) {
		for (i = 0; i < prophyle_worker_data->seqs_cnt; ++i) {
			if (prophyle_worker_data->output[i]) {
				free(prophyle_worker_data->output[i]);
		  }
		}
		if (prophyle_worker_data->output) {
			free(prophyle_worker_data->output);
		}
	}
	free(prophyle_worker_data);
}

void prophyle_process_sequence(void* data, int i, int tid) {
	prophyle_worker_t* prophyle_worker_data = (prophyle_worker_t*)data;
	bwaidx_t* idx = prophyle_worker_data->idx;
	bwa_seq_t seq = prophyle_worker_data->seqs[i];
	const exk_opt_t* opt = prophyle_worker_data->opt;
	klcp_t* klcp = prophyle_worker_data->klcp;
	prophyle_query_aux_t aux_data = prophyle_worker_data->aux_data[tid];
	char* current_streak = aux_data.current_streak;
	char* all_streaks = aux_data.all_streaks;
	int32_t* seen_nodes = aux_data.seen_nodes;
	int32_t* prev_seen_nodes = aux_data.prev_seen_nodes;
	int8_t* seen_nodes_marks = aux_data.seen_nodes_marks;

	if (opt->output_old) {
		fprintf(stdout, "#");
		print_read(&seq);
		fprintf(stdout, "\n");
	}
	bwt_t* bwt = idx->bwt;
	uint64_t k = 0, l = 0, prev_k = 1, prev_l = 0;
	int current_streak_size = 0;
	int prev_nodes_count = 0;
	int start_pos = 0;
	size_t positions_cnt = 0;
	uint64_t decreased_k = 1;
	uint64_t increased_l = 0;
	int is_first_streak = 1;
	int last_ambiguous_index = 0 - opt->kmer_length;
	int is_ambiguous_streak = 0;
	int ambiguous_streak_just_ended = 0;
	if (start_pos + opt->kmer_length > seq.len) {
		if (opt->output) {
			//fprintf(stdout, "0:0\n");
			prophyle_worker_data->output[i] = malloc(5 * sizeof(char));
			strncpy(prophyle_worker_data->output[i], "0:0\n", 5);
		}
	} else {
		while (start_pos + opt->kmer_length <= seq.len) {
			int end_pos = start_pos + opt->kmer_length - 1;
			if (opt->output) {
				if (start_pos == 0) {
					int index = 0;
					for(index = 0; index < opt->kmer_length; ++index) {
						if (seq.seq[index] > 3) {
							last_ambiguous_index = index;
						}
					}
				} else {
					if (seq.seq[end_pos] > 3) {
						last_ambiguous_index = end_pos;
					}
				}
				if (end_pos - last_ambiguous_index < opt->kmer_length) {
					if (!is_ambiguous_streak) {
						construct_streaks(&all_streaks, &current_streak, prev_seen_nodes, prev_nodes_count, current_streak_size,
							is_ambiguous_streak, is_first_streak);
						if (is_first_streak) {
							is_first_streak = 0;
						}
						is_ambiguous_streak = 1;
						current_streak_size = 1;
					} else {
						current_streak_size++;
					}
					start_pos++;
					continue;
				} else {
					if (is_ambiguous_streak && current_streak_size > 0) {
						construct_streaks(&all_streaks, &current_streak, prev_seen_nodes, prev_nodes_count, current_streak_size,
							is_ambiguous_streak, is_first_streak);
						if (is_first_streak) {
							is_first_streak = 0;
						}
						is_ambiguous_streak = 0;
						current_streak_size = 0;
					}
				}
				if (end_pos - last_ambiguous_index == opt->kmer_length) {
					ambiguous_streak_just_ended = 1;
				} else {
					ambiguous_streak_just_ended = 0;
				}
			}
			if (start_pos == 0) {
				k = 0;
				l = 0;
				bwt_cal_sa_coord(bwt, opt->kmer_length, seq.seq, &k, &l, start_pos);
			} else {
				if (opt->use_klcp && k <= l) {
					bwt_cal_sa_coord_continue(bwt, 1, seq.seq, &k, &l, &decreased_k, &increased_l, start_pos + opt->kmer_length - 1, klcp);
				} else {
					k = 0;
					l = 0;
					bwt_cal_sa_coord(bwt, opt->kmer_length, seq.seq, &k, &l, start_pos);
				}
			}
			//fprintf(stderr, "start_pos = %d\n", start_pos);
			//fprintf(stderr, "found k = %llu, l = %llu\n", k, l);
			// fprintf(stderr, "prev k = %llu, prev l = %llu\n", prev_k, prev_l);
			int nodes_cnt = 0;
			if (k <= l) {
				if (prev_l - prev_k == l - k
						&& increased_l - decreased_k == l - k) {
					aux_data.using_prev_rids++;
					shift_positions_by_one(idx, positions_cnt, aux_data.positions, opt->kmer_length, k, l);
				} else {
					aux_data.rids_computations++;
					positions_cnt = get_positions(idx, aux_data.positions, opt->kmer_length,
						k, l);
				}
				nodes_cnt = get_nodes_from_positions(idx, opt->kmer_length,
					positions_cnt, aux_data.positions, seen_nodes, &seen_nodes_marks, opt->skip_positions_on_border);
			}
			if (opt->output_old) {
				output_old(seen_nodes, nodes_cnt);
			} else if (opt->output) {
				if (start_pos == 0 || ambiguous_streak_just_ended || (equal(nodes_cnt, seen_nodes, prev_nodes_count, prev_seen_nodes))) {
					current_streak_size++;
				} else {
					construct_streaks(&all_streaks, &current_streak, prev_seen_nodes, prev_nodes_count, current_streak_size,
						is_ambiguous_streak, is_first_streak);
					if (is_first_streak) {
						is_first_streak = 0;
					}
					current_streak_size = 1;
				}
			}
			int* tmp = seen_nodes;
			seen_nodes = prev_seen_nodes;
			prev_seen_nodes = tmp;
			prev_nodes_count = nodes_cnt;
			prev_k = k;
			prev_l = l;
			start_pos++;
		}
		if (current_streak_size > 0) {
			construct_streaks(&all_streaks, &current_streak, prev_seen_nodes, prev_nodes_count, current_streak_size,
				is_ambiguous_streak, is_first_streak);
		}
		if (opt->output) {
			//fprintf(stdout, "\n");
			size_t all_streaks_length = strlen(all_streaks);
			prophyle_worker_data->output[i] = malloc((all_streaks_length + 1) * sizeof(char));
			strncpy(prophyle_worker_data->output[i], all_streaks, all_streaks_length + 1);
		}
	}
}

void bwa_cal_sa(bwaidx_t* idx, int n_seqs, bwa_seq_t *seqs,
								const exk_opt_t *opt, klcp_t* klcp)
{
	extern void kt_for(int n_threads, void (*func)(void*,int,int), void *data, int n);
	bwase_initialize();
	prophyle_worker_t* prophyle_worker_data = prophyle_worker_init(idx, n_seqs, seqs, opt, klcp);
	kt_for(opt->n_threads, prophyle_process_sequence, prophyle_worker_data, n_seqs);
	int i;
	for (i = 0; i < n_seqs; ++i) {
		bwa_seq_t* seq = seqs + i;

		if (opt->output) {
			fprintf(stdout, "U\t%s\t0\t%d\t", seq->name, seq->len);
			print_streaks(prophyle_worker_data->output[i]);
			if (opt->output_read_qual) {
				fprintf(stdout, "\t");
				print_read(seq);
				fprintf(stdout, "\t");
				print_read_qual(seq);
			}
			fprintf(stdout, "\n");
		}

		free(seq->name); free(seq->seq); free(seq->rseq); free(seq->qual);
		seq->name = 0; seq->seq = seq->rseq = seq->qual = 0;
	}
	// write combining results
	// fprintf(stderr, "rids computed: %d\n", rids_computations);
	// fprintf(stderr, "rids used previous: %d\n", using_prev_rids);
	prophyle_worker_destroy(prophyle_worker_data);
}

void bwa_exk_core(const char *prefix, const char *fn_fa, const exk_opt_t *opt) {
	int n_seqs;
	bwa_seq_t *seqs;
	bwa_seqio_t *ks;
	bwaidx_t* idx;
	int i;
	FILE* log_file;
	if (opt->need_log) {
		log_file = fopen(opt->log_file_name, "w");
	} else {
		log_file = stderr;
	}

	if ((idx = bwa_idx_load_partial(prefix, BWA_IDX_ALL, opt->need_log, log_file)) == 0) {
		fprintf(stderr, "Couldn't load idx from %s\n", prefix);
		return;
	}

	// If fa2pac was called only for doubled string, then set bns->l_pac = bwt->seq_len, as it is for forward-only string
	idx->bns->l_pac = idx->bwt->seq_len / 2;

	fprintf(stderr, "BWA loaded\n");
	bwa_destroy_unused_fields(idx);

	double ctime, rtime;
	ctime = cputime(); rtime = realtime();
	klcp_t* klcp = malloc(sizeof(klcp_t));
	klcp->klcp = malloc(sizeof(bitarray_t));

	if (opt->use_klcp) {
		char* fn = malloc((strlen(prefix) + 10) * sizeof(char));
	  strcpy(fn, prefix);
		strcat(fn, ".");
	  char* kmer_length_str = malloc(5 * sizeof(char));
	  sprintf(kmer_length_str, "%d", opt->kmer_length);
	  strcat(fn, kmer_length_str);
	  strcat(fn, ".klcp");
		klcp_restore(fn, klcp);
		free(fn);
		fprintf(log_file, "klcp_loading\t%.2fs\n", realtime() - rtime);
	}
	ks = bwa_open_reads_new(opt->mode, fn_fa);
	float total_time = 0;
	int64_t total_seqs = 0;
	ctime = cputime(); rtime = realtime();
	int64_t total_kmers_count = 0;
	fprintf(stderr, "number of threads = %d\n", opt->n_threads);
	while ((seqs = bwa_read_seq(ks, 0x40000, &n_seqs, opt->mode, opt->trim_qual)) != 0) {
		bwa_cal_sa(idx, n_seqs, seqs, opt, klcp);
		total_seqs += n_seqs;
		for (i = 0; i < n_seqs; ++i) {
			int seq_kmers_count = seqs[i].len - opt->kmer_length + 1;
			if (seq_kmers_count > 0) {
				total_kmers_count += seq_kmers_count;
			}
		}
		bwa_free_read_seq(n_seqs, seqs);
	}
	total_time = realtime() - rtime;
	fprintf(stderr, "match time: %.2f sec\n", total_time);
	fprintf(stderr, "[M::%s] Processed %llu reads in %.3f CPU sec, %.3f real sec\n", __func__, total_seqs, cputime() - ctime, realtime() - rtime);

	if (opt->need_log) {
		fprintf(log_file, "matching_time\t%.2fs\n", total_time);
		fprintf(log_file, "reads\t%" PRId64 "\n", total_seqs);
		fprintf(log_file, "kmers\t%" PRId64 "\n", total_kmers_count);
		fprintf(log_file, "rpm\t%" PRId64 "\n", (int64_t)(round(total_seqs * 60.0 / total_time)));
		fprintf(log_file, "kpm\t%" PRId64 "\n", (int64_t)(round(total_kmers_count * 60.0 / total_time)));
	}
	//fprintf(stderr, "tot_seqs = %d\n", tot_seqs);
	//fprintf(stderr, "overall_increase = %llu\n", overall_increase);
	//fprintf(stderr, "increase per k-mer = %lf\n", 1.0 * overall_increase / (tot_seqs * (seq_len - opt->kmer_length + 1)));

	if (opt->need_log) {
		fclose(log_file);
	}
	// destroy
	if (opt->use_klcp) {
		destroy_klcp(klcp);
	} else {
		free(klcp->klcp);
		free(klcp);
	}
	bwa_idx_destroy_without_bns_name_and_anno(idx);
	bwa_seq_close(ks);
}
