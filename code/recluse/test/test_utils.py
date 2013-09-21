# test_utils.py

import unittest, os, shutil
from recluse import utils


class UtilsTest(unittest.TestCase):

    def test_open_with_unicode(self):

        infile_obj = utils.open_with_unicode('recluse/test/data/segmenter_training', None, 'r')
        first_line = infile_obj.readline()
        self.assertEqual(first_line, u'\n'), first_line
        self.assertEqual(type(first_line), unicode), type(first_line)

        infile_obj = utils.open_with_unicode('recluse/test/data/small_westbury.txt.bz2', 'bzip2', 'r')
        first_line = infile_obj.readline()
        self.assertEqual(first_line, u'Anarchism.\n'), first_line
        self.assertEqual(type(first_line), unicode), type(first_line)

        infile_obj = utils.open_with_unicode('recluse/test/data/unigram_counts.gz', 'gzip', 'r')
        first_line = infile_obj.readline()
        self.assertEqual(first_line, u'funeral 4\n'), first_line
        self.assertEqual(type(first_line), unicode), type(first_line)

    def test_split_file_into_chunks(self):

        infile_name = 'recluse/test/data/unigram_counts.bz2'
        temp_dir_name = 'TEMP_DIR'
        while os.path.isdir(temp_dir_name):
            temp_dir_name += 'x'
        temp_dir_name += '/'
        os.mkdir(temp_dir_name)
        utils.split_file_into_chunks(infile_name, temp_dir_name, 5)
        self.assertTrue(os.path.isfile(temp_dir_name + '/000.bz2'))
        self.assertTrue(os.path.isfile(temp_dir_name + '/001.bz2'))
        self.assertTrue(os.path.isfile(temp_dir_name + '/002.bz2'))
        self.assertTrue(os.path.isfile(temp_dir_name + '/003.bz2'))
        self.assertTrue(os.path.isfile(temp_dir_name + '/004.bz2'))
        infile_obj = utils.open_with_unicode(temp_dir_name + '/003.bz2', 'bzip2', 'r')
        first_line  = infile_obj.readline()
        self.assertEqual(first_line, u'holy 2\n'), first_line
        shutil.rmtree(temp_dir_name)
        

if __name__ == '__main__':
    unittest.main()
