#! /usr/bin/env python3

import argparse
import datetime
import multiprocessing
import os
import shutil
import subprocess
import sys

c_d=os.path.dirname(os.path.realpath(__file__))

#bin_dir=os.path.normpath(os.path.join(os.path.dirname(__file__),"../../bin"))
#bin_dir=os.path.dirname(__file__)
bwa=os.path.join(c_d,"prophyle-index","bwa","bwa")
exk=os.path.join(c_d,"prophyle-index","prophyle-index")
asm=os.path.join(c_d,"prophyle-assembler","prophyle-assembler")
newick2makefile=os.path.join(c_d,"newick2makefile.py")
test_newick=os.path.join(c_d,"test_newick_tree.py")
merge_fastas=os.path.join(c_d,"create_final_fasta.py")
assign=os.path.join(c_d,"prophyle-assignment","assignment.py")

DEFAULT_K=32
DEFAULT_THREADS=multiprocessing.cpu_count()
DEFAULT_MEASURE='h1'
DEFAULT_HOME_DIR=os.path.join(os.path.expanduser('~'),'prophyle')

LIBRARIES=['bacteria', 'viruses', 'plasmids', 'hmp']

FTP_NCBI='https://ftp.ncbi.nlm.nih.gov'
# todo: add both FTP and HTTP variants
#   http://downloads.hmpdacc.org/data/HMREFG/all_seqs.fa.bz2
#   ftp://public-ftp.hmpdacc.org/HMREFG/all_seqs.fa.bz2


def _test_files(*fns,test_nonzero=False):
	#print(fns)
	for fn in fns:
		assert os.path.isfile(fn), 'File "{}" does not exist'.format(fn)
		if test_nonzero:
			assert _file_sizes(fn)[0], 'File "{}" has size 0'.format(fn)

def _test_newick(fn):
	_test_files(fn)
	cmd=[test_newick, '-n', fn]

def _file_sizes(*fns):
	return tuple( [os.stat(fn).st_size for fn in fns] )

def _run_safe(command, output_fn=None):
	command_str=" ".join(map(lambda x: str(x),command))
	print("Running:", command_str, file=sys.stderr)
	if output_fn is None:
		out_fo=sys.stdout
	else:
		out_fo=open(output_fn,"w+")
	error_code=subprocess.call("/bin/bash -x -o pipefail -c '{}'".format(command_str), shell=True, stdout=out_fo)
	if error_code==0:
		print("Finished:", command_str, file=sys.stderr)
	elif error_code==141:
		pass
		#print("Exited before finishing:", command_str, file=sys.stderr)
	else:
		print("Finished with error (error code {}):".format(error_code), command_str, file=sys.stderr)
		# todo: maybe it will be better to throw an exception
		sys.exit(error_code)

def _message(msg):
	dt=datetime.datetime.now()
	fdt=dt.strftime("%Y-%m-%d %H:%M:%S")
	print('[prophyle]', fdt, msg, file=sys.stderr)

def _touch(*fns):
	for fn in fns:
		if os.path.exists(fn):
			os.utime(fn, None)
		else:
			with open(fn, 'a'):
				pass

def _rm(*fns):
	for fn in fns:
		try:
			os.remove(fn)
		except FileNotFoundError:
			pass


#################
# PROPHYLE INIT #
#################

def _complete(d, i):
	fn=os.path.join(d,".complete.{}".format(i))
	_touch(fn)

# .complete.i exists AND it is newere than .complete.(i-1)
def _is_complete(d, i):
	assert i>0
	fn=os.path.join(d,".complete.{}".format(i))
	fn0=os.path.join(d,".complete.{}".format(i-1))
	if not os.path.isfile(fn):
		return False
	if i==1:
		return True
	if os.path.isfile(fn0) and os.path.getmtime(fn0)<=os.path.getmtime(fn):
		return True
	else:
		return False

def _missing_library(d):
	l=os.path.dirname(d)
	os.makedirs(d, exist_ok=True)
	if _is_complete(d,1):
		_message("Skipping downloading library '{}' (already exists)".format(l))
		return False
	else:
		_message("Downloading library '{}'".format(l))
		return True


def _pseudo_fai(d):
	l=os.path.dirname(d)
	pseudofai_fn=d+".pseudofai"
	os.makedirs(d, exist_ok=True)
	if _is_complete(d,2) and os.path.isfile(pseudofai_fn):
		_message("Skipping generating pseudofai for library '{}' (already exists)".format(l))
	else:
		_message("Generating pseudofai for library '{}'".format(l))
		assert d[-1]!="/"
		cmd=['grep -r --include=\\*.{fa,ffn,fna}', '">"', d, '| sed "s/:>/\t/"']
		_run_safe(cmd, pseudofai_fn)
		_complete(d, 2)

