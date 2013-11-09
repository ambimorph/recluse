# nltk_based_segmenter_tokeniser.py

import nltk
import regex, sys, codecs, unicodedata, string
from recluse import utils

def subtokenise(token, abbreviation_list=[]):

    """
    Returns a tuple of disjoint, non-overlapping substrings that cover
    the token string.

    Subtokens are determined as follows:
    All unicode punctuation characters are considered tokens except:

    * Contractions will follow the convention of splitting into two
    parts, the second of which keeps the apostrophe.

    * Inter-numeric commas and periods stay token-internal.

    * Ellipses composed of periods are kept together as a single token.

    * Periods are kept on abbreviations, as given by the parameter,
      and initials.

    This function does not break strings on spaces.

    Examples: "I'd" -> ["I", "'d"]; "Mr." -> ["Mr", "."]; "like" -> ["like"]
    """
    
    if token[-1] == u'.':
        if token[:-1].lower() in abbreviation_list or is_an_initial(token):
            return [token]

    ellipses = r'\.\.\.'
    number = r'\p{N}+(?:[,\.]\p{N}+)+'
    contraction_part = r'(?<=\p{L})\'\p{L}+'
    other_punctuation = r'\p{P}|\p{S}'
    
    two_problems = regex.compile(r'|'.join([ellipses, number, contraction_part, other_punctuation]))

    return utils.partition_by_list(token, two_problems.findall(token))

def regularise(token):

    """
    Returns a replacement token for the token when appropriate.
    The only case in this version is replacing digit strings.
    Example: "1984" -> "<4-digit-integer>"
    """

    def repl(matchobj): return u'<' + str(len(matchobj.group())) + u'-digit-integer>'
    
    return regex.sub(r'(\p{N}+)', repl, token)

def list_subtokenise_and_regularise(token_list, abbreviation_list=[]):

    """
    Returns the regularised, subtokenised list of tokens.
    Example: ["I'd", "like", "$150,000.00."] -> 
    [['I', "'d"], ['like'], ['$',
    '<3-digit-integer>,<3-digit-integer>.<2-digit-integer>', '.']]
    """
    
    regularised_subtokenised_list = []
    for token in token_list:
        subtokens = [regularise(s) for s in subtokenise(token, abbreviation_list)]
        regularised_subtokenised_list.append(subtokens)

    return regularised_subtokenised_list

def sentence_tokenise_and_regularise(token_list, abbreviation_list=[]):

    """
    Returns the string formed by joining the regularised subtokens of
    each token in the list by spaces.
    Example: ["I'd", "like", "$150,000.00."] -> 
    "I 'd like $ <3-digit-integer>,<3-digit-integer>.<2-digit-integer> ."
    """

    subtokens = []
    for token in token_list:
        these_subtokens = subtokenise(token, abbreviation_list)
        for subtoken in these_subtokens:
            subtokens.append(regularise(subtoken))

    return u' '.join(subtokens)

def is_an_initial(word):

    return len(word) == 2 and unicodedata.category(word[0])[0] == 'L' and word[1] == u'.'

def is_multi_char_word_and_starts_with_a_capital(word):

    return len(word) > 1 and unicodedata.category(word[0]) == 'Lu'

