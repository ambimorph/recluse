# test_nltk_based_segmenter_tokeniser.py

from recluse.nltk_based_segmenter_tokeniser import *
import unittest, StringIO, subprocess, cPickle


class TokeniserTest(unittest.TestCase):

    def test_subtokenise(self):

        tokens = [u"I'd", u'Mr.', u'like', u"'that", u'150', u'150.', u'150,000.', u'$150,000.00.', u'L.']
        expected_subtokens = [[u'I', u"'d"], [u'Mr', u'.'], [u'like',], [u"'", u'that'], [u'150',], [u'150', u'.'], [u'150,000', u'.'], [u'$', u'150,000.00', u'.'], [u'L.',]]
        subtokens = [subtokenise(t) for t in tokens]
        self.assertListEqual(subtokens, expected_subtokens), subtokens

    def test_regularise(self):

        tokens = [u'1984', u'this', u'150,000.00']
        expected_regularised_tokens = [u'<4-digit-integer>', u'this', u'<3-digit-integer>,<3-digit-integer>.<2-digit-integer>']
        regularised_tokens = [regularise(t) for t in tokens]
        self.assertListEqual(regularised_tokens, expected_regularised_tokens), regularised_tokens

    def test_is_an_initial(self):

        tokens = [u'a.', u'ab.', u'a', u'.', u'.a', u'ab']
        expected_initials = [True, False, False, False, False, False]
        initials = [is_an_initial(t) for t in tokens]
        self.assertListEqual(initials, expected_initials), initials

    def test_is_multi_char_word_and_starts_with_a_capital(self):

        tokens = [u'L.', u'La', u'L', u'la']
        expected_evals = [True, True, False, False]
        evals = [is_multi_char_word_and_starts_with_a_capital(t) for t in tokens]
        self.assertListEqual(evals, expected_evals), evals

    def test_list_subtokenise_and_regularise(self):

        token_list = ["I'd", "like", "$150,000.00."]
        expected_list = [['I', "'d"], ['like',], ['$', '<3-digit-integer>,<3-digit-integer>.<2-digit-integer>', '.']]
        result = list_subtokenise_and_regularise(token_list)
        self.assertEqual(result, expected_list), result
    
    def test_sentence_tokenise_and_regularise(self):

        token_list = ["I'd", "like", "$150,000.00."]
        expected_string = "I 'd like $ <3-digit-integer>,<3-digit-integer>.<2-digit-integer> ."
        result = sentence_tokenise_and_regularise(token_list)
        self.assertEqual(result, expected_string), result
    
