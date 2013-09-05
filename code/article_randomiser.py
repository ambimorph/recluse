# article_randomiser.py

# This script will create three directories: train, devel, and test, containing
# approximately the proportions specified of the total text, in a random
# order.  The default proportions are 60/20/20%.

# The articles are assumed to be separated by an identifying line.
# The default is that accompanying the Westbury Lab Wikipedia Corpus.
# The Westbury Lab Corpus consists of a single file containing all and
# only the text of the articles of Wikipedia.  Each article begins
# with a title on a single line, and ends with
# "---END.OF.DOCUMENT---\n\n"

import sys, random

class Randomiser():
    def __init__(self, article_file_obj, train_file_obj, devel_file_obj, test_file_obj, rand_obj, proportions=[.6,.2,.2], article_separation_line="---END.OF.DOCUMENT---\n") :
        self.article_file_obj = article_file_obj
        self.train_file_obj = train_file_obj
        self.devel_file_obj = devel_file_obj
        self.test_file_obj = test_file_obj
        self.proportions = proportions
        self.rand_obj = rand_obj
        assert sum(self.proportions) == 1, proportions
        self.article_separation_line = article_separation_line

    def choose_outfile(self):
        x = self.rand_obj.random()
        if x < self.proportions[0]: return self.train_file_obj
        if x < self.proportions[0] + self.proportions[1]: return self.devel_file_obj
        return self.test_file_obj
        
    def randomise(self):
        blank_between_articles = False
        outfile = self.choose_outfile()
        for line in self.article_file_obj:
            if line == self.article_separation_line:
                outfile.write(line)
                blank_between_articles = True
            elif blank_between_articles:
                outfile = self.choose_outfile()
                blank_between_articles = False
            else:
                outfile.write(line)


if __name__ == '__main__':
    article_file_obj = sys.stdin
    train_file_obj = open("train", 'w')
    devel_file_obj = open("devel", 'w')
    test_file_obj = open("test", 'w')
    r = random.Random(9)
    article_separation_line = sys.argv[1] + '\n'
    proportions = [float(s) for s in sys.argv[2:5]]
    ar = Randomiser(article_file_obj, train_file_obj, devel_file_obj, test_file_obj, r, proportions, article_separation_line)
    ar.randomise()