def init(library, home_dir):
	print('making',home_dir)
	os.makedirs(home_dir, exist_ok=True)
	if library=='all':
		ls=LIBRARIES
	else:
		ls=[library]

	# todo: http vs ftp

	for l in ls:
		if l=='bacteria':
			d=os.path.join(home_dir,'bacteria')
			if _missing_library(d):
				_message("Downloading library '{}'".format(l))
				# fix when error appears
				cmd=['cd', d, '&& curl', FTP_NCBI+'/genomes/archive/old_refseq/Bacteria/all.fna.tar.gz | tar xvz']
				_run_safe(cmd)
				_complete(d, 1)
			_pseudo_fai(d)

		elif l=='viruses':
			d=os.path.join(home_dir,'viruses')
			if _missing_library(d):
				# fix when error appears
				cmd=['cd', d, '&& curl', FTP_NCBI+'/genomes/Viruses/all.ffn.tar.gz | tar xvz']
				_run_safe(cmd)
				cmd=['cd', d, '&& curl', FTP_NCBI+'/genomes/Viruses/all.fna.tar.gz | tar xvz']
				_run_safe(cmd)
				_complete(d, 1)
			_pseudo_fai(d)

		elif l=='plasmids':
			d=os.path.join(home_dir,'plasmids')
			if _missing_library(d):
				# fix when error appears
				cmd=['cd', d, '&& curl', FTP_NCBI+'/genomes/archive/old_refseq/Plasmids/plasmids.all.fna.tar.gz | tar xvz']
				_run_safe(cmd)
				_complete(d, 1)
			_pseudo_fai(d)

		elif l=='hmp':
			d=os.path.join(home_dir,'hmp')
			if _missing_library(d):
				_message("Downloading downloading library '{}'".format(l))
				# fix when error appears
				cmd=['cd', d, '&& curl http://downloads.hmpdacc.org/data/HMREFG/all_seqs.fa.bz2 | bzip2 -d']
				_run_safe(cmd,os.path.join(d,"all_seqs.fa"))
				_complete(d, 1)
			_pseudo_fai(d)


		else:
			raise ValueError('Unknown library ""'.format(library))


##################
# PROPHYLE INDEX #
##################

def _create_makefile(index_dir, k, library_dir):
	_message('Creating Makefile for k-mer propagation')
	propagation_dir=os.path.join(index_dir, 'propagation')
	os.makedirs(propagation_dir,exist_ok=True)

	makefile=os.path.join(propagation_dir,'Makefile')
	newick_fn=os.path.join(index_dir,'tree.newick')
	_test_newick(newick_fn)
	#_test_files(newick2makefile, newick_fn)
	command=[newick2makefile, '-n', newick_fn, '-k', k, '-o', './', '-l', os.path.abspath(library_dir)]
	_run_safe(command,makefile)

def _propagate(index_dir,threads):
	_message('Running k-mer propagation')
	propagation_dir=os.path.join(index_dir, 'propagation')
	_test_files(os.path.join(propagation_dir, 'Makefile'),test_nonzero=True)
	command=['make', '-j', threads, '-C', propagation_dir, 'V=1', "ASSEMBLER={}".format(asm)]
	_run_safe(command)

def _merge_fastas(index_dir):
	_message('Generating index.fa')
	propagation_dir=os.path.join(index_dir, 'propagation')
	# todo: check files for all nodes exist and are of size > 0
	index_fa=os.path.join(index_dir,"index.fa")
	_test_files(merge_fastas)
	command=[merge_fastas, propagation_dir]
	_run_safe(command, index_fa)
	_touch(index_fa+".complete")

def _fa2pac(fa_fn):
	_message('Generating packed FASTA file')
	_test_files(bwa, fa_fn)
	command=[bwa, 'fa2pac', fa_fn, fa_fn]
	_run_safe(command)

def _pac2bwt(fa_fn):
	_message('Generating BWT')
	_test_files(bwa, fa_fn+".pac")
	command=[bwa, 'pac2bwtgen', fa_fn+".pac", fa_fn+".bwt"]
	_run_safe(command)

def _bwt2bwtocc(fa_fn):
	_message('Generating sampled OCC array')
	_test_files(bwa, fa_fn+".bwt")
	command=[bwa, 'bwtupdate', fa_fn+".bwt"]
	_run_safe(command)

