Recluse

Author: L. Amber Wilcox-O'Hearn

Contact: amber@cs.toronto.edu

Released under the GNU AFFERO GENERAL PUBLIC LICENSE, see COPYING file for details.

==============
Introduction
==============

recluse (Reproducible Experimentation for Computational Linguistics USE) is a set of tools for running computational linguistics experiments reproducibly.

This version contains 

* utils, which has four functions:
** open_with_unicode for reading and writing unicode with regular or compressed text
** split_file_into_chunks for splitting a file into smaller pieces.  This is needed for some tools that load everything into RAM, or train on all the data when we would be satisfied with training on partial data.
** partition_by_list works like a combination of the string methods partition and split; it keeps the separators, but partitions into a list.
** precision_recall_f_measure calculates those things.

* article_selector (to replace article_randomiser below), reproducibly randomly selects a portion of a large corpus for the experiment, divides it into training, development, and test sets, and returns an article index to those sets.
* article_randomiser, which reproducibly randomly divides a corpus into training, development, and test sets.
* nltk_based_segmenter_tokeniser, which does sentence segmentation and word tokenisation.
  It is optimised for Wikipedia type text.
* vocabulary_generator and the helper class vocabulary_cutter.  This wraps srilm as it makes unigram counts, and then selects the most frequent.


============
Dependencies
============

recluse depends on the pypi package `regex`_, which (unlike re) has unicode category support.

    sudo pip install regex

==========
Installing
==========

recluse is registered with pypi, so can be installed with pip:

    sudo pip install recluse


.. _regex: https://pypi.python.org/pypi/regex/
