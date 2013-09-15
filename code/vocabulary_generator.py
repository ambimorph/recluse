# vocabulary_generator.py

import subprocess, os, shutil, sys
from utils import open_with_unicode
import vocabulary_cutter

class VocabularyGenerator():

    """
    Uses the SRILM toolkit to generate unigram counts and then cuts
    down to size with the most frequent words.
    """

    def __init__(self, lines_per_chunk=100000):
        self.lines_per_chunk = lines_per_chunk
        self.temporary_data_directory = 'TEMP_DATA_DIR/'

    def split_file_into_chunks(self, file_name):

        """
        Assumes bzip2 compression.
        """

        file_obj = open_with_unicode(file_name, 'bzip2', 'r')
        current_line_number = 0
        current_file_number = 0
        end_of_file = False
        while not end_of_file:
            current_filename = self.temporary_chunk_directory + '%03d' % current_file_number + '.bz2'
            current_file_obj = open_with_unicode(current_filename, 'bzip2', 'w')
            current_file_obj.write(file_obj.readline())
            current_line_number += 1
            while current_line_number % self.lines_per_chunk > 0:
                current_line = file_obj.readline()
                end_of_file = current_line == ''
                current_file_obj.write(current_line)
                current_line_number += 1
            current_file_number += 1
        return

    def srilm_make_merge_batch_counts(self, file_name):

        file_names_file_obj = open(self.temporary_chunk_directory + 'file_names', 'w')
        file_names_file_obj.writelines([self.temporary_chunk_directory + s + '\n' for s in os.listdir(self.temporary_chunk_directory) if s != 'file_names'])
        file_names_file_obj.close()
        srilm_make_batch_counts = subprocess.call(['make-batch-counts', self.temporary_chunk_directory + 'file_names', '1', 'code/nltkbasedsegmentandtokenise.sh', self.temporary_counts_directory, '-write-order 1'])
        srilm_merge_batch_counts = subprocess.call(['merge-batch-counts', self.temporary_counts_directory])

    def generate_vocabulary(self, text_file_name, size, vocabulary_file_obj):
        
        assert not os.path.isdir(self.temporary_data_directory)
        os.mkdir(self.temporary_data_directory)
        self.temporary_chunk_directory = self.temporary_data_directory + 'TEMP_CHUNK_DIR/'
        os.mkdir(self.temporary_chunk_directory)
        self.temporary_counts_directory = self.temporary_data_directory + 'TEMP_COUNTS_DIR/'
        os.mkdir(self.temporary_counts_directory)

        self.split_file_into_chunks(text_file_name) 
        self.srilm_make_merge_batch_counts(text_file_name)
        merged_counts_file = [f for f in os.listdir(self.temporary_counts_directory) if f.endswith('.ngrams.gz')][0]
        unigram_counts_file_obj = open_with_unicode(self.temporary_counts_directory + merged_counts_file, 'gzip', 'r')
        cutter = vocabulary_cutter.VocabularyCutter(unigram_counts_file_obj, vocabulary_file_obj)
        cutter.cut_vocabulary(size)
        
        shutil.rmtree(self.temporary_data_directory)


if __name__ == '__main__':
    infile_name = sys.argv[1]
    size = int(sys.argv[2])
    outfile_obj = sys.stdout
    vg = VocabularyGenerator()
    vg.generate_vocabulary(infile_name, size, outfile_obj)
