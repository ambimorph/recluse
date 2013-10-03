# vocabulary_generator.py

import subprocess, os, stat, shutil, sys
from utils import *
import vocabulary_cutter

class VocabularyGenerator():

    """
    Uses the SRILM toolkit to generate unigram counts and then cuts
    down to size with the most frequent words.
    """

    def __init__(self, file_names):
        self.file_names= file_names

    def srilm_make_merge_batch_counts(self, directory):

        file_names_file_obj = open(directory + 'file_names', 'w')
        file_names_file_obj.writelines([s + '\n' for s in self.file_names])
        file_names_file_obj.close()

        cwd = os.getcwd()

        bash_script_name = cwd + "/nltkbasedsegmentandtokenise.sh"
        bash_script_file_obj = open(bash_script_name, 'w')
        bash_script_file_obj.write("bzcat $1 | nltkbasedsegmentertokeniserrunner\n")
        bash_script_file_obj.close()
        os.chmod(bash_script_name, 0755)

        srilm_make_batch_counts = subprocess.call(['make-batch-counts', directory + 'file_names', '1', bash_script_name, directory, '-write-order 1'])
        srilm_merge_batch_counts = subprocess.call(['merge-batch-counts', directory])

        os.remove(bash_script_name)

    def generate_vocabulary(self, size, vocabulary_file_obj):
        
        temporary_directory = 'TEMP_DIR/'
        if not os.path.isdir(temporary_directory):
            os.mkdir(temporary_directory)
        self.srilm_make_merge_batch_counts(temporary_directory)
        merged_counts_file = [f for f in os.listdir(temporary_directory) if f.endswith('.ngrams.gz')][0]
        unigram_counts_file_obj = open_with_unicode(temporary_directory + merged_counts_file, 'gzip', 'r')
        cutter = vocabulary_cutter.VocabularyCutter(unigram_counts_file_obj, vocabulary_file_obj)
        cutter.cut_vocabulary(size)
        
        shutil.rmtree(temporary_directory)


if __name__ == '__main__':
    size = int(sys.argv[1])
    file_names = sys.argv[2:]
    outfile_obj = sys.stdout
    vg = VocabularyGenerator(file_names)
    vg.generate_vocabulary(size, outfile_obj)
