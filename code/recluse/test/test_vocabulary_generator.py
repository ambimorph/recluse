# test_vocabulary_generator.py

from recluse import vocabulary_generator
import unittest, StringIO, subprocess, bz2


class VocabularyGeneratorTest(unittest.TestCase):

    @classmethod
    def setUpClass(self):
        self.vg = vocabulary_generator.VocabularyGenerator()
        self.text_file_name = 'recluse/test/data/small_westbury.txt.bz2'
        self.size = 20

    def test_no_merge(self):
        out_file_obj = StringIO.StringIO()
        self.vg.generate_vocabulary(self.text_file_name, self.size, out_file_obj)
        words = out_file_obj.getvalue()
        self.assertEqual(words, u'the\n,\n<s>\n</s>\n.\nof\nand\nin\n"\nto\na\nis\n-\nas\nthat\n<4-digit-integer>\nfor\nwas\nwith\n)\n'), words

    def test_merge(self):
        out_file_obj = StringIO.StringIO()
        self.vg.lines_per_chunk = 500
        self.vg.generate_vocabulary(self.text_file_name, self.size, out_file_obj)
        words = out_file_obj.getvalue()
        self.assertEqual(words, u'the\n,\n<s>\n</s>\n.\nof\nand\nin\n"\nto\na\nis\n-\nas\nthat\n<4-digit-integer>\nfor\nwas\nwith\n)\n'), words

    def test_command_line(self):
        generate_vocab = subprocess.Popen(['python', 'recluse/vocabulary_generator.py', self.text_file_name, str(self.size)], stdin=-1, stdout=-1, stderr=-1)
        test_data_reader = bz2.BZ2File('recluse/test/data/small_westbury.txt.bz2', 'r')
        (stdoutdata, stderrdata) = generate_vocab.communicate(input=test_data_reader.read())
        self.assertEqual(generate_vocab.returncode, 0)
        self.assertEqual(stdoutdata, 'the\n,\n<s>\n</s>\n.\nof\nand\nin\n"\nto\na\nis\n-\nas\nthat\n<4-digit-integer>\nfor\nwas\nwith\n)\n'), stdoutdata
        


if __name__ == '__main__':
    unittest.main()
