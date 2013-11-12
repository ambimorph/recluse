# 2012 L. Amber Wilcox-O'Hearn

import sys, bisect

class VocabularyCutter():
    """
    Takes a file of unigram counts and returns a file of the top n
    most frequent words.
    If there are fewer than n words, it returns them all.
    """
    def __init__(self, infile_obj, outfile_obj):
        self.infile_obj = infile_obj
        self.outfile_obj = outfile_obj

    def cut_vocabulary(self, n=None, min_frequency=None):
        frequencies = []
        for line in self.infile_obj:
            tokens = line.split()
            assert len(tokens) == 2, line
            bisect.insort( frequencies, (int(tokens[1]), tokens[0]) )
        if min_frequency is not None:
            frequencies = [x for x in frequencies if x[0] >= min_frequency]
        if n is None: 
            n = len(frequencies)
        else:
            n = min(n, len(frequencies))
        for i in range(n):
            self.outfile_obj.write(frequencies[-1-i][1])
            self.outfile_obj.write('\n')

if __name__ == '__main__':
    infile_obj = sys.stdin
    outfile_obj = sys.stdout
    vc = VocabularyCutter(infile_obj, outfile_obj)
    try:
        n = int(sys.argv[1])
    except ValueError:
        n = None
    try:
        min_freq = int(sys.argv[2])
    except ValueError:
        min_freq = None
    vc.cut_vocabulary(n=n, min_frequency=min_freq)
