'# -*- coding: utf-8 -*-'
from __future__ import division
'''
This compares the topmost popolar words in the first Doccumente to al other Doccuments.
'''
__author__ = 'Dr Avner OTTENSOOSER <avner.ottensooser@gmail.com>'
__version__ = '$Revision: 1 $'

#import  pprint, os, nltk
#from nltk.book import * 
import re
#import unicodedata
#import numpy            # available from http://www.lfd.uci.edu/~gohlke/pythonlibs/#numpy
#import string
#from decimal import *
#import codecs
#import urllib
#import os.path
import AO_mShakespeareWorksCommon



# home folder
AO_sCompelationSite = 'C:\\Users\\Avner\\SkyDrive\\NLP\\TicketNLPWorks\\'
# Calculate the name of the files
AO_sModulesPath        =  AO_sCompelationSite + 'Source Code'
AO_sPlainTextPath      =  AO_sCompelationSite + 'Data\\Plain Text\\'
#AO_s10ersFileName      =  AO_sCompelationSite + 'Data\\CSV\\10ers.CSV'
#AO_s10erGraphsFolde    =  AO_sCompelationSite + 'Graphs\\10ers\\'
AO_sGraphsPass         =  AO_sCompelationSite + 'Graphs\\Volcublary comparison\\'
AO_sCSVfolder          =  AO_sCompelationSite + 'Data\\CSV\\'
AO_sOpinionFolder      =  AO_sCompelationSite + 'Data\\Opion-Lexicon-English\\'
AO_sPostiveWordsFile   =  AO_sOpinionFolder   + 'positive-words.txt'
AO_sNegativeWordsFile  =  AO_sOpinionFolder   + 'negative-words.txt'
AO_sNegationWordsFile  =  AO_sOpinionFolder   + 'negation-words.txt'
AO_sEmphasiseWordsFile =  AO_sOpinionFolder   + 'emphasise-words.txt'

# regular expression used to add space at the end of some words
s = re.compile(r'~')

# This will load list of negation words (no not ...)
AO_lNegationWords = []
AO_fInput = open(AO_sNegationWordsFile)
for line in AO_fInput:
    # remove whight space
    line = line.strip().lower()
    if len(line) > 0:
        if line[0] <> ";":
            line = s.sub(' ', line) #Add space at the end of a word ending with tilda ~
            AO_lNegationWords.append(line)
AO_fInput.close
AO_setNegationWords = set ( AO_lNegationWords)
print str(len(AO_setNegationWords)) + " negation words loaded from " + AO_sNegationWordsFile



# This will load list of emphsaise words (very extrimimly ...)
AO_lEmphasisWords  = []
AO_fInput = open(AO_sEmphasiseWordsFile)
for line in AO_fInput:
    # remove whight space
    line = line.strip().lower()
    if len(line) > 0:
        if line[0] <> ";":
            line = s.sub(' ', line) #Add space at the end of a word ending with tilda ~
            AO_lEmphasisWords.append(line)
AO_fInput.close
AO_setEmphasisWords = set ( AO_lEmphasisWords)
print str(len(AO_setEmphasisWords)) + " emphasis words loaded from " + AO_sEmphasiseWordsFile

# This will load list of positive words
AO_lPositiveWords = []
AO_fInput = open(AO_sPostiveWordsFile)
for line in AO_fInput:
    # remove whight space
    line = line.strip().lower()
    if len(line) > 0:
        if line[0] <> ";":
            AO_lPositiveWords.append(line)
AO_fInput.close
AO_setPositiveWords = set ( AO_lPositiveWords)

print str(len(AO_setPositiveWords)) + " positive words loaded from " + AO_sPostiveWordsFile

# This will load list of negative words
AO_lNegativeWords = []
AO_fInput = open(AO_sNegativeWordsFile)
for line in AO_fInput:
    # remove whight space
    line = line.strip().lower()
    if len(line) > 0:
        if line[0] <> ";":
            AO_lNegativeWords.append(line)
