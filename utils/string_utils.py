#
# Set of utility functions helpful for sentence processing and cleaning
# stopwords obtained from NLTK (https://github.com/nltk/nltk/blob/develop/LICENSE.txt)
# Contractions gotten from https://en.wikipedia.org/wiki/Wikipedia:List_of_English_contractions
#


import string
import re
from difflib import SequenceMatcher


_CONTRACTIONS_DICT = {
    "ain't": "am not",
    "aren't": "are not",
    "can't": "cannot",
    "can't've": "cannot have",
    "'cause": "because",
    "could've": "could have",
    "couldn't": "could not",
    "daren't": "dare not",
    "didn't": "did not",
    "doesn't": "does not",
    "don't": "do not",
    "everyone's": "everyone is",
    "gimme":"give me",
    "gonna":"going to",
    "gotta":"got to",
    "hadn't": "had not",
    "hasn't": "has not",
    "haven't": "have not",
    "he'd": "he would",
    "he'll": "he will",
    "he's": "he is",
    "how'd": "how did",
    "how'll": "how will",
    "how's": "how is",
    "I'd": "I would",
    "I'd've": "I would have",
    "I'll": "I will",
    "I'm": "I am",
    "i'm": "i am",
    "I've": "I have",
    "isn't": "is not",
    "it'd": "it had",
    "it'll": "it will",
    "it's": "it is",
    "let's": "let us",
    "ma'am": "madam",
    "mayn't": "may not",
    "might've": "might have",
    "must've": "must have",
    "mustn't": "must not",
    "mustn't've": "must not have",
    "needn't": "need not",
    "needn't've": "need not have",
    "ne'er":"never",
    "o'clock":"of the clock",
    "ol'":"old",
    "oughtn't": "ought not",
    "oughtn't've": "ought not have",
    "she'd": "she would",
    "she'd've": "she would have",
    "she'll": "she will",
    "she'll've": "she will have",
    "she's": "she is",
    "shouldn't": "should not",
    "so've": "so have",
    "so's": "so is",
    "that'd": "that would",
    "that's": "that is",
    "that'll": "that will",
    "there'd": "there had",
    "there's": "there is",
    "they'd": "they would",
    "they'll": "they will",
    "they're": "they are",
    "they've": "they have",
    "to've": "to have",
    "wasn't": "was not",
    "we'd": "we had",
    "we'll": "we will",
    "we're": "we are",
    "we've": "we have",
    "weren't": "were not",
    "what'll": "what will",
    "what're": "what are",
    "what's": "what is",
    "what've": "what have",
    "when's": "when is",
    "when've": "when have",
    "where'd": "where did",
    "where's": "where is",
    "where've": "where have",
    "who'll": "who will",
    "who's": "who is",
    "who've": "who have",
    "why's": "why is",
    "why've": "why have",
    "will've": "will have",
    "won't": "will not",
    "would've": "would have",
    "wouldn't": "would not",
    "you'll": "you will",
    "you're": "you are",
    "you've": "you have",
    "'tis":"it is"
}

