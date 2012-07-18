'# -*- coding: utf-8 -*-'
from __future__ import division
'''
This module ranks a documents author's opinions by looking for key words
compiled by Minqing Hu and Bing Liu http://www.cs.uic.edu/~liub/FBS/sentiment-analysis.html
and by Taboada et al (lexicon-Base dMethods for Sentiment Analysis). 

'''
__author__ = 'Dr Avner OTTENSOOSER <avner.ottensooser@gmail.com>'
__version__ = '$Revision: 1 $'

AO_ROOT_PATH                = 'C:\\Users\\Avner\\SkyDrive\\NLP\\'
AO_sCommonPath              =  AO_ROOT_PATH   + 'CommonWorks\\'
AO_sCommonCode              =  AO_sCommonPath + 'Source Code'
AO_sSOcalPath               =  AO_sCommonPath + 'Data\\Opion-Lexicon-English\\SO-CAL\\'
AO_sSOcalPickeleFileName    =  AO_sSOcalPath  + 'SO-CAL Lexicon.PKL'
AO_sTaggerPath              =  AO_sCommonPath + 'Data\\Pickeled Taggers\\'
AO_bBeGriddy                =  True

import re
#import AO_mShakespeareWorksCommon
import pickle
import nltk
from nltk import sent_tokenize
from nltk import word_tokenize
import nltk.tag
from nltk import SnowballStemmer
stemmer = SnowballStemmer("english")
import sys
sys.path.append(AO_sCommonCode)

# *****************************
# Load the trained Brill Tagger
# *****************************

'''
This code section unpickels a trained Brill Tagger.

A priviously executed sister module PickleBrill.py trained a Brill Tagger on the conll2000 tagged sentnces
and then pickled the trained tagger and stores it in the Tagger Path: 'Data\\Pickeled Taggers\\

The section is based on http://code.google.com/p/tropo/source/browse/trunk/Python/tr_nltk/brill_demo.py
'''

from nltk import tokenize
from nltk.tag import brill
from nltk.corpus import conll2000
from nltk.tag.brill import *
import pickle

# These files contain the pickled trained taggres
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

# the brill tagger
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

# the less sufisticated refular exprsion tagger
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


# the defual tagger that should never be called
default_tagger = nltk.DefaultTagger('NN')

# **************************************************************
# print "AO-S-BRLTND Brill tagger trained on conll2000 corpora."
# **************************************************************

# the brown POS list from http://en.wikipedia.org/wiki/Brown_Corpus 
AO_setNoun          = set(['NN','BB$','NNP','NNP$','NP','NP$','NPS$','NR','N'])
AO_setAdjective     = set(['JJ','JJR','JJS','JJT','ADJ'])
AO_setVerb          = set(['VB','VBD','VBG','VBN','VBZ'])
AO_setAdverb        = set(['RB','RBR','RBT','RN','RP','ADV'])
AO_setNegationWords = set(["not","none","dosn't","nobody","never","nothing","without","lack","haven't","hadn't","don't","isn't","aren't'"])

# load the SO-CAL and Minqing Hu lexicons craeted by the PickelSO_CAL programme
AO_fPickle  = open(AO_sSOcalPickeleFileName, 'rb')
AO_dLexicon = pickle.load(AO_fPickle)
AO_fPickle.close
print str(len(AO_dLexicon)) + " SO-CAL and Minqing Hu terms were unpickeled from: " + AO_sSOcalPickeleFileName + ' .'

