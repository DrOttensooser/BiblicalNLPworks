'# -*- coding: utf-8 -*-'
from __future__ import division
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


# home folder
AO_sCompelationSite = 'C:\\Users\\Avner\\SkyDrive\\NLP\\BiblicalNLPworks\\'
AO_sBooksSource     = 'http://tanach.us/XMLServer?'  # http://tanach.us/XMLServer?Eccl1:1-12:14

# Calculate the name of the files
AO_ModulesPass   =  AO_sCompelationSite + 'Source Code'
WorkFileOut1     =  AO_sCompelationSite + 'Data\\MatchingPairs.CSV'
WorkFileOut2     =  AO_sCompelationSite + 'Data\\Summary.CSV'
AO_sGraphDir     =  AO_sCompelationSite + 'Graphs'



# This function
# Input   - Book details
# Process - Downloads a book from tancah.us in XML format
#           Count the length of words in each chapter
# Output  - An array with a row for every chapter having linguistic 

def AO_fNLP (AO_sNiceName, AO_sShortName, AO_iLastChapter, AO_iLastVerse):

    # ensure that the graph folder exists
    if not os.path.exists(AO_sGraphDir):
        os.makedirs(AO_sGraphDir)

    # This will include one floating point element per one chapter
    AO_lLigusticDiversity = []
    
    # this is the output of the function - a two dimentionla mtrix
    # It describes a single book.
    # It has one row per chpater.
    # Every the columns are the length of individual words in chapters 
    # AO_mChapterXwords = numpy.zeros(200*5000).reshape((200, 5000))

    # these list will include all the words in one chapter
    AO_sJchaper = ""

    AO_iWordPostionInVerse = 0
    AO_iWordPostionInChapter = 0
    AO_iVerse = 0
    AO_iChapter = 0
       
    # This calculates the URL of the XML book file in tanach.us
    AO_sBookSource = AO_sBooksSource + AO_sShortName+'1:1-'+str(AO_iLastChapter)+':'+str(AO_iLastVerse)
    
    # This is the disk location of the XML which we will next download
    WorkFileIn  =   AO_sCompelationSite + 'Data\\XML\\' + AO_sNiceName + '.XML'

    # ensure that the XML folder exists
    if not os.path.exists(AO_sCompelationSite + 'Data\\XML'):
        os.makedirs(AO_sCompelationSite + 'Data\\XML')

    # see if we need to download the book at all
    if not os.path.isfile(WorkFileIn):
        # Download the book from the net if need be
        urllib.urlretrieve(AO_sBookSource, WorkFileIn)

    # Opens the downloaded book
    AO_fInput    = codecs.open(WorkFileIn,  'r', encoding='utf-8')

    # #############################
    # Now we will pase the XML file
    # #############################


    # for all the lines in the XML file file
    for line in AO_fInput:

        # remove whight space
        line = line.strip()

        # for all the chapters in the book
        if line[0:3] =='<c ':
            AO_iChapter = AO_iChapter +1
            AO_iVerse = 0
            AO_iWordPostionInChapter = 0

            if AO_iChapter > 1:
                # summerise the chapter
                # TODO - this will not summerise the last chapter
                # print AO_sJchaper
                # load the text into NLTK
                tokens = nltk.word_tokenize(AO_sJchaper)
                text = nltk.Text(tokens)
                # find the texttual diversity
                #print len(text)
                vocab = set(text)
                vocab_size = len(vocab)
                # print vocab_size

                # find the common words in the book
                #AO_sCommonVocab =""
                #fdist1 = FreqDist(text)
                #vocabulary1 = fdist1.keys()
                #for t in range(0,5):
                #    w = vocabulary1[t]
                #    if w <> '.':
                #        AO_sCommonVocab = AO_sCommonVocab + w.decode('utf-8') + " " 
                if len(set(text)) > 0: 
                #    AO_sResult = AO_sNiceName + " " + str(AO_iChapter - 1) + " " + str(len(text)/len(set(text))) + " " + AO_sCommonVocab 
                    # print AO_sResult
                    AO_lLigusticDiversity.append(len(text)/len(set(text)))

                # Now that the chapter was analysied - clear the J list
                AO_sJchaper = ""
        else:
            # For all the verses in the chapter
            if line[0:2] == '<v':
                AO_iVerse = AO_iVerse + 1
                AO_iWordPostionInVerse = 0
            else:
                # for all the words in the verse    
                if line[0:3]== '<w>':
                    AO_iWordPostionInVerse = AO_iWordPostionInVerse + 1
                    AO_iWordPostionInChapter = AO_iWordPostionInChapter + 1

                    # Parse the word into Prefix, content and suffix
                    AO_listWord = re.compile('/',re.UNICODE).split(line[3:][:-4])

                    # if the stem has suffix(s) and or prefix(s) 
                    if len(AO_listWord) > 1:
                        AO_sWord = ''
                        AO_iWordPart = 0

                        # for all the characters in the word
                        for i in AO_listWord:
                            # rebuild the word without the prefix or suffix / sperator
                            AO_sWord = AO_sWord + i 
                            AO_iWordPart = AO_iWordPart + 1

                            # here we count the hebrew characters is the word, ignoring addents, Marks ...
                            AO_iWordLength = 0
                            AO_sWordNoNikud = ''
                            for i in AO_sWord:    
                                AO_sCharName = unicodedata.name(i)

                                # if the unicode letter it is not NIKUD
                                if  AO_sCharName[0:13] == "HEBREW LETTER":
                                    AO_iWordLength = AO_iWordLength +1
                                    AO_sWordNoNikud = AO_sWordNoNikud +i
                                    
                                    # here we print a word that has suffix, prefix or both
                                    # AO_fOutput.write(   AO_sBook + '~'+ str(AO_iChapter) + '~'+ str(AO_iVerse) + "~" + str(AO_iWordPostionInVerse) + "~" + AO_sWord +  '~' + str(AO_iWordLength) +  '~' + AO_sWordNoNikud + '\n')

                        # set the word length
                        # AO_mChapterXwords[AO_iChapter][AO_iWordPostionInChapter]=AO_iWordLength
                        AO_sJchaper = AO_sJchaper + AO_sWordNoNikud.encode('utf-8')  + " "

                    # else if the word has niether suffix nor prefix
                    else:
                        # Remove the XML stuff
                        AO_sWord = line[3:][:-4]
                        # here we count the hebrew characters is the word, ignoring addents, Marks ...
                        AO_sWordNoNikud = ''
                        AO_iWordLength = 0

                        # for all the letters in the word
                        for i in AO_sWord:
                            AO_sCharName = unicodedata.name(i)

                            # if the unicode letter it is not NIKUD
                            if  AO_sCharName[0:13] == "HEBREW LETTER":
                                AO_iWordLength = AO_iWordLength +1
                                AO_sWordNoNikud = AO_sWordNoNikud + i
                            
                        # here we print a word with no suffix or prefix
                        # AO_fOutput.write( AO_sBook + '~' + str(AO_iChapter) + '~' + str(AO_iVerse) + '~' + str(AO_iWordPostionInVerse)  + '~'  + str(AO_iWordLength)+ AO_sWordNoNikud              + '\n')

                        # set the word length
                        # AO_mChapterXwords[AO_iChapter][AO_iWordPostionInChapter]=AO_iWordLength
                        AO_sJchaper = AO_sJchaper + AO_sWordNoNikud.encode('utf-8')  + " "
                # for all the words in the verse    
            # for all the verses in the chapter
        # for all the chpater in the book
    # for all the lines in the book
    AO_fInput.close

    # summerise the last chapter
    # load the text into NLTK
    tokens = nltk.word_tokenize(AO_sJchaper)
    text = nltk.Text(tokens)
    # find the texttual diversity
    #print len(text)
    vocab = set(text)
    vocab_size = len(vocab)
    if len(set(text)) > 0: 
        AO_lLigusticDiversity.append(len(text)/len(set(text)))
    return AO_lLigusticDiversity  