class NLTKBasedSegmenterTokeniser():

    """
    This Segementer/Tokeniser is customised in the following ways:

    1. It has NLTK training parameters optimised for Wikipedia text
    (i.e. text that is inconsistent in its spelling of abbreviations,
    has an immense vocabulary, and is stylistically diverse and
    non-standard), as recommended by NLTK developers.

    2. This version replaces strings of digits with a special string
    that has only a digit count. TODO: make this optional.

    3. The tokenisation is almost completely reversible.  Tokenisation
    results in a TokenisedSentence which can be used either to emit
    tokens or to emit the original text stream.  EXCEPTION: note that
    in this version non-linebreaking whitespace is always collapsed to
    a single space, which violates complete reversibility.

    4. This version always starts by training on the supplied text.
    New text can also be supplied after the training (though this is
    not yet tested), but the training is not currenty loadable or
    savable. TODO: allow loaded segmentation models.

    """

    def __init__(self, infile_obj=None, punkt_obj=None):

        """
        Gets text and trains a segmenter with NLTK, or reads in
        previously trained segmenter.

        A punkt_obj is an sbd attribute of an
        nltk.tokenise.punkt.PunktSentenceTokenizer.
        """

        assert (infile_obj is None) ^ (punkt_obj is None)
        if infile_obj is not None:
            self.unicode_infile_obj = codecs.getreader('utf-8')(infile_obj)
            self.text = self.unicode_infile_obj.read()
            assert len(self.text) > 0
            trainer = nltk.tokenize.punkt.PunktTrainer()
            # Wikipedia optimisation:
            trainer.ABBREV = .15
            trainer.IGNORE_ABBREV_PENALTY = True
            trainer.INCLUDE_ALL_COLLOCS = True
            trainer.MIN_COLLOC_FREQ = 10
            # -----------------------
            trainer.train(self.text)
            self.sbd = nltk.tokenize.punkt.PunktSentenceTokenizer(trainer.get_params())
        else:
            self.sbd = punkt_obj


    def apply_ugly_hack_to_reattach_wrong_splits_in_certain_cases_with_initials(self, lines):
        """
        NLTK currently splits sentences between 2 initials.  Hacking
        those back together.  Also has the effect of collapsing
        whitespace to a single space char.
        """
        lines = list(lines)
        if len(lines) == 0: return []
        reattached_lines = []
        i = 0
        current_line = lines[i].split()
        while i < len(lines) - 1:
            reattach = False
            next_line = lines[i+1].split()
            last_word = current_line[-1]
            next_line_starts_with_a_capital = False
            first_word_of_next_line = next_line[0]
            if len(first_word_of_next_line) > 1 and unicodedata.category(first_word_of_next_line[0]) == 'Lu':
                next_line_starts_with_a_capital = True
            if is_an_initial(last_word):
                nltk_ortho_context = self.sbd._params.ortho_context[first_word_of_next_line.lower()]
                if unicodedata.category(first_word_of_next_line[0])[0] != 'L':
                    reattach = True
                # The following is an ugly and imperfect hack.  See mailing list for nltk.
                elif is_multi_char_word_and_starts_with_a_capital(first_word_of_next_line) and \
                        nltk_ortho_context <= 46 or \
                        is_an_initial(first_word_of_next_line):
                    reattach = True

            if reattach:
                    current_line += next_line
            else:
                reattached_lines.append(u' '.join(current_line))
                current_line = next_line
            i += 1 
        reattached_lines.append(u' '.join(current_line))
        return reattached_lines

    def sentence_segment(self, text=None, tokenise=True, lower=True):

        """
        This function returns a generator, to avoid storing massive
        amounts of text in RAM.  If text is None, the training text
        itself is segmented.  If tokenised is True, the sentences will
        be in tokenised form, i.e. with spaces inserted at token and
        subtoken boundaries, and digit strings replaced with special
        tokens.  If lowered is True, the strings will be lower-cased.
        """

        assert text is None or isinstance(text, unicode), text
        if text == None: text = self.text
        
        for line in (t for t in text.split('\n')):
            sentences = self.sbd.sentences_from_text(line, realign_boundaries=True)
            sentences = self.apply_ugly_hack_to_reattach_wrong_splits_in_certain_cases_with_initials(sentences)
            for sentence in sentences:
                if tokenise:
                    sentence = sentence_tokenise_and_regularise(sentence.split(), abbreviation_list=self.sbd._params.abbrev_types)
                if lower:
                    sentence = sentence.lower()
                yield sentence + '\n'

def run_me():
    
    st = NLTKBasedSegmenterTokeniser(sys.stdin)
    for tokenised_sentence in st.sentence_segment():
        sys.stdout.write(tokenised_sentence.encode('utf-8'))


if __name__ == '__main__':

    run_me()