class SegmenterAndTokeniserTest(unittest.TestCase):

    @classmethod
    def setUpClass(self):
        training_text_file = open('recluse/test/data/segmenter_training', 'r')
        self.segmenter_tokeniser = NLTKBasedSegmenterTokeniser(infile_obj=training_text_file)

    # These are essentially all regression tests.

    def test_commandline(self):

        segment_and_tokenise = subprocess.Popen(['python', 'recluse/nltk_based_segmenter_tokeniser.py'], stdin=-1, stdout=-1, stderr=-1)
        (stdoutdata, stderrdata) = segment_and_tokenise.communicate(input="this's a test\" and. so is 1984.")
        self.assertEqual(segment_and_tokenise.returncode, 0, msg=stderrdata)
        self.assertEqual(stdoutdata, 'this \'s a test " and .\nso is <4-digit-integer> .\n'), stdoutdata

    def test_suffixes(self):

        text_to_segment_tokenise = u'Don\'t keep this together: -suffix'
        expected_text_output = 'don \'t keep this together : - suffix\n'
        result = [s for s in self.segmenter_tokeniser.sentence_segment(text=text_to_segment_tokenise)]
        self.assertEqual(result, [expected_text_output]), result

    def test_no_lower_no_tokens(self):

        text_to_segment_tokenise = u'Don\'t Lower ME.'

        expected_text_output = u'Don\'t Lower ME.\n'
        result = [s for s in self.segmenter_tokeniser.sentence_segment(text=text_to_segment_tokenise, tokenise=False, lower=False)]
        self.assertEqual(result, [expected_text_output]), result

        expected_text_output = u'don\'t lower me.\n'
        result = [s for s in self.segmenter_tokeniser.sentence_segment(text=text_to_segment_tokenise, tokenise=False)]
        self.assertEqual(result, [expected_text_output]), result

        expected_text_output = u'Don \'t Lower ME .\n'
        result = [s for s in self.segmenter_tokeniser.sentence_segment(text=text_to_segment_tokenise, lower=False)]
        self.assertEqual(result, [expected_text_output]), result

    def test_multiple_spaces_space_at_beginning_of_line(self):
        text_to_segment_tokenise = u'Extra  spaces     here \n and here'
        expected_text_output = [u'extra spaces here\n', u'and here\n']
        result = [s for s in self.segmenter_tokeniser.sentence_segment(text=text_to_segment_tokenise)]
        self.assertEqual(result, expected_text_output), result

    def test_initials(self):

        text_to_segment_tokenise = u'Neither was J. S. Bach.'
        expected_text_output = ['neither was j. s. bach .\n']
        result = [s for s in self.segmenter_tokeniser.sentence_segment(text=text_to_segment_tokenise)]
        self.assertEqual(result, expected_text_output), result

    def test_abbreviations(self):

        # This is, of course, incorrectly segmented, but correctly
        # characterises the behaviour of the segmenter.

        text_to_segment_tokenise = u'Mr. Shimizu was not born in the U.S. "You are just joking."'
        expected_text_output = ['mr. shimizu was not born in the u.s. " you are just joking . "\n']
        result = [s for s in self.segmenter_tokeniser.sentence_segment(text=text_to_segment_tokenise)]
        self.assertEqual(result, expected_text_output), result

    def test_dollar_percent_and_strings_of_consecutive_numbers(self):

        text_to_segment_tokenise = u"$1.50, 30%"
        expected_text_output = ['$ <1-digit-integer>.<2-digit-integer> , <2-digit-integer> %\n']
        result = [s for s in self.segmenter_tokeniser.sentence_segment(text=text_to_segment_tokenise)]
        self.assertEqual(result, expected_text_output), result

    def test_sentence_final_punctuation(self):

        text_to_segment_tokenise = u'Finally.\nFinally?\nFinally!'
        expected_text_output = ['finally .\n', 'finally ?\n', 'finally !\n']
        result = [s for s in self.segmenter_tokeniser.sentence_segment(text=text_to_segment_tokenise)]
        self.assertEqual(result, expected_text_output), result

    def test_mid_word(self):

        text_to_segment_tokenise = u'a line-or-three or 100,000.1 lines.  This&that.\nH. Amber Wilcox-O\'Hearn\n'+"They're his, not my brother's.\n3m/s"
        expected_text_output = [u'a line - or - three or <3-digit-integer>,<3-digit-integer>.<1-digit-integer> lines .\n', 'this & that .\n', 'h. amber wilcox - o \'hearn\n', 'they \'re his , not my brother \'s .\n', '<1-digit-integer>m / s\n']
        result = [s for s in self.segmenter_tokeniser.sentence_segment(text=text_to_segment_tokenise)]
        self.assertEqual(result, expected_text_output), result

    def test_elipses(self):

        text_to_segment_tokenise = u"Elipses here... and there..."
        expected_text_output = ['elipses here ... and there ...\n']
        result = [s for s in self.segmenter_tokeniser.sentence_segment(text=text_to_segment_tokenise)]
        self.assertEqual(result, expected_text_output), result

    def test_ints_with_or_without_following_punctuation(self):

        text_to_segment_tokenise = u'Hidehiko Shimizu (born 4 November 1954) is a former Japanese football player. He has played for Nissan Motors.'
        expected_text_output = ['hidehiko shimizu ( born <1-digit-integer> november <4-digit-integer> ) is a former japanese football player .\n', 'he has played for nissan motors .\n']
        result = [s for s in self.segmenter_tokeniser.sentence_segment(text=text_to_segment_tokenise)]
        self.assertEqual(result, expected_text_output), result

    def test_quotations_and_multiple_punctuation(self):

        text_to_segment_tokenise = u'Accordingly, "libertarian socialism" is sometimes used as a synonym for socialist anarchism, to distinguish it from "individualist libertarianism" (individualist anarchism). On the other hand, some use "libertarianism" to refer to individualistic free-market philosophy only, referring to free-market anarchism as "libertarian anarchism." '+"Citizens can oppose a decision ('besluit') made by a public body ('bestuursorgaan') within the administration\nThe Treaty could be considered unpopular in Scotland: Sir George Lockhart of Carnwath, the only member of the Scottish negotiating team against union, noted that `The whole nation appears against the Union' and even Sir John Clerk of Penicuik, an ardent pro-unionist and Union negotiator, observed that the treaty was `contrary to the inclinations of at least three-fourths of the Kingdom'."
        expected_text_output = ['accordingly , " libertarian socialism " is sometimes used as a synonym for socialist anarchism , to distinguish it from " individualist libertarianism " ( individualist anarchism ) .\n', 'on the other hand , some use " libertarianism " to refer to individualistic free - market philosophy only , referring to free - market anarchism as " libertarian anarchism . "\n', "citizens can oppose a decision ( ' besluit ' ) made by a public body ( ' bestuursorgaan ' ) within the administration\n", "the treaty could be considered unpopular in scotland : sir george lockhart of carnwath , the only member of the scottish negotiating team against union , noted that ` the whole nation appears against the union ' and even sir john clerk of penicuik , an ardent pro - unionist and union negotiator , observed that the treaty was ` contrary to the inclinations of at least three - fourths of the kingdom ' .\n"]
        result = [s for s in self.segmenter_tokeniser.sentence_segment(text=text_to_segment_tokenise)]
        self.assertEqual(result, expected_text_output), result

    def test_sentence_segmentation(self):

        text_to_segment_tokenise = u'Another libertarian tradition is that of unschooling and the free school in which child-led activity replaces pedagogic approaches. Experiments in Germany led to A. S. Neill founding what became Summerhill School in 1921. Summerhill is often cited as an example of anarchism in practice. However, although Summerhill and other free schools are radically libertarian, they differ in principle from those of Ferrer by not advocating an overtly-political class struggle-approach.\nThe Academy of Motion Picture Arts and Sciences itself was conceived by Metro-Goldwyn-Mayer studio boss Louis B. Mayer.  The 1st Academy Awards ceremony was held on Thursday, May 16, 1929, at the Hotel Roosevelt in Hollywood to honor outstanding film achievements of 1927 and 1928.\nWhen the Western Roman Empire collapsed, Berbers became independent again in many areas, while the Vandals took control over other parts, where they remained until expelled by the generals of the Byzantine Emperor, Justinian I. The Byzantine Empire then retained a precarious grip on the east of the country until the coming of the Arabs in the eighth century.'
        expected_text_output = ['another libertarian tradition is that of unschooling and the free school in which child - led activity replaces pedagogic approaches .\n', 'experiments in germany led to a. s. neill founding what became summerhill school in <4-digit-integer> .\n', 'summerhill is often cited as an example of anarchism in practice .\n', 'however , although summerhill and other free schools are radically libertarian , they differ in principle from those of ferrer by not advocating an overtly - political class struggle - approach .\n', 'the academy of motion picture arts and sciences itself was conceived by metro - goldwyn - mayer studio boss louis b. mayer .\n', 'the <1-digit-integer>st academy awards ceremony was held on thursday , may <2-digit-integer> , <4-digit-integer> , at the hotel roosevelt in hollywood to honor outstanding film achievements of <4-digit-integer> and <4-digit-integer> .\n', 'when the western roman empire collapsed , berbers became independent again in many areas , while the vandals took control over other parts , where they remained until expelled by the generals of the byzantine emperor , justinian i.\n', 'the byzantine empire then retained a precarious grip on the east of the country until the coming of the arabs in the eighth century .\n']
        result = [s for s in self.segmenter_tokeniser.sentence_segment(text=text_to_segment_tokenise)]
        self.assertEqual(result, expected_text_output), result

    def test_unicode(self):

        text_to_segment_tokenise = 'The term "anarchism" derives from the Greek \xe1\xbc\x84\xce\xbd\xce\xb1\xcf\x81\xcf\x87\xce\xbf\xcf\x82, "anarchos", meaning "without rulers", from the prefix \xe1\xbc\x80\xce\xbd- ("an-", "without") + \xe1\xbc\x80\xcf\x81\xcf\x87\xce\xae ("arch\xc3\xaa", "sovereignty, realm, magistracy") + -\xce\xb9\xcf\x83\xce\xbc\xcf\x8c\xcf\x82 ("-ismos", from the suffix -\xce\xb9\xce\xb6\xce\xb5\xce\xb9\xce\xbd, "-izein" "-izing").\nHere\xc2\xa0are\xc2\xa0some\xc2\xa0\nNBSPs!'.decode('utf-8')
        expected_text_output = ['the term " anarchism " derives from the greek \xe1\xbc\x84\xce\xbd\xce\xb1\xcf\x81\xcf\x87\xce\xbf\xcf\x82 , " anarchos " , meaning " without rulers " , from the prefix \xe1\xbc\x80\xce\xbd - ( " an - " , " without " ) + \xe1\xbc\x80\xcf\x81\xcf\x87\xce\xae ( " arch\xc3\xaa " , " sovereignty , realm , magistracy " ) + - \xce\xb9\xcf\x83\xce\xbc\xcf\x8c\xcf\x82 ( " - ismos " , from the suffix - \xce\xb9\xce\xb6\xce\xb5\xce\xb9\xce\xbd , " - izein " " - izing " ) .\n', 'here are some\nnbsps !\n']


    def test_get_punkt_from_pickle(self):

        pickled_punkt = cPickle.loads(cPickle.dumps(self.segmenter_tokeniser.sbd))
        new_segmenter_tokeniser = NLTKBasedSegmenterTokeniser(punkt_obj=pickled_punkt)
        self.assertEqual(len(new_segmenter_tokeniser.sbd._params.abbrev_types), 56)



if __name__ == '__main__':
    unittest.main()