_CONTRACTIONS_REGEX = re.compile(r'('+'|'.join(_CONTRACTIONS_DICT.keys())+')')
_ENGLISH_STOPWORDS = ['i', 'me', 'my', 'myself', 'we', 'our', 'ours', 'ourselves', 'you', "you're", "you've",
                      "you'll", "you'd", 'your', 'yours', 'yourself', 'yourselves', 'he', 'him', 'his', 'himself',
                      'she', "she's", 'her', 'hers', 'herself', 'it', "it's", 'its', 'itself', 'they', 'them',
                      'their', 'theirs', 'themselves', 'what', 'which', 'who', 'whom', 'this', 'that', "that'll",
                      'these', 'those', 'am', 'is', 'are', 'was', 'were', 'be', 'been', 'being', 'have', 'has',
                      'had', 'having', 'do', 'does', 'did', 'doing', 'a', 'an', 'the', 'and', 'but', 'if', 'or',
                      'because', 'as', 'until', 'while', 'of', 'at', 'by', 'for', 'with', 'about', 'against',
                      'between', 'into', 'through', 'during', 'before', 'after', 'above', 'below', 'to', 'from',
                      'up', 'down', 'in', 'out', 'on', 'off', 'over', 'under', 'again', 'further', 'then', 'once',
                      'here', 'there', 'when', 'where', 'why', 'how', 'all', 'any', 'both', 'each', 'few', 'more',
                      'most', 'other', 'some', 'such', 'no', 'nor', 'not', 'only', 'own', 'same', 'so', 'than', 'too',
                      'very', 's', 't', 'can', 'will', 'just', 'don', "don't", 'should', "should've", 'now', 'd', 'll',
                      'm', 'o', 're', 've', 'y', 'ain', 'aren', "aren't", 'couldn', "couldn't", 'didn', "didn't",
                      'doesn', "doesn't", 'hadn', "hadn't", 'hasn', "hasn't", 'haven', "haven't", 'isn', "isn't",
                      'ma', 'mightn', "mightn't", 'mustn', "mustn't", 'needn', "needn't", 'shan', "shan't", 'shouldn',
                      "shouldn't", 'wasn', "wasn't", 'weren', "weren't", 'won', "won't", 'wouldn', "wouldn't"]


_STOPWORDS_REGEX = re.compile(r'(?:^|(?<= ))('+'|'.join(_ENGLISH_STOPWORDS)+')(?:(?= )|$)')


def _contractions_replace(match):
    """
    Helper internal method used to easily replace the specified contraction with the match
    """
    return _CONTRACTIONS_DICT[match.group(0)]


def expand_contractions(text, regex=_CONTRACTIONS_REGEX):
    """
    Expands contractions found in text
    :param text: the text string to which we'll expand the contractions inside itself
    :param regex: regex to use to find the contractions, should be left to default most of the time
    :return: the text with the contractions expanded
    """
    return regex.sub(_contractions_replace, text)


def remove_stopwords(text, regex=_STOPWORDS_REGEX):
    """
    Removes the stopwords found in the text
    :param text: the text string that we'll be removing the stopwords from
    :param regex: regex to be used to find the stopwords in the text, should be left to default unless you want to use
        another set of stopwords
    :return: the text without the stopwords
    """
    return regex.sub('',text)


def strip_punc(s, all=False):
    """
    Removes punctuation from a string.
    :param s: The string.
    :param all: Remove all punctuation. If False, only removes punctuation from
        the ends of the string.
    """
    if all:
        return re.compile('[{0}]'.format(re.escape(string.punctuation))).sub('', s.strip())
    else:
        return s.strip().strip(string.punctuation)


def calculate_string_distance(first, final):
    """
    Calculates the string "distance"
    :param first: first string to check
    :param final: second string to check
    :return: The ratio found by the SequenceMatcher
    """
    return SequenceMatcher(None, first.lower(), final.lower()).ratio()


def normalize(line, accepted_chars='abcdefghijklmnopqrstuvwxyz '):
    """
    Return only the subset of chars from accepted_chars.
    This helps keep the  model relatively small by ignoring punctuation, 
    infrequenty symbols, etc.
    """
    return [c.lower() for c in line if c.lower() in accepted_chars]


def ngram(n, l):
    """ Return all n grams from l after normalizing """
    filtered = normalize(l)
    for start in range(0, len(filtered) - n + 1):
        yield ''.join(filtered[start:start + n])


def pre_process_sentence( sentence):
    """
    pre_process_sentence expands contractions on a sentence and changes the symbol ? so it can be specially processed
    :param sentence: the sentence to pre-process
    :return: the sentence with the modifications
    """
    # expand the contractions
    expanded_sentence = expand_contractions(sentence.lower())
    # remove punctuation
    return strip_punc(expanded_sentence)


