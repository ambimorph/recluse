# L. Amber Wilcox-O'Hearn 2011
# test_vocabulary_cutter.py

import unittest, StringIO, subprocess
from recluse import vocabulary_cutter


class VocabularyCutterTest(unittest.TestCase):

    def test_cut_vocabulary(self):

        infile_obj = open('recluse/test/data/unigram_counts', 'r')
        outfile_obj = StringIO.StringIO()

        vc = vocabulary_cutter.VocabularyCutter(infile_obj, outfile_obj)
        vc.cut_vocabulary(5)

        assert outfile_obj.getvalue() == "being\nheld\nGer\ndeficits\nChris\n", outfile_obj.getvalue()

    def test_commandline(self):

        cut_vocab = subprocess.Popen(['python', 'recluse/vocabulary_cutter.py', '5'], stdin=-1, stdout=-1, stderr=-1)
        infile_obj = open('recluse/test/data/unigram_counts', 'r')
        (stdoutdata, stderrdata) = cut_vocab.communicate(input=infile_obj.read())
        self.assertEqual(cut_vocab.returncode, 0)
        self.assertEqual(stdoutdata, "being\nheld\nGer\ndeficits\nChris\n")


if __name__ == '__main__':
    unittest.main()