def _bwtocc2sa(fa_fn):
	_message('Generating sampled SA')
	_test_files(bwa, fa_fn+".bwt")
	command=[bwa, 'bwt2sa', fa_fn+".bwt", fa_fn+".sa"]
	_run_safe(command)

def _bwtocc2klcp(fa_fn,k):
	_message('Generating k-LCP array')
	_test_files(exk, fa_fn+".bwt")
	command=[exk, 'index', '-k', k, fa_fn]
	_run_safe(command)

def index(index_dir, threads, k, newick_fn, library_dir, cont=False, klcp=True, ccontinue=False):
	assert k>1

	# check files & dirs
	_test_newick(newick_fn)
	index_fa=os.path.join(index_dir,'index.fa')
	index_newick=os.path.join(index_dir,'tree.newick')
	makefile_dir=os.path.join(index_dir,'propagation')
	makefile=os.path.join(index_dir,'propagation','Makefile')

	# make index dir
	if ccontinue:
		assert not os.path.isfile(index_dir)
		os.makedirs(index_dir, exist_ok=True)
	else:
		assert not os.path.isfile(index_dir)
		assert not os.path.isdir(index_dir)

	# copy newick
	if ccontinue and os.path.isfile(index_newick):
		_message('Skipping Newick copying, already exists')
	else:
		shutil.copy(newick_fn, index_newick)

	# create Makefile & run Makefile & merge fastas
	if ccontinue and os.path.isfile(index_fa+'.complete'):
		_message('Skipping k-mer propagation, index.fa already exists')
	else:
		_create_makefile(index_dir, k, library_dir)
		_propagate(index_dir, threads=threads)
		_merge_fastas(index_dir)
		_touch(index_fa+'.complete')

	# bwa index & klcp
	if ccontinue and os.path.isfile(index_fa+'.bwt') and os.path.isfile(index_fa+'.bwt.complete'):
		_message('Skipping BWT construction, already exists')
	else:
		_rm(index_fa+'.bwt',index_fa+'.bwt.complete')
		_fa2pac(index_fa)
		_pac2bwt(index_fa)
		_bwt2bwtocc(index_fa)
		_touch(index_fa+'.bwt.complete')

	if ccontinue and os.path.isfile(index_fa+'.sa'):
		_message('Skipping SA construction, already exists')
	else:
		_bwtocc2sa(index_fa)

	if klcp:
		klcp_fn="{}.{}.bit.klcp".format(index_fa,k)
		if ccontinue and os.path.isfile(klcp_fn):
			_message('Skipping k-LCP construction, already exists')
		else:
			_bwtocc2klcp(index_fa,k)


#####################
# PROPHYLE CLASSIFY #
#####################

def classify(index_dir,fq_fn,k,use_klcp,out_format,mimic_kraken,measure,annotate,tie_lca):
	index_fa=os.path.join(index_dir, 'index.fa')
	index_newick=os.path.join(index_dir, 'tree.newick')

	_test_newick(index_newick)
	_test_files(fq_fn,index_fa,exk,assign)

	_test_files(
			index_fa+'.bwt',
			index_fa+'.pac',
			index_fa+'.sa',
			index_fa+'.ann',
			index_fa+'.amb',
		)

	(bwt_s, sa_s, pac_s)=_file_sizes(index_fa+'.bwt',index_fa+'.sa',index_fa+'.pac')
	assert abs(bwt_s - 2*sa_s) < 1000, 'Inconsistent index (SA vs. BWT)'
	assert abs(bwt_s - 2*pac_s) < 1000, 'Inconsistent index (PAC vs. BWT)'

	if use_klcp:
		klcp_fn="{}.{}.bit.klcp".format(index_fa,k)
		_test_files(klcp_fn)
		(klcp_s,)=_file_sizes(klcp_fn)
		assert abs(bwt_s - 4*klcp_s) < 1000, 'Inconsistent index (KLCP vs. BWT)'

	if mimic_kraken:
		cmd_assign=[assign, '-i', '-', '-k', k, '-n', index_newick, '-m', 'h1', '-f', 'kraken', '-l', '-t']
	else:
		cmd_assign=[assign, '-i', '-', '-k', k, '-n', index_newick, '-m', measure, '-f', out_format]
		if annotate:
			cmd_assign+=['--annotate']
		if tie_lca:
			cmd_assign+=['--tie-lca']

	cmd_match=[exk, 'match', '-k', k, '-u' if use_klcp else '', index_fa, fq_fn]


	#(['|', '|'] if mimic_kraken else ['|']) \
	command=cmd_match + ['|'] + cmd_assign
	_run_safe(command)


########
# MAIN #
########

