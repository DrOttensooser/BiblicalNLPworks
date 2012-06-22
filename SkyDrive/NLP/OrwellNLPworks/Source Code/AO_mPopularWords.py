'# -*- coding: utf-8 -*-'
from __future__ import division
'''
This compares the topmost popolar words in the first sonnete to al other sonnets.
'''
__author__ = 'Dr Avner OTTENSOOSER <avner.ottensooser@gmail.com>'
__version__ = '$Revision: 1 $'

import  pprint, os, nltk
from nltk.book import * 
import re
import unicodedata
import numpy            # available from http://www.lfd.uci.edu/~gohlke/pythonlibs/#numpy
import string
from decimal import *
import codecs
import urllib
import os.path
import AO_mShakespeareWorksCommon



# home folder
AO_sCompelationSite = 'C:\\Users\\Avner\\SkyDrive\\NLP\\OrwellNLPworks\\'
# Calculate the name of the files
AO_sModulesPath      =  AO_sCompelationSite + 'Source Code'
AO_sModulesPath      =  AO_sCompelationSite + 'Source Code'
AO_sPlainTextPath    =  AO_sCompelationSite + 'Data\\Plain Text\\'
AO_s10ersFileName    =  AO_sCompelationSite + 'Data\\CSV\\10ers.CSV'
AO_s10erGraphsFolde  =  AO_sCompelationSite + 'Graphs\\10ers\\'
AO_sGraphsPass       =  AO_sCompelationSite + 'Graphs\\Volcublary comparison\\'

'''
This function
Input   - Book details
Process - Downloads a book from tancah.us in XML format
          Count the length of words in each Sonnete
Output  - An array with a row for every Sonnete having linguistic 
'''

def AO_fPopularWords (AO_iLastEssay):

    # This will include one floating point element per one Sonnete
    AO_lLigusticDiversity = []
    
    # this is the output of the function - a two dimentionla mtrix
    # It describes a single book.
    # It has one row per chpater.
    # Every the columns are the length of individual words in Sonnetes 
    # AO_mSonneteXwords = numpy.zeros(200*5000).reshape((200, 5000))

    # these list will include all the words in one Sonnete
    AO_sJchaper = ""

    AO_iWordPostionInVerse = 0
    AO_iWordPostionInSonnete = 0
    AO_iVerse = 0
    AO_iSonnete = 0
       
    '''
    WorkFileOut =   AO_sCompelationSite + 'Data\\Popular Words\\' + 'Sonnetes' + '.CSV'

    # ensure that the popular words exists
    if not os.path.exists(AO_sCompelationSite + 'Data\\Popular Words\\'):
        os.makedirs(AO_sCompelationSite + 'Data\\Popular Words\\')

     
    AO_fOutpot   = codecs.open(WorkFileOut,  'w', encoding='utf-8')
    '''

    # #############################
    # Parse the first sonnet
    # #############################

    AO_sEssay = ""
    AO_sRoman      = AO_mShakespeareWorksCommon.Arab2Roman(1)
    AO_sSonnetTXT  = AO_sPlainTextPath + 'o' + str(1) +  '.txt'

    # Opens the already downloaded Essay
    AO_fInput    = codecs.open(AO_sSonnetTXT,  'r', encoding='utf-8')

    # for all the lines in the sonnete 
    for line in AO_fInput:
        # remove whight space
        line = line.strip()
        AO_sEssay = AO_sEssay + line + " "

    # summerise the First sonnete 
    # load the text sonnete NLTK
    tokens = nltk.word_tokenize(AO_sEssay)
    text = nltk.Text(tokens)
    fdist1 = FreqDist(text)
    vocabulary1 = fdist1.keys()
    AO_lSonnetOneWords = vocabulary1[0:20]
    AO_fInput.close
    

    # ######################################################
    # Now we will parse all the text files (one per sonnete)
    # ######################################################

    # for all the other sonnetes
    for j in range(2,AO_iLastEssay):
        AO_sSonnetTXT  = AO_sPlainTextPath + 'o' + str(j) + '.txt'
        AO_sEssay = ""

        # Opens the already downloaded Essay
        AO_fInput    = codecs.open(AO_sSonnetTXT,  'r', encoding='utf-8')

        # print AO_sSonnetTXT

        # for all the lines in the sonnete 
        for line in AO_fInput:
            # remove whight space
            line = line.strip()
            AO_sEssay = AO_sEssay + line + " "
        
       

        # summerise the J sonnete 
        # load the text sonnete NLTK
        tokens = nltk.word_tokenize(AO_sEssay)
        text = nltk.Text(tokens)
        fdist = FreqDist(text)
        vocabulary1 = fdist.keys()
        AO_lSonnetJWords = vocabulary1[0:20]
        AO_fInput.close

        #print AO_sEssay
        #print AO_lSonnetJWords

        # Compare the top N words
        AO_iMatchRank = 0
        for q in range(0,9):
            for r in range (0,9):
                # avoid the end of short Sonnetes
                if len(vocabulary1) >= q:
                    if AO_lSonnetJWords[q]==AO_lSonnetOneWords[r]:
                        AO_iMatchRank = AO_iMatchRank + 10 - abs(q-r)
        # print str(AO_iMatchRank)                      
        AO_lLigusticDiversity.append(AO_iMatchRank)
        AO_fInput.close()
    return AO_lLigusticDiversity  
