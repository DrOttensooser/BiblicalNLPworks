import nltk.corpus, nltk.tag
from nltk.tag import brill
import itertools
 
conll_train = nltk.corpus.conll2000.tagged_sents()
 
def AO_fBackoffTagger(tagged_sents, tagger_classes, backoff=None):
    if not backoff:
        backoff = tagger_classes[0](tagged_sents)
        del tagger_classes[0]
 
    for cls in tagger_classes:
        tagger = cls(tagged_sents, backoff=backoff)
        backoff = tagger
 
    return backoff
 

AO_sWordPatterns = [
	(r'^-?[0-9]+(.[0-9]+)?$', 'CD'),
	(r'.*ould$', 'MD'),
	(r'.*ing$', 'VBG'),
	(r'.*ed$', 'VBD'),
	(r'.*ness$', 'NN'),
	(r'.*ment$', 'NN'),
	(r'.*ful$', 'JJ'),
	(r'.*ious$', 'JJ'),
	(r'.*ble$', 'JJ'),
	(r'.*ic$', 'JJ'),
	(r'.*ive$', 'JJ'),
	(r'.*ic$', 'JJ'),
	(r'.*est$', 'JJ'),
	(r'^a$', 'PREP'),
]

AO_fRAUBTtagger = AO_fBackoffTagger(conll_train, [nltk.tag.AffixTagger, nltk.tag.UnigramTagger, nltk.tag.BigramTagger, nltk.tag.TrigramTagger],
    backoff=nltk.tag.RegexpTagger(AO_sWordPatterns))

templates = [
    brill.SymmetricProximateTokensTemplate(brill.ProximateTagsRule, (1,1)),
    brill.SymmetricProximateTokensTemplate(brill.ProximateTagsRule, (2,2)),
    brill.SymmetricProximateTokensTemplate(brill.ProximateTagsRule, (1,2)),
    brill.SymmetricProximateTokensTemplate(brill.ProximateTagsRule, (1,3)),
    brill.SymmetricProximateTokensTemplate(brill.ProximateWordsRule, (1,1)),
    brill.SymmetricProximateTokensTemplate(brill.ProximateWordsRule, (2,2)),
    brill.SymmetricProximateTokensTemplate(brill.ProximateWordsRule, (1,2)),
    brill.SymmetricProximateTokensTemplate(brill.ProximateWordsRule, (1,3)),
    brill.ProximateTokensTemplate(brill.ProximateTagsRule, (-1, -1), (1,1)),
    brill.ProximateTokensTemplate(brill.ProximateWordsRule, (-1, -1), (1,1))
]

trainer = brill.FastBrillTaggerTrainer(AO_fRAUBTtagger, templates)

brill_tagger = trainer.train(conll_train, max_rules=100, min_score=3)


print "AO-I-BRLTND Brill tagger trained on conll2000 corpora."
