'# -*- coding: utf-8 -*-'
from __future__ import division
'''
This module ranks a documents author's opinions by looking for key words
compiled by Minqing Hu and Bing Liu http://www.cs.uic.edu/~liub/FBS/sentiment-analysis.html
'''
__author__ = 'Dr Avner OTTENSOOSER <avner.ottensooser@gmail.com>'
__version__ = '$Revision: 1 $'

AO_ROOT_PATH                = 'C:\\Users\\Avner\\SkyDrive\\NLP\\'
AO_sCommonPath              =  AO_ROOT_PATH   + 'CommonWorks\\'
AO_sSOcalPath               =  AO_sCommonPath + 'Data\\Opion-Lexicon-English\\SO-CAL\\'
AO_sSOcalPickeleFileName    =  AO_sSOcalPath  + 'SO-CAL Lexicon.PKL'

import re
import AO_mShakespeareWorksCommon
import pickle
import nltk
from nltk import sent_tokenize
AO_fStemmer = nltk.PorterStemmer() # This will make chaning the stemmer easier

# TODO Add stanford sentence tokeniser support
# from nltk import sent_tokenize, regexp_tokenize
# from nltk.tag.stanford import StanfordTagger
# st = stanford.StanfordTagger('bidirection-distsim-wsj-0-18.tagger')

#Load a cascading tagger

# Most NLTK taggers permit a backoff tagger to be specified. The backoff tagger may itself have a backoff tagger.

from nltk import pos_tag, word_tokenize


t0 = nltk.DefaultTagger('NN')

from nltk.corpus import brown
AOL_lTrainingSentences = brown.tagged_sents(categories='news')[:5000]

from nltk.tag import UnigramTagger
t1 = nltk.UnigramTagger(AOL_lTrainingSentences, backoff = t0)
AO_fTagger = nltk.BigramTagger(AOL_lTrainingSentences, backoff = t1)



# load the SO-CAL lexicon craeted by the PickelSO_CAL programme
AO_fPickle  = open(AO_sSOcalPickeleFileName, 'rb')
AO_dLexicon = pickle.load(AO_fPickle)
AO_fPickle.close

print str(len(AO_dLexicon)) + " SO-CAL and Minqing Hu terms were unpickeled from: " + AO_sSOcalPickeleFileName + ' .'

