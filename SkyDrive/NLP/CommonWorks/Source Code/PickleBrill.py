'# -*- coding: utf-8 -*-'

'''
This module trains a Bril Tagger on the conll2000 tagged sentnces
and then pickled the trained tagger and stores it in the Tagger Path: 'Data\\Pickeled Taggers\\

A sister module unPickleBrill.py tests this module by unpickeling the trained Brill Tagger and tagging an imprtal phrase.

The module is based on http://code.google.com/p/tropo/source/browse/trunk/Python/tr_nltk/brill_demo.py
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
import os
import sys, time
import pickle

if not os.path.exists(AO_sTaggerPath):
        os.makedirs(AO_sTaggerPath)

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


unigram_tagger_2        = nltk.UnigramTagger(conll_train, backoff=regexp_tagger)
bigram_tagger           = nltk.BigramTagger(conll_train, backoff=unigram_tagger_2)
trigram_tagger          = nltk.TrigramTagger(conll_train, backoff=bigram_tagger)
default_tagger          = nltk.DefaultTagger('NN')
affix_tagger            = nltk.AffixTagger(conll_train, affix_length=-3, min_stem_length=2, backoff=default_tagger)
trainer                 = FastBrillTaggerTrainer(initial_tagger=unigram_tagger_2, templates=templates, trace=3, deterministic=True)
tagger                  = trainer.train(conll_train, max_rules=10)

AO_fpklOut2             = open(AO_sTaggerPath + 'affix.pickle'   , 'wb')
AO_fpklOut3             = open(AO_sTaggerPath + 'unigram.pickle' , 'wb')
AO_fpklOut4             = open(AO_sTaggerPath + 'bigram.pickle'  , 'wb')
AO_fpklOut5             = open(AO_sTaggerPath + 'trigram.pickle' , 'wb')
AO_fpklOut6             = open(AO_sTaggerPath + 'affix.pickle'   , 'wb')
AO_fpklOut7             = open(AO_sTaggerPath + 'trainer.pickle' , 'wb')
AO_fpklOut8             = open(AO_sTaggerPath + 'tagger.pickle'  , 'wb')

pickle.dump(affix_tagger,     AO_fpklOut2)
pickle.dump(unigram_tagger_2, AO_fpklOut3)
pickle.dump(bigram_tagger,    AO_fpklOut4)
pickle.dump(trigram_tagger,   AO_fpklOut5)
pickle.dump(affix_tagger,     AO_fpklOut6)
pickle.dump(trainer,          AO_fpklOut7)
pickle.dump(tagger,           AO_fpklOut8)

AO_fpklOut2.close()
AO_fpklOut3.close()   
AO_fpklOut4.close()
AO_fpklOut5.close()
AO_fpklOut6.close()
AO_fpklOut7.close()
AO_fpklOut8.close()

AO_fpklIn2              = open(AO_sTaggerPath + 'affix.pickle'   , 'r')
AO_fpklIn3              = open(AO_sTaggerPath + 'unigram.pickle' , 'r')
AO_fpklIn4              = open(AO_sTaggerPath + 'bigram.pickle'  , 'r')
AO_fpklIn5              = open(AO_sTaggerPath + 'trigram.pickle' , 'r')
AO_fpklIn6              = open(AO_sTaggerPath + 'affix.pickle'   , 'r')
AO_fpklIn7              = open(AO_sTaggerPath + 'trainer.pickle' , 'r')
AO_fpklIn8              = open(AO_sTaggerPath + 'tagger.pickle'  , 'r')

affix_tagger            = pickle.load(AO_fpklIn2)
unigram_tagger_2        = pickle.load(AO_fpklIn3)
bigram_tagger           = pickle.load(AO_fpklIn4)
trigram_tagger          = pickle.load(AO_fpklIn5)
affix_tagger            = pickle.load(AO_fpklIn6)
trainer                 = pickle.load(AO_fpklIn7)
tagger                  = pickle.load(AO_fpklIn8)

AO_fpklIn2.close()
AO_fpklIn3.close()   
AO_fpklIn4.close()
AO_fpklIn5.close()
AO_fpklIn6.close()
AO_fpklIn7.close()
AO_fpklIn8.close()

flu = 'And now for something different'
tokens = tokenize.WordPunctTokenizer().tokenize(flu)
for term, what in tagger.tag(tokens):
  print "\t", term, what
