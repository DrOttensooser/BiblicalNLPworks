'# -*- coding: utf-8 -*-'

'# -*- coding: utf-8 -*-'

'''
This code section unpickels a trained Brill Tagger and then taggs an imortal sentence.

A priviously executed sister module PickleBrill.py trains a Brill Tagger on the conll2000 tagged sentnces
and then pickled the trained tagger and stores it in the Tagger Path: 'Data\\Pickeled Taggers\\

The code is based on http://code.google.com/p/tropo/source/browse/trunk/Python/tr_nltk/brill_demo.py
'''


__author__ = 'Dr Avner OTTENSOOSER <avner.ottensooser@gmail.com>'
__version__ = '$Revision: 0.01 $'

AO_ROOT_PATH         =  'C:\\Users\\Avner\\SkyDrive\\NLP\\'
AO_sCommonPath       =  AO_ROOT_PATH   + 'CommonWorks\\'
AO_sTaggerPath        =  AO_sCommonPath + 'Data\\Pickeled Taggers\\'

import nltk
from nltk import tokenize
from nltk.tag import brill
from nltk.corpus import conll2000
from nltk.tag.brill import *
import sys, time
import pickle

AO_fpklIn2       = open(AO_sTaggerPath + 'affix.pickle'   , 'r')
AO_fpklIn3       = open(AO_sTaggerPath + 'unigram.pickle' , 'r')
AO_fpklIn4       = open(AO_sTaggerPath + 'bigram.pickle'  , 'r')
AO_fpklIn5       = open(AO_sTaggerPath + 'trigram.pickle' , 'r')
AO_fpklIn6       = open(AO_sTaggerPath + 'affix.pickle'   , 'r')
AO_fpklIn7       = open(AO_sTaggerPath + 'trainer.pickle' , 'r')
AO_fpklIn8       = open(AO_sTaggerPath + 'tagger.pickle'  , 'r')

affix_tagger     = pickle.load(AO_fpklIn2)
unigram_tagger_2 = pickle.load(AO_fpklIn3)
bigram_tagger    = pickle.load(AO_fpklIn4)
trigram_tagger   = pickle.load(AO_fpklIn5)
affix_tagger     = pickle.load(AO_fpklIn6)
trainer          = pickle.load(AO_fpklIn7)
tagger           = pickle.load(AO_fpklIn8)

AO_fpklIn2.close()
AO_fpklIn3.close()   
AO_fpklIn4.close()
AO_fpklIn5.close()
AO_fpklIn6.close()
AO_fpklIn7.close()
AO_fpklIn8.close()

# see nltk-0.9.5/nltk/test/tag.doctest

conll_train = nltk.corpus.conll2000.tagged_sents()

regexp_tagger = nltk.RegexpTagger(
    [(r'^-?[0-9]+(.[0-9]+)?$', 'CD'),   # cardinal numbers
     (r'(The|the|A|a|An|an)$', 'AT'),   # articles
     (r'.*able$', 'JJ'),                # adjectives
     (r'.*ness$', 'NN'),                # nouns formed from adjectives
     (r'.*ly$', 'RB'),                  # adverbs
     (r'.*s$', 'NNS'),                  # plural nouns
     (r'.*ing$', 'VBG'),                # gerunds
     (r'.*ed$', 'VBD'),                 # past tense verbs
     (r'.*', 'NN')                      # nouns (default)
])

templates = [
    SymmetricProximateTokensTemplate(ProximateTagsRule, (1,1)),
    SymmetricProximateTokensTemplate(ProximateTagsRule, (2,2)),
    SymmetricProximateTokensTemplate(ProximateTagsRule, (1,2)),
    SymmetricProximateTokensTemplate(ProximateTagsRule, (1,3)),
    SymmetricProximateTokensTemplate(ProximateWordsRule, (1,1)),
    SymmetricProximateTokensTemplate(ProximateWordsRule, (2,2)),
    SymmetricProximateTokensTemplate(ProximateWordsRule, (1,2)),
    SymmetricProximateTokensTemplate(ProximateWordsRule, (1,3)),
    ProximateTokensTemplate(ProximateTagsRule, (-1, -1), (1,1)),
    ProximateTokensTemplate(ProximateWordsRule, (-1, -1), (1,1)),
    ]

default_tagger = nltk.DefaultTagger('NN')

flu = 'And now for something different'
tokens = tokenize.WordPunctTokenizer().tokenize(flu)
for term, what in tagger.tag(tokens):
  print "\t", term, what
    
