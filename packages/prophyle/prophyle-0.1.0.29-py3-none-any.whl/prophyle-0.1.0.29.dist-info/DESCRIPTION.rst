ProPhyle – accurate and resource-frugal phylogeny-based metagenomic classification
==================================================================================


.. image:: https://travis-ci.org/karel-brinda/prophyle.svg?branch=master
	:target: https://travis-ci.org/karel-brinda/prophyle

ProPhyle is a metagenomic classifier based on BWT-index and phylogenetic trees.
The indexing strategy is based on the bottom-up propagation of k-mers in the tree,
assembling contigs at each node and matching using a standard full-text search.
The analysis of shared k-mers between NGS reads and the genomes in the index determines
which nodes are the best candidates for their classification.

More information can be found in our `poster <http://brinda.cz/publications/2017_cmda_prophyle.pdf>`_.


Getting started
---------------

Prerequisities
^^^^^^^^^^^^^^

* GCC 4.8+
* ZLib
* Python 3 with ete3 library
* SamTools



Installation using PIP
^^^^^^^^^^^^^^^^^^^^^^

>From PyPI::

	pip install --upgrade prophyle

>From Git::

	pip install --upgrade git+https://github.com/karel-brinda/prophyle

>From PyPI to the current directory::

	pip install --user prophyle
	export PYTHONUSERBASE=`pwd`
	export PATH=$PATH:`pwd`/bin


Installation using Conda
^^^^^^^^^^^^^^^^^^^^^^^^

Environment installation::

	conda create -y --name prophyle -c etetoolkit -c bioconda \
		python==3.6 ete3 bitarray samtools=1.3.1
	source activate prophyle
	pip install --upgrade prophyle


Environment activation::

	source activate prophyle


Examples
^^^^^^^^

Quick example (small k, subsampled bacterial database)::

	prophyle download bacteria
	prophyle index -k 10 ~/prophyle/test_bacteria.nw test_idx
	prophyle classify test_idx reads.fq > result.sam


Quick example (k=31, full bacterial database)::

	prophyle download bacteria
	prophyle index -k 31 ~/prophyle/bacteria.nw test_idx
	prophyle classify test_idx reads.fq > result.sam


