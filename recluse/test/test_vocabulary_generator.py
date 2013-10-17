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
        words = out_file_obj.getvalue().split()
        self.assertEqual(words, [u',', u'"', u'the', u'of', u'<s>', u'</s>', u'.', u'and', u'-', u'anarchism', u'a', u'to', u'as', u'in', u'or', u'is', u'from', u'some', u'anarchists', u')']), words

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
        self.assertEqual(stdoutdata.split(), ['the', ',', '.', '<s>', '</s>', 'of', 'and', 'in', '"', 'to', 'a', 'is', '-', 'as', 'that', '<4-digit-integer>', 'for', 'was', 'with', "'s"]), stdoutdata.split()
        
        shutil.rmtree(temporary_chunk_directory)

if __name__ == '__main__':
    unittest.main()