def main():
	try:
		parser = argparse.ArgumentParser()
		subparsers = parser.add_subparsers(help='sub-command help',dest='subcommand')
		fc=lambda prog: argparse.HelpFormatter(prog,max_help_position=27)

		##########

		parser_init = subparsers.add_parser('init', help='Initialize data', formatter_class=fc)
		parser_init.add_argument(
				'library',
				metavar='<library>',
				choices=LIBRARIES+['all'],
				help='genomic library {}'.format(LIBRARIES+['all']),
			)
		parser_init.add_argument(
				'-m','--prophyle-dir',
				metavar='DIR',
				dest='home_dir',
				type=str,
				default=DEFAULT_HOME_DIR,
				help='ProPhyle directory [{}]'.format(DEFAULT_HOME_DIR),
			)

		##########

		parser_index = subparsers.add_parser('index', help='Create index', formatter_class=fc)
		parser_index.add_argument(
				'-n','--newick',
				metavar='FILE',
				dest='newick',
				type=str,
				help='taxonomy tree (in Newick format)',
				required=True,
			)
		parser_index.add_argument(
				'index_dir',
				metavar='<index.dir>',
				type=str,
				help='index directory (will be created)',
			)
		parser_index.add_argument(
				'-l','--lib-dir',
				metavar='DIR',
				dest='library_dir',
				type=str,
				help='directory with genomic sequences',
				required=True,
			)
		parser_index.add_argument(
				'-t','--threads',
				metavar='INT',
				dest='threads',
				type=int,
				help='number of threads [auto={}]'.format(DEFAULT_THREADS),
				default=DEFAULT_THREADS,
			)
		parser_index.add_argument(
				'-k','--kmer-len',
				dest='k',
				metavar='INT',
				type=int,
				help='k-mer length [{}]'.format(DEFAULT_K),
				default=DEFAULT_K,
			)
		parser_index.add_argument(
				'--continue',
				dest='ccontinue',
				action='store_true',
				help='continue with index construction (construct only missing parts)',
			)

		##########

		parser_classify = subparsers.add_parser('classify', help='Classify reads', formatter_class=fc)
		parser_classify.add_argument(
				'index_dir',
				metavar='<index.dir>',
				type=str,
				help='index directory',
			)
		parser_classify.add_argument(
				'reads',
				metavar='<reads.fq>',
				type=str,
				help='file with reads in FASTA or FASTQ [- for standard input]',
			)
		parser_classify.add_argument(
				'-k','--kmer-len',
				dest='k',
				metavar='INT',
				type=int,
				help='k-mer length [{}]'.format(DEFAULT_K),
				default=DEFAULT_K,
			)
		parser_classify.add_argument(
				'-n','--no-klcp',
				dest='klcp',
				action='store_false',
				help='do not use k-LCP',
			)
		parser_classify.add_argument(
				'-m','--measure',
				dest='measure',
				choices=['h1','c1'],
				help='measure: h1=hit count, c1=coverage [{}]'.format(DEFAULT_MEASURE),
				default=DEFAULT_MEASURE,
			)
		parser_classify.add_argument(
				'-o','--out-form',
				dest='oform',
				choices=['kraken','sam'],
				default='sam',
				help='output format',
			)
		parser_classify.add_argument(
				'--annotate',
				dest='annotate',
				action='store_true',
				help='annotate assignments',
			)
		parser_classify.add_argument(
				'--tie-lca',
				dest='tie',
				action='store_true',
				help='use LCA when tie (multiple hits with the same score)',
			)
		parser_classify.add_argument(
				'--mimic-kraken',
				dest='mimic',
				action='store_true',
				help='mimic Kraken algorithm and output (for debugging purposes)',
			)

		##########

		args = parser.parse_args()
		subcommand=args.subcommand

		if subcommand=="init":
			init(
					library=args.library,
					home_dir=args.home_dir,
				)

		elif subcommand=="index":
			index(
					index_dir=args.index_dir,
					threads=args.threads,
					k=args.k,
					newick_fn=args.newick,
					library_dir=args.library_dir,
					ccontinue=args.ccontinue,
				)

		elif subcommand=="classify":
			classify(
					index_dir=args.index_dir,
					fq_fn=args.reads,
					k=args.k,
					use_klcp=args.klcp,
					out_format=args.oform,
					mimic_kraken=args.mimic,
					measure=args.measure,
					tie_lca=args.tie,
					annotate=args.annotate,
				)

		else:
			parser.print_help()
			sys.exit(1)

	except (IOError, OSError):
		sys.exit(0)

if __name__ == "__main__":
	main()