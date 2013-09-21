# vocabulary_generator.py

import subprocess, os, shutil, sys
from utils import *
import vocabulary_cutter

class VocabularyGenerator():

    """
    Uses the SRILM toolkit to generate unigram counts and then cuts
    down to size with the most frequent words.
    """

    def __init__(self, lines_per_chunk=100000):
        self.lines_per_chunk = lines_per_chunk
        self.temporary_data_directory = 'TEMP_DATA_DIR/'

    def srilm_make_merge_batch_counts(self, chunk_directory):

        self.temporary_counts_directory = self.temporary_data_directory + 'TEMP_COUNTS_DIR/'
        os.mkdir(self.temporary_counts_directory)
        file_names_file_obj = open(chunk_directory + 'file_names', 'w')
        file_names_file_obj.writelines([chunk_directory + s + '\n' for s in os.listdir(chunk_directory) if s != 'file_names'])
        file_names_file_obj.close()
        srilm_make_batch_counts = subprocess.call(['make-batch-counts', chunk_directory + 'file_names', '1', 'recluse/nltkbasedsegmentandtokenise.sh', self.temporary_counts_directory, '-write-order 1'])
        srilm_merge_batch_counts = subprocess.call(['merge-batch-counts', self.temporary_counts_directory])

    def generate_vocabulary(self, text_file_name, size, vocabulary_file_obj):
        
        assert not os.path.isdir(self.temporary_data_directory)
        os.mkdir(self.temporary_data_directory)

        temporary_chunk_directory = self.temporary_data_directory + 'TEMP_CHUNK_DIR/'
        os.mkdir(temporary_chunk_directory)
        split_file_into_chunks(text_file_name, temporary_chunk_directory, self.lines_per_chunk) 

        self.srilm_make_merge_batch_counts(temporary_chunk_directory)
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