AO_fInput.close
AO_setNegativeWords = set ( AO_lNegativeWords)

print str(len(AO_lNegativeWords)) + " Negative words loaded from " + AO_sNegativeWordsFile

'''
This function
Input   - A document
Process - Lookup of all the words in the document within the positive and negative word lists
Output  - An array with Percent Pocitive Words
                        Percent Negative Words
                        Some of the above
                        Simmery line with the above percents and tagged list of all the opionion words in teh documents 

        
'''

def AO_lAssessOpinion (AO_sDocument,AO_sDocumentName,AO_sDocumentsType):

    # print AO_sDocument
    
    AO_lOpinion=[0,0,"","",""]
    AO_iPosWords = 0
    AO_iNegWords = 0
    AO_sLine = ""
    
    # we only work with lower case
    AO_sDocument=AO_sDocument.lower()
    
    AO_lTokens = AO_mShakespeareWorksCommon.AO_lTokenize(AO_sDocument)

    # for all the words in the document
    for j in range(0, len(AO_lTokens)):
        
        AO_bNegationFound = False
        # if the word is a positive word
        if AO_lTokens[j] in AO_setPositiveWords:
            
            # now we chceck word pairs, starting ofcourse with the second word
            if J > 0:
                
                # now we try all the negation words
                for k in range (0,len(AO_setNegationWords)):
                    
                    # now we check for "Not good". Note that the negation word may have a space so unimpresive will also be caught
                    if AO_setNegationWords[k] + AO_lTokens[J] == AO_lTokens[j-1] + AO_lTokens[j]:
                        AO_iNegWords = AO_iNegWords + 1 # a negation of a positive word is negative
                        AO_sLine = AO_sLine + 'notP: ' + AO_setNegationWords[k] + AO_lTokens[J] +' ~ '
                        AO_bNegationFound = True
                        break
                
                if AO_bNegationFound == False  
                        AO_iPosWords = AO_iPosWords + 1
                        AO_sLine = AO_sLine + 'P: ' + AO_lTokens[j] +' ~ '
                        
        AO_bNegationFound = False     
        # if the word is a negative words
        if AO_lTokens[j] in AO_setNegativeWords:
            
            # now we chceck word pairs, starting ofcourse with the second word
            if J > 0:
                
                # now we try all the negation words
                for k in range (0,len(AO_setNegationWords)):
                    
                    # now we check for "Not bad". Note that the negation word may have a space so unexpiring will also be caught
                    if AO_setNegationWords[k] + AO_lTokens[J] == AO_lTokens[j-1] + AO_lTokens[j]:
                        AO_iPosWords = AO_iPosWords + 1 # not bad is positive
                        AO_sLine = AO_sLine + 'notN: ' + AO_setNegationWords[k] + AO_lTokens[J] +' ~ '
                        AO_bNegationFound = True
                        break
                
                if  AO_bNegationFound == False
                    AO_iNegWords = AO_iNegWords + 1
                    AO_sLine = AO_sLine + 'N: ' + AO_lTokens[j] +' ~ '
                        
                    
            # now we chceck word pairs
            AO_iNegWords = AO_iNegWords + 1
            AO_sLine = AO_sLine + 'N: ' + AO_lTokens[j].lower() +' ~ '

        

    if len(AO_lTokens) > 0:
        
        a =  ( AO_iPosWords / len(AO_lTokens))*100
        b =  (-AO_iNegWords / len(AO_lTokens))*100
        c = a+ b

        #AO_sLine = 'Meam: ' + str(c) + ' ~ ' + AO_sLine
        #AO_sLine = 'n: '    + str(b) + ' ~ ' + AO_sLine
        #AO_sLine = 'p: '    + str(a) + ' ~ ' + AO_sLine
        
        AO_lOpinion=[a,b,c,AO_sLine]
                     
    return AO_lOpinion  
