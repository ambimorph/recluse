# L. Amber Wilcox-O'Hearn 2011
# test_article_randomiser.py

from recluse import article_randomiser
import unittest, StringIO, random, subprocess, bz2, os


class ArticleRandomiserTest(unittest.TestCase):

    def test_randomise(self):

        r = random.Random(999)

        article_separation_line = "---END.OF.DOCUMENT---\n"

        a1 = ["Anarchism.\n", "Anarchism is a political philosophy which considers the state undesirable, unnecessary and harmful, and instead promotes a stateless society, or anarchy. It seeks to diminish or even abolish authority in the conduct of human relations. Anarchists may widely disagree on what additional criteria are required in anarchism. \"The Oxford Companion to Philosophy\" says, \"there is no single defining position that all anarchists hold, and those considered anarchists at best share a certain family resemblance.\"", "---END.OF.DOCUMENT---\n"]
        a2 = ["Hidehiko Shimizu.\n", "Hidehiko Shimizu (born 4 November 1954) is a former Japanese football player. He has played for Nissan Motors.\n", "---END.OF.DOCUMENT---\n"]
        a3 = ["Some other thing.\n", "this\n", "could\n", "be a line or three.\n", "---END.OF.DOCUMENT---\n"]
        a4 = ["Finally.\n", "Another one.\n", "---END.OF.DOCUMENT---\n"]

        newline_list = ["\n"]

        article_file_obj = a1 + newline_list + a2 + newline_list + a3 + newline_list + a4

        train_file_obj = StringIO.StringIO()
        devel_file_obj = StringIO.StringIO()
        test_file_obj = StringIO.StringIO()

        ar = article_randomiser.Randomiser(article_file_obj, train_file_obj, devel_file_obj, test_file_obj, r)
        ar.randomise()
        assert train_file_obj.getvalue() == "".join(a2+a4), "".join(a2+a4) + train_file_obj.getvalue()
        assert devel_file_obj.getvalue() == "".join(a1), "".join(a1) + devel_file_obj.getvalue()
        assert test_file_obj.getvalue() == "".join(a3),  "".join(a3) + test_file_obj.getvalue() 

    def test_command_line(self):

        randomize = subprocess.Popen(['python', 'recluse/article_randomiser.py', "---END.OF.DOCUMENT---", '.5', '.3', '.2'], stdin=-1, stdout=-1, stderr=-1 )
        test_data_reader = bz2.BZ2File('recluse/test/data/small_westbury.txt.bz2', 'r')
        randomize.communicate(input=test_data_reader.read())
        self.assertEqual(randomize.returncode, 0)
        num_train = subprocess.Popen(['grep', '-c', 'END', 'train'], stdout=-1)
        self.assertEqual(int(num_train.stdout.read()), 11), num_train
        num_devel = subprocess.Popen(['grep', '-c', 'END', 'devel'], stdout=-1)
        self.assertEqual(int(num_devel.stdout.read()), 5), num_devel
        num_test = subprocess.Popen(['grep', '-c', 'END', 'test'], stdout=-1)
        self.assertEqual(int(num_test.stdout.read()), 2), num_test
        os.remove('train')
        os.remove('devel')
        os.remove('test')

if __name__ == '__main__':
    unittest.main()