def AO_fAssessWord(AO_sWord, AO_lTypes):

    # lockup a string in the SO-CAL lexicon using a hash of the word type and the word and 
    # GIVE the SO-CAl rating between -5 and +5

    _fAssessWord = float(0)
    AO_bEcodingSucceeded = True
    try:
        AO_sCurrentWord = AO_sWord[0].encode('ascii','ignore')
    except: # This exception can raise if the string is glibrige
        AO_bEcodingSucceeded = False

    # if this is not giblige
    if AO_bEcodingSucceeded:
        AO_sCurrentWord = AO_sCurrentWord.lower()
       
        # we first evalute intensifiers regardless of their part of speach tags
        if (AO_lTypes[0] == 'int'):
            AO_sCompundKey = 'int'+AO_sCurrentWord
            _fAssessWord = AO_dLexicon.get(AO_sCompundKey,float(0))

        else:  #['adj','adv','noun','verb']
            
            # the SO-CAL lexicon has a simplified clasification
            if AO_sWord[1] in  AO_setNoun:
                AO_sFirstCandidate = 'noun'
            elif AO_sWord[1] in AO_setVerb:
                AO_sFirstCandidate = 'verb'
            elif AO_sWord[1] in AO_setAdjective:
                AO_sFirstCandidate = 'adj'
            elif AO_sWord[1] in AO_setAdverb:
                AO_sFirstCandidate = 'adv'  
                
            # try 1 - MSO-Cal  lexicon
            AO_sCompundKey = AO_sFirstCandidate+AO_sCurrentWord
            _fAssessWord = AO_dLexicon.get(AO_sCompundKey,float(0))

            if AO_bBeGriddy:
                # try 2 - Minqing Hu lexicon
                # if the word is not fount in the SO-CAL lexicon, fall back to the Minqing Hu lexicon
                if (_fAssessWord == float(0)):
                    AO_sCompundKey = 'minqinghu' + AO_sCurrentWord
                    _fAssessWord = AO_dLexicon.get(AO_sCompundKey,float(0))  
                    
                # tries 3 - recursive stem
                # if reslt not found yet fall back to the stem and call the function recursivly ...
                if (_fAssessWord == float(0)):
                    AO_sStemmed = str(stemmer.stem(AO_sCurrentWord))
                    if (AO_sStemmed <> AO_sCurrentWord):
                        AO_sWord = (AO_sStemmed,AO_sWord[1]) #'tuple' object does not support item assignment
                        AO_fAssessWord(AO_sWord, AO_lTypes)
                    # ehile we can further stem the word
                # end if not found  un stemmed
            #endif griddy search  
        # endif - the word was not an intencifier
    # endif the word is not gilbrige

    return _fAssessWord

    

