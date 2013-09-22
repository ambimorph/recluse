# test_vocabulary_generator.py

from recluse import vocabulary_generator
from recluse.utils import split_file_into_chunks
import unittest, StringIO, subprocess, os, shutil

size = 20
file_names = ['recluse/test/data/f1.bz2', 'recluse/test/data/f2.bz2', 'recluse/test/data/f3.bz2']

class VocabularyGeneratorTest(unittest.TestCase):

    def test_vocabulary_generator(self):

        vg = vocabulary_generator.VocabularyGenerator(file_names)
        out_file_obj = StringIO.StringIO()
        vg.generate_vocabulary(size, out_file_obj)
        words = out_file_obj.getvalue()
        self.assertEqual(words, u',\n"\nthe\nof\n<s>\n</s>\n.\nand\n-\nanarchism\na\nto\nas\nin\nor\nis\nfrom\nsome\nanarchists\n)\n'), words

    def test_command_line(self):
        text_file_name = 'recluse/test/data/small_westbury.txt.bz2'
        vg = vocabulary_generator.VocabularyGenerator(text_file_name)
        temporary_chunk_directory = 'TEMP_CHUNK_DIR/'
        os.mkdir(temporary_chunk_directory)
        lines_per_chunk = 500
        split_file_into_chunks(text_file_name, temporary_chunk_directory, lines_per_chunk) 
        file_names = [s for s in os.listdir(temporary_chunk_directory)]

        generate_vocab = subprocess.Popen(['python', 'recluse/vocabulary_generator.py', str(size)] + [temporary_chunk_directory + '/' + fn for fn in file_names], stdin=-1, stdout=-1, stderr=-1)
        (stdoutdata, stderrdata) = generate_vocab.communicate()
        self.assertEqual(generate_vocab.returncode, 0)
        self.assertEqual(stdoutdata, 'the\n,\n<s>\n</s>\n.\nof\nand\nin\n"\nto\na\nis\n-\nas\nthat\n<4-digit-integer>\nfor\nwas\nwith\n)\n'), stdoutdata
        
        shutil.rmtree(temporary_chunk_directory)

if __name__ == '__main__':
    unittest.main()
