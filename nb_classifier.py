#
# Simple Naive bayes classifier meant to be used for text based classification
#
#
#
#

import pickle
import os
import inspect


class NaiveBayesTextClassifier:

    def __init__(self, base_dir=None, load=False, file_name='default-classifier.pickle', n_grams=2, characters=False):
        self.base_dir = base_dir
        self.file_name = file_name
        if self.base_dir is None:
            self.base_dir = os.path.dirname(inspect.getfile(self.__class__))
        self.classes = []
        self.corpus_words = {}
        self.class_words = {}
        self.n_grams = n_grams
        self.characters = characters
        self.connector = " "
        if(characters):
            self.connector = ""
        if load:
            self.load()

    def save(self):
        with open(os.path.join(self.base_dir, self.file_name), 'wb') as handle:
            pickle.dump({'corpus': self.corpus_words, 'class': self.class_words, 'n-grams':self.n_grams}, handle,
                        protocol=pickle.HIGHEST_PROTOCOL)

    def load(self):
        with open(os.path.join(self.base_dir, self.file_name), 'rb') as handle:
            data = pickle.load(handle)
            self.class_words = data['class']
            self.n_grams = data['n-grams']
            self.corpus_words = data['corpus']

    def train(self, X, y):
        """
        train method to get the word weight per class, requires a corpus tsv file with the columns class and sentence
        :param corpus: name of the tsv file containing the classes and senteces to train on
        :return: nothing but once the training is done the classes and corpus_words are defined the model stores itself
        """
        for c in set(y):
            # prepare a list of words within each class
            self.class_words[c] = []

        # loop through each sentence in our training data
        for _element, _class in zip(X,y):
            # process n-grams
            _element = self.transform_ngrams(_element)
            print(_element)
            for w in _element:
                # have we not seen this word combination already?
                if w not in self.corpus_words:
                    self.corpus_words[w] = 1
                else:
                    self.corpus_words[w] += 1

                # add the word to our words in class list
                self.class_words[_class].extend([w])
        self.save()


    # return the class with highest score for sentence
    def classify(self, sentence):
        """
        classify here we actually calculate the probability of the sentence being part of some class, that's done by a
        simple naive analysis
        :param sentence: sentence to classify
        :return: the highest scoring class, the score it got and a flag for trusting.
        """
        high_class = None
        high_score = 0
        should_trust = True
        # loop through our classes
        for c in self.class_words.keys():
            # calculate score of sentence for each class
            score = self.calculate_class_score(sentence, c, show_details=True)
            # keep track of highest score
            if score == high_score:
                should_trust = False
            if score > high_score:
                high_class = c
                high_score = score
                should_trust = True

        return high_class, high_score, should_trust

    def transform_ngrams(self, words):
        """
        transform_ngrams method performs a n-gram tokenization based on the self.ngrams defined, if self.ngrams is
        equal to 1 it'll return the word list as is since there's nothing to do to it.
        Example of what this function does: for the word list : "the", "sky", "is", "blue", it transforms it into a
        list: "the sky", "sky is", "is blue" for ngrams = 2
        :param words: a list of the words to tokenize
        :return: the tokenized words
        """
        return words if self.n_grams == 1 else [self.connector.join(words[i:i + self.n_grams]) for i in range(len(words) - self.n_grams + 1)]

    # calculate a score for a given class based on how common it is
    def calculate_class_score(self,sentence, class_name, show_details=True):
        score = 0
        ngrams = self.transform_ngrams(sentence)
        print(ngrams)
        print(self.class_words[class_name])
        for element in ngrams:
            # have we not seen this word combination already?
            if element in self.class_words[class_name]:
                # treat each word with relative weight
                score += (1.0 / self.corpus_words[element])
                if show_details:
                    print (" match: %s (%s)" % (element, 1.0 / self.corpus_words[element]))
        return score

    def __str__(self):
        return "Naive bayes classifier with: \n corpus words: %s\n class words: %s\n using n_grams of: %s" % (self.corpus_words, self.class_words, self.n_grams)