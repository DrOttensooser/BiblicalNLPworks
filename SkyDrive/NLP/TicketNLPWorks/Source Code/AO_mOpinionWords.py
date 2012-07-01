'# -*- coding: utf-8 -*-'
from __future__ import division
'''
This compares the topmost popolar words in the first Doccumente to al other Doccuments.
'''
__author__ = 'Dr Avner OTTENSOOSER <avner.ottensooser@gmail.com>'
__version__ = '$Revision: 1 $'

#import  pprint, os, nltk
#from nltk.book import * 
#import re
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
AO_sModulesPath      =  AO_sCompelationSite + 'Source Code'
AO_sModulesPath      =  AO_sCompelationSite + 'Source Code'
AO_sPlainTextPath    =  AO_sCompelationSite + 'Data\\Plain Text\\'
AO_s10ersFileName    =  AO_sCompelationSite + 'Data\\CSV\\10ers.CSV'
AO_s10erGraphsFolde  =  AO_sCompelationSite + 'Graphs\\10ers\\'
AO_sGraphsPass       =  AO_sCompelationSite + 'Graphs\\Volcublary comparison\\'
AO_sCSVfolder        =  AO_sCompelationSite + 'Data\\CSV\\'
AO_sOpinionFolder    =  AO_sCompelationSite + 'Data\\Opion-Lexicon-English\\'
AO_sPostiveWordsFile =  AO_sOpinionFolder   + 'positive-words.txt'
AO_sNegativeWordsFile=  AO_sOpinionFolder   + 'negative-words.txt'

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
    
    AO_lTokens = AO_mShakespeareWorksCommon.AO_lTokenize(AO_sDocument)

    for j in range(0, len(AO_lTokens)):
        if AO_lTokens[j].lower() in AO_setPositiveWords:
            AO_iPosWords = AO_iPosWords + 1
            AO_sLine = AO_sLine + 'P: ' + AO_lTokens[j].lower() +' ~ '

        if AO_lTokens[j].lower() in AO_setNegativeWords:
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
