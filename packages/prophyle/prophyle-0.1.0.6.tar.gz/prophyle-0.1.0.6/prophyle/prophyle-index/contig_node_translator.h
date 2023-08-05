#ifndef CONTIG_NODE_TRANSLATOR_H
#define CONTIG_NODE_TRANSLATOR_H

#include <stdint.h>

int get_node_from_contig(int contig);
char* get_node_name(int node);
int get_node_name_length(const int node);
void add_contig(char* contig, int contig_number);

#endif //CONTIG_NODE_TRANSLATOR_H
