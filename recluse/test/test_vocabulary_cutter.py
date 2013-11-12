# test_vocabulary_cutter.py

import unittest, StringIO, subprocess
from recluse import vocabulary_cutter

class VocabularyCutterTest(unittest.TestCase):

    def test_cut_vocabulary_to_n(self):

        infile_obj = open('recluse/test/data/unigram_counts', 'r')
        outfile_obj = StringIO.StringIO()

        vc = vocabulary_cutter.VocabularyCutter(infile_obj, outfile_obj)
        vc.cut_vocabulary(n=5)

        assert outfile_obj.getvalue() == "being\nheld\nGer\ndeficits\nChris\n", outfile_obj.getvalue()

    def test_n_greater_than_vocab(self):

        infile_obj = open('recluse/test/data/unigram_counts', 'r')
        outfile_obj = StringIO.StringIO()

        vc = vocabulary_cutter.VocabularyCutter(infile_obj, outfile_obj)
        vc.cut_vocabulary(n=50)

        assert outfile_obj.getvalue() == "being\nheld\nGer\ndeficits\nChris\nfocused\ndivided\nedge\nfuneral\nextra\ncontact\nadequate\ndirection\ndependence\nWestern\nholy\nexhibit\neves\ndemonstrated\nabandon\nSwedish\nArkansas\nfelon\nevocative\neducator\n", outfile_obj.getvalue()

    def test_min_frequency(self):

        infile_obj = open('recluse/test/data/unigram_counts', 'r')
        outfile_obj = StringIO.StringIO()

        vc = vocabulary_cutter.VocabularyCutter(infile_obj, outfile_obj)
        vc.cut_vocabulary(min_frequency=10)

        assert outfile_obj.getvalue() == "being\nheld\n", outfile_obj.getvalue()

    def test_min_frequency_and_max_n(self):

        infile_obj = open('recluse/test/data/unigram_counts', 'r')
        outfile_obj = StringIO.StringIO()
        vc = vocabulary_cutter.VocabularyCutter(infile_obj, outfile_obj)
        vc.cut_vocabulary(n=5, min_frequency=10)
        assert outfile_obj.getvalue() == "being\nheld\n", outfile_obj.getvalue()

        infile_obj = open('recluse/test/data/unigram_counts', 'r')
        outfile_obj = StringIO.StringIO()
        vc = vocabulary_cutter.VocabularyCutter(infile_obj, outfile_obj)
        vc.cut_vocabulary(n=5, min_frequency=3)
        assert outfile_obj.getvalue() == "being\nheld\nGer\ndeficits\nChris\n", outfile_obj.getvalue()


    def test_commandline(self):

        cut_vocab = subprocess.Popen(['python', 'recluse/vocabulary_cutter.py', '5', '3'], stdin=-1, stdout=-1, stderr=-1)
        infile_obj = open('recluse/test/data/unigram_counts', 'r')
        (stdoutdata, stderrdata) = cut_vocab.communicate(input=infile_obj.read())
        self.assertEqual(cut_vocab.returncode, 0)
        self.assertEqual(stdoutdata, "being\nheld\nGer\ndeficits\nChris\n")


if __name__ == '__main__':
    unittest.main()
