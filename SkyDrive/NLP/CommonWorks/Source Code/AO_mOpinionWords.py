'# -*- coding: utf-8 -*-'
from __future__ import division
'''
Here we rank a documents author's opinions by looking for key words compiled by Minqing Hu and Bing Liu 
http://www.cs.uic.edu/~liub/FBS/sentiment-analysis.html 
and by Taboada et al (lexicon-Base dMethods for Sentiment Analysis). 

We break the document into individual sentences, then we perform part of speach analysis on each sentence.

For any word/POS tapple we look up for sentiment in a Taboada et al lexicon.  Failing to find the word,
We look up the word in Minqing Hu lexicon. 

Failing to do this we stem the word and repeat until there is nothing to stem.

We account for Taboada et al intensifiers as well as to our own list of negators.
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
AO_iNEGATIONconstatnt       =  2 # Taboada et al. p277
AO_setNegationWords         =  set(['no',"not","none","dosn't","nobody","never","nothing","without","lack","haven't","hadn't","don't","isn't","aren't'"])

import re
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
AO_setNoun          = set(['SYM','NN','BB$','NNP','NNPS','NNP$','NP','NP$','NPS$','NR','N'])
AO_setAdjective     = set(['JJ','JJR','JJS','JJT','ADJ','UH','NNS'])
AO_setVerb          = set(['VB','VBD','VBG','VBN','VBZ','VBP','MD'])
AO_setAdverb        = set(['RB','RBR','RBT','RN','RP','ADV','RBS'])
AO_setOther         = set(['EX','FW','CD','WP','WDT','WP$','IN',"''",'PRP','PRP$','DT','RPR','CC','TO','POS','WRB','#','$',"``",',',':',' ','','.'])

# load the SO-CAL and Minqing Hu lexicons craeted by the PickelSO_CAL programme
AO_fPickle  = open(AO_sSOcalPickeleFileName, 'rb')
AO_dLexicon = pickle.load(AO_fPickle)
AO_fPickle.close
print str(len(AO_dLexicon)) + " SO-CAL and Minqing Hu terms were unpickeled from: " + AO_sSOcalPickeleFileName + ' . \n'

def AO_fAssessWord(AO_sWord, AO_lTypes):

    # lockup a string in the SO-CAL lexicon using a hash of the word type and the word and 
    # GIVE the SO-CAl rating between -5 and +5

    # print '>' + AO_sWord[0] + '< >' + AO_sWord[1] + '<'

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
            elif AO_sWord[1] in AO_setOther:
                 AO_sFirstCandidate = '-'
            else:
                print "Un expectet Taple: >" + str(AO_sWord[0]) + '< >' + str(AO_sWord[1]) + '<'
                AO_sFirstCandidate = '-'
                
            # try 1 - MSO-Cal  lexicon
            AO_sCompundKey = AO_sFirstCandidate+AO_sCurrentWord
            _fAssessWord = AO_dLexicon.get(AO_sCompundKey,float(0))

            if AO_bBeGriddy:
                # try 2 - Minqing Hu lexicon
                # if the word is not fount in the SO-CAL lexicon, fall back to the Minqing Hu lexicon
                if (_fAssessWord == float(0)):
                    AO_sCompundKey = 'minqinghu' + AO_sCurrentWord
                    _fAssessWord = AO_dLexicon.get(AO_sCompundKey,float(0))  
                    
                # try 3 - recursive stem
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

    

def AO_lAssessOpinion (AO_sDocument):

    
    '''
    This function
    Input   - A document
    
    Output  - An array with Percent Pocitive Words
                            Percent Negative Words
                            Some of the above
                            Summery line with the above percents and tagged list of all the opionion words in teh documents 
    '''


    
    AO_lOpinion=[0,0,"","",""]
    AO_fPosWords = 0
    AO_fNegWords = 0
    AO_sLine = ""

    if AO_sDocument.strip() =='':
        return AO_lOpinion
     
    # Break the document into sentences
    AO_lSentences = sent_tokenize(AO_sDocument)

    
    # For all the sentences in the document
    for i in range (0, len(AO_lSentences)):
        
        # identify the POS
        tokens = tokenize.WordPunctTokenizer().tokenize(AO_lSentences[i])
        AO_lTokens = tagger.tag(tokens)
        
        AO_bNetNegation = False
        AO_sNegationPhrase = ''

        # for all the individual words in the sentece
        for j in range(0, len(AO_lTokens)):
            
            AO_fWordSentiment =0
            
            # see if this is a negator
            if str(AO_lTokens[j][0]).lower() in AO_setNegationWords:
                AO_bNetNegation = not AO_bNetNegation
            
            if AO_bNetNegation:
                AO_sNegationPhrase = AO_sNegationPhrase + ' ' + AO_lTokens[j][0]
        
            else:
                AO_sNegationPhrase =''

            # is this a negation word , we will deal with it with next words    
            if str(AO_lTokens[j][0]).lower() not in AO_setNegationWords:        

                # if this is an internsifier, we will deal with it with next word
                if AO_fAssessWord(AO_lTokens[j],['int']) == 0:

                    AO_fWordSentiment = AO_fAssessWord(AO_lTokens[j],['adj','adv','noun','verb','minqinghu'])
                    
                    # if the word is a positive word
                    if abs(AO_fWordSentiment) > 0:
                        
                        if (j == 0):
                            if(AO_fWordSentiment > 0):
                                # Firts ford positive sentiment
                                AO_fPosWords = AO_fPosWords + AO_fWordSentiment
                                AO_sLine = AO_sLine                     +\
                                'P ('                                   +\
                                str(AO_fWordSentiment)                  +\
                                '): '                                   +\
                                str(AO_lTokens[j][0])                   +\
                                ' '                                     +\
                                str(str(AO_lTokens[j][1]))              +\
                                ' ~ '
                            
                            elif(AO_fWordSentiment < 0):
                                # First word Negative sentiment
                                AO_fNegWords = AO_fNegWords + AO_fWordSentiment
                                AO_sLine = AO_sLine                     +\
                                'N('                                    +\
                                str(AO_fWordSentiment)                  +\
                                '): '                                   +\
                                str(AO_lTokens[j][0])                   +\
                                ','                                     +\
                                str(AO_lTokens[j][1])                   +\
                                ' ~ '

                        else: # if this is not the first word in the sentence, 
                              # then it may have been intensified by the word before it
                            AO_fIntensifier = AO_fAssessWord(AO_lTokens[j-1],['int'])

                            if   (AO_fWordSentiment > 0)      \
                            and (AO_fIntensifier == float(0)) \
                            and (AO_bNetNegation == True):
                                # Negated Positve sentiment (but not intencified)

                                AO_fPosWords = AO_fPosWords + AO_fWordSentiment - AO_iNEGATIONconstatnt
                                AO_sLine = AO_sLine                     +\
                                'NegatedP (' +str(AO_fWordSentiment)    +\
                                ' - '                                   +\
                                str(AO_iNEGATIONconstatnt)              +\
                                '): '                                   +\
                                AO_sNegationPhrase                      +\
                                ' ~ '
                                
                            elif (AO_fWordSentiment > 0)      \
                            and (AO_fIntensifier <> float(0)) \
                            and (AO_bNetNegation == False):
                                #  Intencified Positve sentiment that is not negated

                                AO_fSentiment = AO_fWordSentiment* (1+AO_fIntensifier)
                                AO_fPosWords = AO_fPosWords + AO_fSentiment # double the scoring
                                AO_sLine = AO_sLine                     +\
                                'emphP((1+'                             +\
                                str(AO_fIntensifier)                    +\
                                ')*('                                   +\
                                str(AO_fWordSentiment )                 +\
                                ')=('+str(AO_fSentiment)                +\
                                ')): '                                  +\
                                str(AO_lTokens[j-1][0])                 +\
                                ' '                                     +\
                                str(AO_lTokens[j][0])                   +\
                                ' , '                                   +\
                                str(AO_lTokens[j-1][1])                 +\
                                ' '                                     +\
                                str(AO_lTokens[j][1])                   +\
                                ' ~ '

                                
                            elif (AO_fWordSentiment > 0)       \
                            and (AO_fIntensifier <>  float(0)) \
                            and (AO_bNetNegation == True):
                                #Negated postive word that is intencified

                                AO_fSentiment = AO_fWordSentiment* (1+AO_fIntensifier) - AO_iNEGATIONconstatnt
                                AO_fPosWords = AO_fPosWords + AO_fSentiment # double the scoring
                                AO_sLine = AO_sLine                     +\
                                'NegatedEmphP((1+'                      +\
                                str(AO_fIntensifier)                    +\
                                ')*('                                   +\
                                str(AO_fWordSentiment )                 +\
                                '-'+str(AO_iNEGATIONconstatnt)          +\
                                ')=('                                   +\
                                str(AO_fSentiment)                      +\
                                ')): '                                  +\
                                AO_sNegationPhrase                      +\
                                ' ~ '
                                
                                
                            elif (AO_fWordSentiment > 0)       \
                            and (AO_fIntensifier ==  float(0)) \
                            and (AO_bNetNegation == False):
                                # Nth Positive sentiment, nither negated nor intencified

                                AO_fPosWords = AO_fPosWords + AO_fWordSentiment
                                AO_sLine = AO_sLine                     +\
                                'P ('                                   +\
                                str(AO_fWordSentiment)                  +\
                                '): '                                   +\
                                str(AO_lTokens[j][0])                   +\
                                ' '                                     +\
                                str(str(AO_lTokens[j][1]))              +\
                                ' ~ '
                            
                            elif (AO_fWordSentiment < 0)      \
                            and (AO_fIntensifier <> float(0)) \
                            and (AO_bNetNegation == True):
                                # negated emphesised negative sentimet
                                
                                AO_fSentiment = AO_fWordSentiment* (1+AO_fIntensifier) + AO_iNEGATIONconstatnt
                                AO_fNegWords = AO_fNegWords + AO_fSentiment  # double the scoring
                                AO_sLine = AO_sLine                     +\
                                'NegatedEmphN((1+'                      +\
                                str(AO_fIntensifier)                    +\
                                ')*('                                   +\
                                str(AO_fWordSentiment )                 +\
                                '-'                                     +\
                                str(AO_iNEGATIONconstatnt)              +\
                                ')=('                                   +\
                                AO_sNegationPhrase                      +\
                                ' ~ '
                                
                                
                            elif (AO_fWordSentiment < 0)      \
                            and (AO_fIntensifier <> float(0)) \
                            and (AO_bNetNegation == False):
                                # emphesised Negative sentiment

                                AO_fSentiment = AO_fWordSentiment* (1+AO_fIntensifier)
                                AO_fNegWords = AO_fNegWords + AO_fSentiment  # double the scoring
                                AO_sLine = AO_sLine                     +\
                                'emphN((1+'                             +\
                                str(AO_fIntensifier)                    +\
                                ')*('                                   +\
                                str(AO_fWordSentiment )                 +\
                                ')=('+str(AO_fSentiment)                +\
                                ')): '                                  +\
                                str(AO_lTokens[j-1][0])                 +\
                                ' '                                     +\
                                str(AO_lTokens[j][0])                   +\
                                ' , '                                   +\
                                str(AO_lTokens[j-1][1])                 +\
                                ','                                     +\
                                str(AO_lTokens[j][1])                   +\
                                ' ~ '
                                
                            elif (AO_fWordSentiment < 0)       \
                            and (AO_fIntensifier ==  float(0)) \
                            and (AO_bNetNegation == True):
                                # Negated Negative Sentiment

                                AO_fNegWords = AO_fNegWords + AO_fWordSentiment + AO_iNEGATIONconstatnt
                                AO_sLine = AO_sLine                     +\
                                'N('                                    +\
                                str(AO_fWordSentiment)                  +\
                                '+'                                     +\
                                str(AO_iNEGATIONconstatnt)              +\
                                '): '                                   +\
                                AO_sNegationPhrase                      +\
                                ' ~ '

                                
                            elif (AO_fWordSentiment < 0)       \
                            and (AO_fIntensifier ==  float(0)) \
                            and (AO_bNetNegation == False):
                                # Nth Negative sentiment
                                
                                AO_fNegWords = AO_fNegWords + AO_fWordSentiment
                                AO_sLine = AO_sLine                     +\
                                'N('                                    +\
                                str(AO_fWordSentiment)                  +\
                                '): '                                   +\
                                str(AO_lTokens[j][0])                   +\
                                ','                                     +\
                                str(AO_lTokens[j][1])                   +\
                                ' ~ '

                            # end elif
                        # end if - first word
                    # endif negarive word
                # endif this is an intensifier
            # endif the word is a negator
        # for all the words in the sentence
    #for all the sentences in the document
    
    if len(AO_lTokens) > 0:
        
        a =  round(AO_fPosWords,2) 
        b =  round(AO_fNegWords,2) 
        c =  round(a+ b,2)
        
        AO_lOpinion=[a,b,c,AO_sLine]
                     
    return AO_lOpinion 
    
# end of function

def AO_TestMe (AO_sDocument,AO_sTestDescription, AO_lExpectedResult):

    AO_lOpinion = AO_lAssessOpinion(AO_sDocument)
    
    AO_bReult =                                 \
    (                                           \
    (AO_lOpinion[0]==AO_lExpectedResult[0]) and \
    (AO_lOpinion[1]==AO_lExpectedResult[1]) and \
    (AO_lOpinion[2]==AO_lExpectedResult[2]) and \
    (AO_lOpinion[3]==AO_lExpectedResult[3])     \
    )
    
    if AO_bReult == False:
        print '**** Failed test case ****'
        print AO_sTestDescription 
        print AO_sDocument 
        print 'Expected result:  '
        print AO_lExpectedResult
        print 'Actual resalt:  '
        print AO_lOpinion   

    return AO_bReult

if __name__ == '__main__':

    # unit tests
    AO_bTest = AO_TestMe('The cat sat on the mat.'                                                  ,\
    'TC00 Pos:Not Neg:Not Emph:Not Ngegated:Not 1st Word:Not'                                       ,\
    [0,0,0,''])
    
    AO_bTest = AO_bTest and AO_TestMe('No cat sat on the mat.'                                      ,\
    'TC02 Pos:Not Neg:Yes Emph:Not Ngegated:Yes 1st Word:Not'                                       ,\
    [0,0,0,''])
    
    AO_bTest = AO_bTest and AO_TestMe('Sorta cat sat on the mat.'                                   ,\
    'TC04 Pos:Not Neg:Not Emph:Yes Ngegated:Not 1st Word:Not'                                       ,\
    [0,0,0,''])
    
    AO_bTest = AO_bTest and AO_TestMe('No cat mostly sat on a mat.'                                 ,\
    'TC06 Pos:Not Neg:Not Emph:Yes Ngegated:Yes 1st Word:Not'                                       ,\
    [0,0,0,''])
    
    AO_bTest = AO_bTest and AO_TestMe('The fat cat sat on the mat.'                                 ,\
    'TC08 Pos:Not Neg:Yes Emph:Not Ngegated:Not 1st Word:Not'                                       ,\
    [0, -3.0, -3.0, 'N(-3.0): fat,JJ ~ '])
    
    AO_bTest = AO_bTest and AO_TestMe('No fat cat sat on the mat.'                                  ,\
    'TC10 Pos:Not Neg:Yes Emph:Not Ngegated:Yes 1st Word:Not'                                       ,\
    [0, -1.0, -1.0, 'N(-3.0+2):  No fat ~ '])
   
    AO_bTest = AO_bTest and AO_TestMe('Very fat cat sat on the mat.'                                ,\
    'TC12 Pos:Not Neg:Yes Emph:Yes Ngegated:Not 1st Word:Not'                                       ,\
    [0.0, -3.6, -3.6, 'emphN((1+0.2)*(-3.0)=(-3.6)): Very fat , NN,JJ ~ '])
    
    AO_bTest = AO_bTest and AO_TestMe('The priceless cat sat on the mat.'                           ,\
    'TC16 Pos:Yes Neg:Yes Emph:Not Ngegated:Not 1st Word:Not'                                       ,\
    [5.0, 0.0, 5.0, 'P (5.0): priceless JJ ~ '])
    
    AO_bTest = AO_bTest and AO_TestMe('Priceless cat sat on the mat.'                               ,\
    'TC17 Pos:Yes Neg:Yes Emph:Not Ngegated:Not 1st Word:Yes'                                       ,\
    [5.0, 0.0, 5.0, 'P (5.0): Priceless NNS ~ '])
    
    AO_bTest = AO_bTest and AO_TestMe('No priceless cat sat on the mat.'                            ,\
    'TC18 Pos:Yes Neg:Not Emph:Not Ngegated:Yes 1st Word:Not'                                       ,\
    [3.0, 0.0, 3.0, 'NegatedP (5.0 - 2):  No priceless ~ '])
    
    AO_bTest = AO_bTest and AO_TestMe('Very priceless cat sat on the mat.'                          ,\
    'TC20 Pos:Yes Neg:Not Emph:Yes Ngegated:Not 1st Word:Not'                                       ,\
    [6.0, 0.0, 6.0, 'emphP((1+0.2)*(5.0)=(6.0)): Very priceless , NN JJ ~ '])
    
    AO_bTest = AO_bTest and AO_TestMe('Not a single very charming cat sat on the mat.'              ,\
    'TC22 Pos:Yes Neg:Not Emph:Yes Ngegated:Yes 1st Word:Not'                                       ,\
    [2.8, 0.0, 2.8, 'NegatedEmphP((1+0.2)*(4.0-2)=(2.8)):  Not a single very charming ~ '])
    
    AO_bTest = AO_bTest and AO_TestMe('Not a single very charming fat cat sat on the mat.'          ,\
    'TC22 Pos:Yes Neg:Not Emph:Yes Ngegated:Yes 1st Word:Not'                                       ,\
    [2.8, -1.0, 1.8, 'NegatedEmphP((1+0.2)*(4.0-2)=(2.8)):  Not a single very charming ~ N(-3.0+2):  Not a single very charming fat ~ '])

    AO_bTest = AO_TestMe('The cat sat on the mat. No cat sat on the mat. Sorta cat sat on the mat.', 'Combinatoion',[0,0,0,''])

    print '\nUnit Test passed = ' + str(AO_bTest) +'.\n'

    
 
