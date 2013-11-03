# article_selector.py

class ArticleSelector():

    """
    This script is designed to set up an experiment by selecting
    training, development and test sets out of a large corpus of
    articles.  The corpus in mind is the Westbury Lab Wikipedia
    Corpus.

    It randomly chooses n articles out of a set m >= n articles.  It
    then splits them into the required sets approximating a specified
    distribution. m must be known in advance.

    The default proportions are 60/20/20%, and the default separating
    line is "---END.OF.DOCUMENT---\n", the WestburyLab separator.
    """

    def __init__(self, article_file_obj, train_file_obj, devel_file_obj, test_file_obj, article_separation_line="---END.OF.DOCUMENT---\n") :

        self.article_file_obj = article_file_obj
        self.train_file_obj = train_file_obj
        self.devel_file_obj = devel_file_obj
        self.test_file_obj = test_file_obj
        self.article_separation_line = article_separation_line

    def select_and_distribute(self, rand_obj, m, n, proportions=[.6,.2,.2]):

        assert sum(proportions) == 1, proportions

        selection = rand_obj.sample(xrange(m),n)
        slices = [int(n*proportions[0]), int(n*(proportions[0]+proportions[1]))]
        training_indices = selection[:slices[0]]
        development_indices = selection[slices[0]:slices[1]]
        test_indices = selection[slices[1]:]

        article_number = 0
        article = ''
        line = self.article_file_obj.readline()
        while line:
            while line != self.article_separation_line:
                article += line
                line = self.article_file_obj.readline()
            article += line
            line = self.article_file_obj.readline() # blank between articles
            article += line
        
            if article_number in selection:
                if article_number in training_indices:
                    self.train_file_obj.write(article)
                elif article_number in development_indices:
                    self.devel_file_obj.write(article)
                else:
                    assert article_number in test_indices
                    self.test_file_obj.write(article)
        
            article_number += 1
            article = ''
            line = self.article_file_obj.readline()

        return training_indices, development_indices, test_indices