def AO_fAssessWord(AO_sWord, AO_lTypes):

    # lockup a string in the SO-CAL lexicon using a hash of the word type and the word and GIVE the SO-CAl rating between -5 and +5

    _fAssessWord = float(0)

   
    # we first evalute intensifiers regardless of their part of speach tags
    if (AO_lTypes == 'int'):
        AO_sCompundKey = AO_lTypes[i]+AO_sWord[0]
        _fAssessWord = AO_dLexicon.get(AO_sCompundKey,float(0))

    else:  #['adj','adv','noun','verb']

        AO_sFirstCandidate = 'None'
        if AO_sWord[1] == 'NN':
            AO_sFirstCandidate = 'noun'
        elif AO_sWord[1] == 'NNP':
            AO_sFirstCandidate = 'noun'
        elif AO_sWord[1] == 'VBP':
            AO_sFirstCandidate = 'verb'
        elif AO_sWord[1] == 'JJ':
            AO_sFirstCandidate = 'adj'
        elif AO_sWord[1] == 'RB':
            AO_sFirstCandidate = 'adv'  
            
        if (AO_sFirstCandidate <> 'None'):
            AO_sCompundKey = AO_sFirstCandidate+AO_sWord[0]
            _fAssessWord = AO_dLexicon.get(AO_sCompundKey,float(0))
        
        # this is while (_fAssessWord <> float(0)) loop
        for i in range (0, len(AO_lTypes)):
            if _fAssessWord <> float(0):    
                break
            AO_sCompundKey = AO_lTypes[i]+AO_sWord[0]
            _fAssessWord = AO_dLexicon.get(AO_sCompundKey,float(0))
        
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
    
    # we only work with lower case
    

    
    # Breake the document into sentences
    AO_lSentences = sent_tokenize(AO_sDocument)
    for i in range (0, len(AO_lSentences)):
        AO_lTokens = pos_tag(word_tokenize(AO_lSentences[i]))
        # AO_lTags = AO_fTagger.tag(AO_lSentences[i])
        # for all the individual words in the document
        for j in range(0, len(AO_lTokens)):

            # if this is an internsifier, we will deal with it with next word
            if (AO_fAssessWord(AO_lTokens[j],['int']) <> float(0)):

                AO_fWordSentiment = AO_fAssessWord(AO_lTokens[j],['adj','adv','noun','verb','minqinghu'])

                # if the word was not found give us a second shot at the stem
                if AO_fWordSentiment == 0:
                    AO_fWordSentiment = AO_fAssessWord(AO_lTokens[j],['adj','adv','noun','verb','minqinghu'])
                    
                # if the word is a positive word
                if AO_fWordSentiment > 0:
                    AO_bNegationFound  = False # the word was not found to be negated, yet
                    AO_bEmphasiseFound = False # the word was not found to be emphasised yet
                    
                    # see if the privious word negated the j word
                    if j > 0: # is these is a privious word at all
                        
                        # now we see if the privious word id intensifier

                        AO_fIntencity = AO_fAssessWord(AO_lTokens[j-1],['int'])
                                        
                        # now we check for "Not good". Note that the negation word may have a space so unimpresive will also be caught
                        if (AO_fIntencity < 0):
                            AO_fNegWords = AO_fNegWords + AO_fIntencity*AO_fWordSentiment  # a negation of a positive word is negative
                            AO_sLine = AO_sLine + 'notP('+str(AO_fIntencity )+'*'+str(AO_fWordSentiment)+ '): ' + AO_lTokens[j-1][0] +',' + AO_lTokens[j-1][1]+  ' ' + AO_lTokens[j][0] +',' + AO_lTokens[j][1]+ ' ~ '
                            AO_bNegationFound = True
                        #endif word was negated
                            
                            
                        # now we try all the emphasise words
                            
                        # now we check for "Very good". Note that the negation word may have a space so unimpresive will also be caught
                        if (AO_fIntencity > 0):
                            AO_fPosWords = AO_fPosWords + AO_fIntencity*AO_fWordSentiment # double the scoring
                            AO_sLine = AO_sLine + 'emphP('+str(AO_fIntencity )+'*'+str(AO_fWordSentiment)+  '): ' + AO_lTokens[j-1][0] +',' + AO_lTokens[j-1][1]+  ' ' + AO_lTokens[j][0] +',' + AO_lTokens[j][1]+ ' ~ '
                            AO_bEmphasiseFound = True
                        # endif word was emphasied
                            
                    # end for all the possible emphasise words
                    
                    # if the positve word was not negated
                    
                    if (AO_bNegationFound == False)  and (AO_bEmphasiseFound == False) and (AO_fAssessWord(AO_lTokens[j],['int']) <> 0):
                        AO_fPosWords = AO_fPosWords + AO_fWordSentiment
                        AO_sLine = AO_sLine + 'P (' +str(AO_fWordSentiment)+ '): ' + AO_lTokens[j][0] +',' + AO_lTokens[j][1]+ ' ~ '
                        
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
                            AO_fPosWords = AO_fPosWords + AO_fWordSentiment*AO_fIntencity  # not bad is positive
                            AO_sLine = AO_sLine + 'notN('+str(AO_fIntencity )+'*'+str(AO_fWordSentiment)+'): ' + AO_lTokens[j-1][0] +',' + AO_lTokens[j-1][1]+  ' ' + AO_lTokens[j][0] +',' + AO_lTokens[j][1]+ ' ~ '
                            AO_bNegationFound = True
                        #endif word was negated
                            
                        # now we try all the emphasise words
                        # now we check for "Very good". Note that the negation word may have a space so unimpresive will also be caught
                        if (AO_fIntencity > 0):
                            AO_fNegWords = AO_fNegWords + AO_fIntencity*AO_fWordSentiment  # double the scoring
                            AO_sLine = AO_sLine + 'emphN('+str(AO_fIntencity )+'*'+str(AO_fWordSentiment)+'-' +'): ' + AO_lTokens[j-1][0] +',' + AO_lTokens[j-1][1]+  ' ' + AO_lTokens[j][0] +',' + AO_lTokens[j][1]+ ' ~ '
                            AO_bEmphasiseFound = True
                        # end if word was emphasied
                            
                            
                    # if the negative word was not negated    
                    if (AO_bNegationFound == False) and (AO_bEmphasiseFound == False) and (AO_fAssessWord(AO_lTokens[j],['int']) <> 0):
                        AO_fNegWords = AO_fNegWords + AO_fWordSentiment
                        AO_sLine = AO_sLine + 'N('+str(AO_fWordSentiment)+'): ' + AO_lTokens[j][0] +',' + AO_lTokens[j][1] +' ~ '
                    
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
