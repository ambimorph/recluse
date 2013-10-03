=========
RECLUSE
=========

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