def AO_lAssessOpinion (AO_sDocument,AO_sDocumentName,AO_sDocumentsType):
    '''
    This function
    Input   - A document
    Process - Lookup of all the words in the document within the positive and negative word lists
    Output  - An array with Percent Pocitive Words
                            Percent Negative Words
                            Some of the above
                            Simmery line with the above percents and tagged list of all the opionion words in teh documents 
       
    '''


    
    AO_lOpinion=[0,0,"","",""]
    AO_fPosWords = 0
    AO_fNegWords = 0
    AO_sLine = ""
     
    # Break the document into sentences
    AO_lSentences = sent_tokenize(AO_sDocument)
    
    # For all the sentences in the document
    for i in range (0, len(AO_lSentences)):
        # AO_lTokens = pos_tag(word_tokenize(AO_lSentences[i])) # this easy to call tagger was deemed too slow
        
        # Call the brill tagger to identify POS
        # AO_lTokens = tokenize.WordPunctTokenizer().tokenize(AO_lSentences[i])
        tokens = tokenize.WordPunctTokenizer().tokenize(AO_lSentences[i])
        AO_lTokens = tagger.tag(tokens)
        AO_bNegationFound = False
        
        # for all the individual words in the sentece
        for j in range(0, len(AO_lTokens)):
            
            AO_fWordSentiment =0
            
            # is this a negation word?
            if str(AO_lTokens[j][0]) in AO_setNegationWords:
                AO_bNegationFound = not AO_bNegationFound
            
            # if this is an internsifier, we will deal with it with next word
            if (AO_fAssessWord(AO_lTokens[j],['int']) <> float(0)):

                AO_fWordSentiment = AO_fAssessWord(AO_lTokens[j],['adj','adv','noun','verb','minqinghu'])
                
                # if the word is a positive word
                if AO_fWordSentiment > 0:
                    AO_bNegationFound  = False # the word was not found to be negated, yet
                    AO_bEmphasiseFound = False # the word was not found to be emphasised yet
                    
                    # see if the privious word negated the j word
                    if j > 0: # is these is a privious word at all
                        
                        # now we see if the privious word is intensifier
                        AO_fIntencity = AO_fAssessWord(AO_lTokens[j-1],['int'])
                                        
                        # now we check for "Not good". Note that the negation word may have a space so unimpresive will also be caught
                        if (AO_fIntencity < 0):
                            
                            # (Taboada et al. Lexicon-Based Methods for Sentiment Analysis p275)
                            AO_fSentiment = AO_fWordSentiment* (1+AO_fIntencity)
                            AO_fNegWords = AO_fNegWords +  AO_fSentiment  
                            AO_sLine = AO_sLine + 'notP((1+'+str(AO_fIntencity)+ ')*('+'('+str(AO_fWordSentiment )+')=('+str(AO_fSentiment)+')): ' + str(AO_lTokens[j-1][0]) +' ' + str(AO_lTokens[j][0])+  ' , ' + str(AO_lTokens[j-1][1]) +' ' + str(AO_lTokens[j][1])+ ' ~ '
                            AO_bNegationFound = True
                        #endif word was negated                        
                              
                        # now we check for "Very good". Note that the negation word may have a space so unimpresive will also be caught
                        if (AO_fIntencity > 0):
                            AO_fSentiment = AO_fWordSentiment* (1+AO_fIntencity)
                            AO_fPosWords = AO_fPosWords + AO_fSentiment # double the scoring
                            AO_sLine = AO_sLine + 'emphP((1+'+str(AO_fIntencity)+ ')*(' + str(AO_fWordSentiment )+')=('+str(AO_fSentiment)+')): ' + str(AO_lTokens[j-1][0]) +' ' + str(AO_lTokens[j][0])+  ' , ' + str(AO_lTokens[j-1][1]) +' ' + str(AO_lTokens[j][1])+ ' ~ '
                            AO_bEmphasiseFound = True
                        # endif word was emphasied
                            
                    # end for all the possible emphasise words
                    
                    # if the positve word was not negated
                    
                    if (AO_bNegationFound == False)  and (AO_bEmphasiseFound == False) and (AO_fAssessWord(AO_lTokens[j],['int']) <> 0):
                        AO_fPosWords = AO_fPosWords + AO_fWordSentiment
                        AO_sLine = AO_sLine + 'P (' +str(AO_fWordSentiment)+ '): ' + str(AO_lTokens[j][0]) +' ' + str(str(AO_lTokens[j][1])) + ' ~ '
                        
                     # endif - word was not emphasised or negated
                                
                # endif positive  word
                
                # if the word is a negative words
                if AO_fWordSentiment < 0:
                    
                    # now we chceck word pairs, starting ofcourse with the second word
                    AO_bNegationFound   = False # the word was not found to be negated, yet
                    AO_bEmphasiseFound = False # the word was not found to be emphasised yet
                    if j > 0:
                        
                        # now we try all the negation words

                        AO_fIntencity = AO_fAssessWord(AO_lTokens[j-1],['int'])
                            
                        # now we check for "Not bad". Note that the negation word may have a space so unexpiring will also be caught
                        if (AO_fIntencity < 0):
                            AO_fSentiment = AO_fWordSentiment* (1+AO_fIntencity)
                            AO_fPosWords = AO_fPosWords + AO_fSentiment # not bad is positive
                            
                            AO_sLine = AO_sLine + 'notN((1+'+str(AO_fIntencity)+')*('+str(AO_fWordSentiment )+')=('+str(AO_fSentiment)+')): ' + str(AO_lTokens[j-1][0]) +' ' + str(AO_lTokens[j][0])+  ' , ' + str(AO_lTokens[j-1][1]) +' ' + str(AO_lTokens[j][1])+ ' ~ '
                            
                            AO_bNegationFound = True
                        #endif word was negated
                            
                        # now we try all the emphasise words
                        # now we check for "Very good". Note that the negation word may have a space so unimpresive will also be caught
                        if (AO_fIntencity > 0):
                            AO_fSentiment = AO_fWordSentiment* (1+AO_fIntencity)
                            AO_fNegWords = AO_fNegWords + AO_fSentiment  # double the scoring
                            AO_sLine = AO_sLine + 'emphN((1+'+str(AO_fIntencity) +')*('+str(AO_fWordSentiment )+')=('+str(AO_fSentiment)+')): ' + str(AO_lTokens[j-1][0]) +' ' + str(AO_lTokens[j][0])+  ' , ' + str(AO_lTokens[j-1][1]) +',' + str(AO_lTokens[j][1])+ ' ~ '
                            AO_bEmphasiseFound = True
                        # end if word was emphasied
                            
                            
                    # if the negative word was not negated    
                    if (AO_bNegationFound == False) and (AO_bEmphasiseFound == False) and (AO_fAssessWord(AO_lTokens[j],['int']) <> 0):
                        AO_fNegWords = AO_fNegWords + AO_fWordSentiment
                        AO_sLine = AO_sLine + 'N('+str(AO_fWordSentiment)+'): ' + str(AO_lTokens[j][0]) +',' + str(AO_lTokens[j][1]) +' ~ '
                    
                    # endif - word was not emphasised or negated
                
                # endif negarive word
            # endif this is an intensifier    
        # for all the words in the sentence
    #for all the sentences in the document
    
    if len(AO_lTokens) > 0:
        
        a =  AO_fPosWords 
        b =  AO_fNegWords 
        c =  a+ b
        
        AO_lOpinion=[a,b,c,AO_sLine]
                     
    return AO_lOpinion 
    
# end of function
