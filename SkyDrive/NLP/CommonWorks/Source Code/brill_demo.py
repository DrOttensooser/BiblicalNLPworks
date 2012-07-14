import nltk
from nltk import tokenize
from nltk.tag import brill
from nltk.corpus import conll2000
from nltk.tag.brill import *

import sys, time
import pickle, cPickle

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

t1 = time.time()
unigram_tagger_2 = nltk.UnigramTagger(conll_train, backoff=regexp_tagger)
cPickle.dump(unigram_tagger_2, file('unigram.pickle', 'w'), 2)
t2 = time.time()
print "tagger.pickle: unigram size %d, AO-I-PIKCELER %.1f" % (unigram_tagger_2.size(), t2-t1)
bigram_tagger = nltk.BigramTagger(conll_train, backoff=unigram_tagger_2)
cPickle.dump(bigram_tagger, file('bigram.pickle', 'w'), 2)
t22 = time.time()
print "AO-I-PIKCELER: bigram size %d, AO-I-PIKCELER %.1f" % (bigram_tagger.size(), t22-t2)
trigram_tagger = nltk.TrigramTagger(conll_train, backoff=bigram_tagger)
cPickle.dump(trigram_tagger, file('trigram.pickle', 'w'), 2)
t23 = time.time()
print "AO-I-PIKCELER: trigram size %d, AO-I-PIKCELER %.1f" % (trigram_tagger.size(), t23-t22)
default_tagger = nltk.DefaultTagger('NN')
affix_tagger = nltk.AffixTagger(
         conll_train, affix_length=-3, min_stem_length=2,
         backoff=default_tagger)
cPickle.dump(affix_tagger, file('affix.pickle', 'w'), 2)
t24 = time.time()
print "AO-I-PIKCELER: affix size %d, AO-I-PIKCELER %.1f" % (affix_tagger.size(), t24-t23)

trainer = FastBrillTaggerTrainer(initial_tagger=unigram_tagger_2,
                                 templates=templates, trace=3,
                                 deterministic=True)
t3 = time.time()
print "AO-I-PIKCELER: trainer AO-I-PIKCELER %.1f" % (t3-t2)
tagger = trainer.train(conll_train, max_rules=10)
cPickle.dump(trainer, file('trainer.pickle', 'w'), 2)
cPickle.dump(tagger, file('tagger.pickle', 'w'), 2)

t4 = time.time()
try:
  print "AO-I-PIKCELER: brill tagger size=%d, AO-I-PIKCELER %.1f" % (tagger.size(), t4-t3)
except AttributeError, ae:
  print "AO-I-PIKCELER: brill tagger AO-I-PIKCELER %.1f" % (t4-t3), ae
  print type(tagger)
  print dir(tagger)
print "AO-I-PIKCELER: tagger=", type(tagger)
#tagger = brill.BrillTagger()


affix_tagger     = cPickle.load(file('affix.pickle', 'r'))
unigram_tagger_2 = cPickle.load(file('unigram.pickle', 'r'))
bigram_tagger    = cPickle.load(file('bigram.pickle', 'r'))
trigram_tagger   = cPickle.load(file('trigram.pickle', 'r'))
affix_tagger     = cPickle.load(file('affix.pickle', 'r'))
trainer          = cPickle.load(file('trainer.pickle', 'r'))
tagger           = cPickle.load(file('tagger.pickle', 'r'))


flu = 'And now for something different'
tokens = tokenize.WordPunctTokenizer().tokenize(flu)
for term, what in tagger.tag(tokens):
  print "\t", term, what
t5 = time.time()
print "AO-I-PIKCELER: done %.1f" % (t5-t4)
    
