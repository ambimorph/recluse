=========
RECLUSE
=========

Release 0.4.4 (2014-03-17)
..........................
* NON-BACKWARDS-COMPATIBLE change to open_with_unicode parameters: now compression_type is a keyword argument; when left out, transparently falls back to opening with no compression, and matches the interface of regular Python open.
* Cleaned up a lot redundancy in open_with_unicode (Thank you, Allison Kaptur!)

Release 0.4.3 (2013-11-23)
..........................
* Wrapped the shutil.rmtree in vocabulary_generator in case of errors due to timing effects of .nsf files.

Release 0.4.2 (2013-11-11)
..........................
* Refined the vocabulary_cutter and vocabulary_generator so they can optionally use a frequency cutoff instead of a size.

Release 0.4.1 (2013-11-09)
..........................
* Refined the nltk_based_segmenter_tokeniser punkt object option; the punkt_obj must be an sbd attribute of an nltk.tokenise.punkt.PunktSentenceTokenizer.

Release 0.4.0 (2013-11-08)
..........................
* nltk_based_segmenter_tokeniser can now read in a punkt object from prior work, for example, a pickled one.

Release 0.3.2 (2013-11-03)
..........................
* Made a new module article_selector, intended to replace article_randomiser.

Release 0.3.1 (2013-11-03)
..........................
* README has some dependency and installation information.

Release 0.3.0 (2013-10-25)
..........................
* utils now has a function to calculate precision, recall, and f-measure.

Release 0.2.4 (2013-10-20)
..........................
* utils.partition_by_list now returns a list, not a tuple.

Release 0.2.1 (2013-10-17)
..........................
* Fixed a unicode issue: the commandline version of the tokeniser must decode before sending to stdout.
* Updated a regression test of vocabulary generator that had slightly different output based on changes to the tokenisation.

Release 0.2.0 (2013-10-16)
..........................
* Changed the interface to nltk_based_segmenter_tokeniser.  
** It still can return a generator of sentences, and prints out tokenised segmented sentences when used on the commandline.
** The generator now yields sentences in strings, either the original or the tokenised version
** Methods for doing the tokenisation are provided separately.
** This puts the burden of aligning tokenised text to original text in the client, while still allowing the client access to the information needed to do so.
* There is a change in dealing with contractions; we now follow the convention of separating a contraction into two parts with the apostrophe attached to the second part.

Release 0.1.21 (2013-10-03)
..........................
* data needed for testing should now be included.

Release 0.1.20 (2013-10-03)
..........................
* vocabulary_generator now writes a temporary bash script for srilm to call that invokes nltkbasedsegmentertokeniserrunner.
* The intermediate directory 'code/' has been removed.

Release 0.1.19 (2013-10-03)
..........................
* vocabulary_cutter now falls back to including all words if n is greater than the original size.
* There is now a script called nltkbasedsegmentertokeniserrunner that simply imports and runs the corresponding module.

Release 0.1.14 (2013-09-22)
..........................
* Changed the interface and functionality of vocabulary_generator.  It no longer does splitting of large files.  Instead it takes a list of file names, and the calling function can decide whether or not to split.

Release 0.1.10 (2013-09-21)
..........................
* Added versioneer to deal with git+pypi package management.
* Moved the split_file_into_chunks function that had been in vocabulary_generator into utils.
* Made unit tests for utils.py

Release 0.1.7 (2013-09-15)
..........................
* Fixed pathnames in tests to go along with new packaging structure.

Release 0.1.6 (2013-09-15)
..........................
* Fixed packaging error in which the package was named 'code' instead of 'recluse'.

Release 0.1.5 (2013-09-15)
..........................
* Added vocabulary building tools: vocabulary_cutter and vocabulary_generator.

Release 0.1.4 (2013-09-14)
..........................
* Little typographical fixes.

Release 0.1.3 (2013-09-14)
..........................
* Little typographical fixes.

Release 0.1.2 (2013-09-14)
..........................
* Added the nltk_based_segmenter_tokeniser.


Release 0.1.1 (2013-09-10)
..........................
* Added a test of the commandline functionality of article_randomizer.
* Added utils.py with the open_with_unicode function.


Release 0.1.0 (2013-09-05)
..........................
Initial release.
