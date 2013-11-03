# test_article_selector.py

from recluse import article_selector
import unittest, StringIO, random


class ArticleSelectorTest(unittest.TestCase):

    def test_select_and_distribute(self):

        r = random.Random(21)

        a0 = "Anarchism.\nAnarchism is a political philosophy which considers the state undesirable, unnecessary and harmful, and instead promotes a stateless society, or anarchy. It seeks to diminish or even abolish authority in the conduct of human relations. Anarchists may widely disagree on what additional criteria are required in anarchism. \"The Oxford Companion to Philosophy\" says, \"there is no single defining position that all anarchists hold, and those considered anarchists at best share a certain family resemblance.\"\n---END.OF.DOCUMENT---\n\n"
        a1 = "Hidehiko Shimizu.\nHidehiko Shimizu (born 4 November 1954) is a former Japanese football player. He has played for Nissan Motors.\n---END.OF.DOCUMENT---\n\n"
        a2 = "Some other thing.\nthis\ncould\nbe a line or three.\n---END.OF.DOCUMENT---\n\n"
        a3 = "Finally.\nAnother one.\n---END.OF.DOCUMENT---\n\n"
        a4 = "Autism.\nAutism is a disorder of neural development characterized by impaired social interaction and communication, and by restricted and repetitive behavior. These signs all begin before a child is three years old. Autism affects information processing in the brain by altering how nerve cells and their synapses connect and organize; how this occurs is not well understood. The two other autism spectrum disorders (ASD) are Asperger syndrome, which lacks delays in cognitive development and language, and PDD-NOS, diagnosed when full criteria for the other two disorders are not met.\nAutism has a strong genetic basis, although the genetics of autism are complex and it is unclear whether ASD is explained more by rare mutations, or by rare combinations of common genetic variants. In rare cases, autism is strongly associated with agents that cause birth defects. Controversies surround other proposed environmental causes, such as heavy metals, pesticides or childhood vaccines; the vaccine hypotheses are biologically implausible and lack convincing scientific evidence. The prevalence of autism is about 1-2 per 1,000 people; the prevalence of ASD is about 6 per 1,000, with about four times as many males as females. The number of people diagnosed with autism has increased dramatically since the 1980s, partly due to changes in diagnostic practice; the question of whether actual prevalence has increased is unresolved.\nParents usually notice signs in the first two years of their child's life. The signs usually develop gradually, but some autistic children first develop more normally and then regress. Although early behavioral or cognitive intervention can help autistic children gain self-care, social, and communication skills, there is no known cure. Not many children with autism live independently after reaching adulthood, though some become successful. An autistic culture has developed, with some individuals seeking a cure and others believing autism should be tolerated as a difference and not treated as a disorder.\n---END.OF.DOCUMENT---\n"


        article_file_obj = StringIO.StringIO(a0+a1+a2+a3+a4)
        train_file_obj = StringIO.StringIO()
        devel_file_obj = StringIO.StringIO()
        test_file_obj = StringIO.StringIO()

        ar = article_selector.ArticleSelector(article_file_obj, train_file_obj, devel_file_obj, test_file_obj)
        result = ar.select_and_distribute(r, 5, 4, proportions=[.5, .25, .25])
        self.assertTupleEqual(result, ([0, 2], [1], [4])), result
        self.assertEqual(train_file_obj.getvalue(), a0+a2), train_file_obj.getvalue()
        self.assertEqual(devel_file_obj.getvalue(), a1), devel_file_obj.getvalue()
        self.assertEqual(test_file_obj.getvalue(), a4), test_file_obj.getvalue() 

if __name__ == '__main__':
    unittest.main()
