

import time
import csv
import inspect
import os

from morphy import Morphy
from pos_tagger import PerceptronTagger
from utils import string_utils as su
from nb_classifier import NaiveBayesTextClassifier


def command_interface():
    print('NB classifier interactive tester\n---------')
    print('Welcome to the NB classifier tester. ')
    print('This is for testing and debugging the classifier performance')
    train = True
    s = 'hello'
    continue_chat = True

    start = time.time()
    classifier = NaiveBayesTextClassifier()
    with open("test.tsv") as tsvfile:
        reader = csv.DictReader(tsvfile, dialect='excel-tab')
        training_data = list(reader)
    sentences = list()
    classes = list()
    for data in training_data:
        print(data)
        sentences.append(su.pre_process_sentence(data['sentence']).split())
        classes.append(data['class'])
    classifier.train(sentences,classes)
    end = time.time()

    print("training finished in:")
    print(end - start)
    morphy = Morphy(base_dir=os.path.dirname(inspect.getfile(classifier.__class__)))
    pos_tagger = PerceptronTagger(base_dir=os.path.dirname(inspect.getfile(classifier.__class__)))
    print('=' * 20)
    print(classifier)
    print("Please input a sentence to be classified or type `quit' to finish the tests")
    try:
        s = raw_input('> ')
    except EOFError:
        continue_chat = False
    while continue_chat:
        print(s)
        print(pos_tagger.tag(s))
        print(morphy.change_to_base(pos_tagger.tag(s)))
        print(su.remove_stopwords(s.lower()))
        s = su.pre_process_sentence(s).split()
        c, s, t = classifier.classify(s)
        print(c)
        print(s)
        print(t)
        if True:
            try:
                s = raw_input('> ')
            except EOFError:
                s = 'quit'
            if s == 'quit':
                return



if __name__ == "__main__":
    command_interface()
