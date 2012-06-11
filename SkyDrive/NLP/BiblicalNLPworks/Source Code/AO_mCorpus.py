import re
import unicodedata
# import numpy            # available from http://www.lfd.uci.edu/~gohlke/pythonlibs/#numpy
import string
from decimal import *
import codecs
import urllib

# home folder
AO_sCompelationSite = 'C:\\Users\\Avner\\SkyDrive\\NLP\\BiblicalNLPworks\\'
AO_sBooksSource     = 'http://tanach.us/XMLServer?'  # http://tanach.us/XMLServer?Eccl1:1-12:14

# Calculate the name of the files
AO_ModulesPass   =  AO_sCompelationSite + 'Source Code'
WorkFileOut1     =  AO_sCompelationSite + 'Data\\MatchingPairs.CSV'
WorkFileOut2     =  AO_sCompelationSite + 'Data\\Summary.CSV'
AO_sGraphDir     =  AO_sCompelationSite + 'Graphs'


# input - text
# Output - an indication of the richness of the text
def A0_fLexicalDiversity(text):
    return float(len(text)) / float(len(set(text)))

# Input   - Book details
# Process - Downloads a book from tancah.us in XML format
#           Count the length of words in each chapter
# Output  - 

def AO_fCorpus (AO_sNiceName, AO_sShortName, AO_iLastChapter, AO_iLastVerse):
    
    # this is the output of the function - a two dimentionla mtrix
    # It describes a single book.
    # It has one row per chpater.
    # Every the columns are the length of individual words in chapters 
    # AO_mChapterXwords = numpy.zeros(200*5000).reshape((200, 5000))

    # these list will include only one chapter
    # AO_lIchaper = []
    AO_lJchaper = []

    AO_iWordPostionInVerse = 0
    AO_iWordPostionInChapter = 0
    AO_iVerse = 0
    AO_iChapter = 0
       
    # This calculates the URL of the XML book file in tanach.us
    AO_sBookSource = AO_sBooksSource + AO_sShortName+'1:1-'+str(AO_iLastChapter)+':'+str(AO_iLastVerse)
    
    # This is the disk location of the XML which we will next download
    WorkFileIn  =   AO_sCompelationSite + 'Data\\' + AO_sNiceName + '.XML'

    WorkFileOut  =   AO_sCompelationSite + 'Data\\' + AO_sNiceName + '.TXT'

    # TODO see if we need to download the book at all

    # Download the book from the net 
    # urllib.urlretrieve(AO_sBookSource, WorkFileIn)

    # Opens the downloaded book
    AO_fInput    = codecs.open(WorkFileIn,  'r', encoding='utf-8')
    WorkFileOut  = codecs.open(WorkFileOut,  'w', encoding='utf-8')

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
           

        else:
            # For all the verses in the chapter
            if line[0:2] == '<v':
                # if AO_iVerse > 0:
                WorkFileOut.write("\n .")
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
                        WorkFileOut.write(AO_sWordNoNikud + " ")
                        # print AO_sWordNoNikud
                        # set the word length
                        # AO_mChapterXwords[AO_iChapter][AO_iWordPostionInChapter]=AO_iWordLength

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
                        WorkFileOut.write(AO_sWordNoNikud + " ")
                        # print AO_sWordNoNikud
                        # set the word length
                        # AO_mChapterXwords[AO_iChapter][AO_iWordPostionInChapter]=AO_iWordLength
                    # if it a suffixed word or not    
                # if it is a word
            #if it is a verse
        #if it is a chapter
    AO_fInput.close
    return 1  
