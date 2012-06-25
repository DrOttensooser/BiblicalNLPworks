'# -*- coding: utf-8 -*-'
from __future__ import division
'''
This compares the topmost popolar words in the first Doccumente to al other Doccuments.
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
AO_sCSVfolder        =  AO_sCompelationSite + 'Data\\CSV\\'

'''
This function
Input   - Book details
Process - Downloads a book from tancah.us in XML format
          Count the length of words in each Doccumente
Output  - An array with a row for every Doccumente having linguistic 
'''

def AO_fPopularWords (AO_iLastDocument,AO_sDocumentName,AO_sDocumentsType):


    AO_sCSVfile = AO_sCSVfolder + AO_sDocumentName + " - top 20 words.CSV"
    AO_fCSV = codecs.open(AO_sCSVfile,   'w', encoding='utf-8')
    # write the header of the CSV file
    AO_fCSV.write(AO_sDocumentsType + ' ~ ')
    AO_fCSV.write('\n')

    # This will include one floating point element per one Doccumente
    AO_lLigusticDiversity = []
    AO_lLigusticDiversity.append(100) # the first record is 100 by definition
    
    # this is the output of the function - a two dimentionla mtrix
    # It describes a single book.
    # It has one row per chpater.
    # Every the columns are the length of individual words in Doccumentes 
    # AO_mDoccumenteXwords = numpy.zeros(200*5000).reshape((200, 5000))

    # these list will include all the words in one Doccumente
    AO_sJchaper = ""

    AO_iWordPostionInVerse = 0
    AO_iWordPostionInDoccumente = 0
    AO_iVerse = 0
    AO_iDoccumente = 0
       
    '''
    WorkFileOut =   AO_sCompelationSite + 'Data\\Popular Words\\' + 'Doccumentes' + '.CSV'

    # ensure that the popular words exists
    if not os.path.exists(AO_sCompelationSite + 'Data\\Popular Words\\'):
        os.makedirs(AO_sCompelationSite + 'Data\\Popular Words\\')

     
    AO_fOutpot   = codecs.open(WorkFileOut,  'w', encoding='utf-8')
    '''

    # #############################
    # Parse the first Doccument
    # #############################

    AO_sDocumentTXT  = AO_sPlainTextPath + 'o' + str(1) +  '.txt'
    AO_sDoccument = ""
    # Opens the already downloaded Essay
    AO_fInput    = codecs.open(AO_sDocumentTXT,  'r', encoding='utf-8')

    exclude = set(string.punctuation)

    # for all the lines in the Doccumente 
    for line in AO_fInput:
        # remove whight space
        line = line.strip().lower()
        # remove punctuation
        line = ''.join(ch for ch in line if ch not in exclude)
        AO_sDoccument = AO_sDoccument + line + " "

    # summerise the First Doccumente 
    # load the text Doccumente NLTK
    tokens = nltk.word_tokenize(AO_sDoccument)
    text = nltk.Text(tokens)
    fdist1 = FreqDist(text)
    vocabulary1 = fdist1.keys()
    AO_lDoccumentOneWords = vocabulary1[0:20]
    AO_fInput.close


    # write the CSV file
    AO_fCSV.write(str(1) + ' ~ ')
    for k in range (0,len(AO_lDoccumentOneWords)):
        AO_fCSV.write(str(AO_lDoccumentOneWords[k]) + ' ~ ')
    AO_fCSV.write('\n')

    # ######################################################
    # Now we will parse all the text files (one per Doccumente)
    # ######################################################

    # for all the other Doccumentes
    for j in range(2,AO_iLastDocument+1):
        AO_sDocumentTXT  = AO_sPlainTextPath + 'o' + str(j) + '.txt'
        AO_sDoccument = ""

        # Opens the already downloaded Essay
        AO_fInput    = codecs.open(AO_sDocumentTXT,  'r', encoding='utf-8')

        # print AO_sDocumentTXT

        # for all the lines in the Doccumente 
        for line in AO_fInput:
            # remove whight space
            line = line.strip()

            # remove whight space
            line = line.strip().lower()
            # remove punctuation
            line = ''.join(ch for ch in line if ch not in exclude)
            
            AO_sDoccument = AO_sDoccument + line + " "
        
       

        # summerise the J Doccumente 
        # load the text Doccumente NLTK
        tokens = nltk.word_tokenize(AO_sDoccument)
        text = nltk.Text(tokens)
        fdist = FreqDist(text)
        vocabulary1 = fdist.keys()
        AO_lDoccumentJWords = vocabulary1[0:20]
        AO_fInput.close

        # write the CSV file
        AO_fCSV.write(str(j) + ' ~ ')
        for k in range (0,len(AO_lDoccumentJWords)):
            AO_fCSV.write(str(AO_lDoccumentJWords[k]) + ' ~ ')
        AO_fCSV.write('\n')

        #print AO_sDoccument
        #print AO_lDoccumentJWords

        # Compare the top N words
        AO_iMatchRank = 0
        for q in range(0,9):
            for r in range (0,9):
                # avoid the end of short Doccuments
                if len(vocabulary1) >= q:
                    if AO_lDoccumentJWords[q]==AO_lDoccumentOneWords[r]:
                        AO_iMatchRank = AO_iMatchRank + 10 - abs(q-r)
        # print str(AO_iMatchRank)                      
        AO_lLigusticDiversity.append(AO_iMatchRank)
        AO_fInput.close()
    AO_fCSV.close
    return AO_lLigusticDiversity  
