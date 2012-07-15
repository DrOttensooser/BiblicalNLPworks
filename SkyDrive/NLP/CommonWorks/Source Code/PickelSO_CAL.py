'# -*- coding: utf-8 -*-'

'''
This module pickels the SO-CAL lexicon as four dictinary whose keys is a word and its payload is an array of Ppart Of speach, Postive and Negative valus.
'''

__author__ = 'Dr Avner OTTENSOOSER <avner.ottensooser@gmail.com>'
__version__ = '$Revision: 0.01 $'

AO_ROOT_PATH         =  'C:\\Users\\Avner\\SkyDrive\\NLP\\'
AO_DOCUMENT_NAME     =  "WordSentiNet"
AO_DOCUMENT_TYPE     =  "Word"
AO_sCommonPath       =  AO_ROOT_PATH   + 'CommonWorks\\'
AO_sCompelationPath  =  AO_sCommonPath + 'Source Code'
AO_sCommonCode       =  AO_sCompelationPath
AO_sSOcalPath        =  AO_sCommonPath + 'Data\\Opion-Lexicon-English\\SO-CAL\\'
AO_sCSVfileName      =  AO_sSOcalPath  + 'SO-CAL Lexicon.CSV'
AO_sPickeleFileName  =  AO_sSOcalPath  + 'SO-CAL Lexicon.PKL'
AO_sSOcalSuffix      =  '_dictionary1.11.txt'
AO_lSOcalTypes       =  ['adj','adv','noun','verb','int']

MinqingHuPath        = AO_sCommonPath + 'Data\\Opion-Lexicon-English\\Minqing Hu\\'
MinqingHuNeg         = MinqingHuPath  + 'negative-words.txt'
MinqingHuPos         = MinqingHuPath  + 'positive-words.txt'

 
AO_dLexicon = {}

import urllib
import os.path
import sys
import re
import codecs
import os
import nltk
# import rpy
# import numpy as np
# import matplotlib.pyplot as plt
# import shutil
# from rpy import *
# from nltk.tokenize import word_tokenize
import AO_mCommon 
# import AO_mGradeDocumentReadability
import AO_mPopularWords
# import AO_mShakespeareWorksCommon
import pickle

def AO_lParseSOcalLine(AO_sLine):

    '''

    This function parses a SO-CAL row file. The chalange is to identify when the '-' string is a hyphen pr the minus sign.
    
    Example of the parcing chalange
    
    mega-success	5
    bold	3
    built-to-last	3
    eerie	-1
    emotional	-1
    emotionally-invested	-1
    '''

    AO_sState = 'string'
    AO_lParssed = ['',0]
    AO_sWord = ''
    AO_sFloat = '0'
    
    # for all the letters in the line
    for m in range (1,len(AO_sLine)):

        if (AO_sState == "string"):
            if (AO_sLine[m].isdigit()) and (AO_sLine[m-1]=='-'):
                AO_sState = 'negativeNumber'
            if (AO_sLine[m].isdigit()) and (AO_sLine[m-1].strip()==''):
                AO_sState = 'positiveNumber'
                    
        if (AO_sState == 'negativeNumber'):
            AO_sFloat = AO_sLine[m-1:]
            AO_sWord  = AO_sLine[0:m-2].strip()
            break
                    
        if (AO_sState == 'positiveNumber'):
            AO_sFloat = AO_sLine[m:]
            AO_sWord  = AO_sLine[0:m-1].strip()
            break
                    
    AO_lParssed[0] = AO_sWord
    AO_lParssed[1] = AO_sFloat                
    return AO_lParssed

def main():


    AO_fcsvOut   = codecs.open(AO_sCSVfileName,   'w', encoding='utf-8')
    AO_fpklOut   = open(AO_sPickeleFileName, 'wb')
    AO_lLexicon  =[]
    AO_fcsvOut.write("POS ~")
    AO_fcsvOut.write("SO-CAL Score ~")
    AO_fcsvOut.write("Term \n")

   # read the SO-Cal list
  
    for j in range (0,len(AO_lSOcalTypes)):
        AO_fInput    = open(AO_sSOcalPath + AO_lSOcalTypes[j]  + AO_sSOcalSuffix,  'r')
        
        # for all the lines in the lexicon
        for line in AO_fInput:
            AO_fcsvOut.write ("Line~")
            AO_fcsvOut.write(unicode(line, errors='ignore') + '\n')
            # remove whight space
            line = line.strip() + " "
            # break the document into individual words (tokenize)
            if len(line) > 0:
                if line[0] <> "#": # ignore the comments at the header
                    AO_lTokens = AO_lParseSOcalLine(line)
                    AO_fcsvOut.write ("raw tokanisation~")

                    for k in range (0, len(AO_lTokens)):
                        AO_fcsvOut.write(   unicode(AO_lTokens[k], errors='ignore') + '~')
                    AO_fcsvOut.write ("\n")

                    AO_lTapple = [AO_lSOcalTypes[j]+AO_lTokens[0],float(AO_lTokens[1])]
                    AO_fcsvOut.write ("Pikled tokanisation~")
                    AO_fcsvOut.write(  AO_lSOcalTypes[j])
                    AO_fcsvOut.write(  unicode(AO_lTokens[0], errors='ignore') + "~")
                    AO_fcsvOut.write(  unicode(AO_lTokens[1], errors='ignore') +  "\n")
                    AO_lLexicon.append(AO_lTapple)
        AO_fInput.close
     
    # read the Minqing Hu Positive list
    AO_fInput    = open(MinqingHuPos,  'r')
    for line in AO_fInput:
        # remove whight space
        line = line.strip().lower()
        if len(line) > 0:
            if line[0] <> ";": # ignore the comments at the header
                AO_fcsvOut.write ("raw tokanisation~" + unicode(line, errors='ignore') + '\n')
                AO_fcsvOut.write (  unicode(line, errors='ignore') +'~' + str(float(2.5))+ '\n')
                AO_lTapple = ['minqinghu'+line,float(2.5)]
                AO_lLexicon.append(AO_lTapple)
    AO_fInput.close

    

    # read the Minqing Hu negative list
    AO_fInput    = open(MinqingHuNeg,  'r')
    for line in AO_fInput:
        # remove whight space
        line = line.strip()
        if len(line) > 0:
            if line[0] <> ";": # ignore the comments at the header
                AO_fcsvOut.write ("raw tokanisation~" + unicode(line, errors='ignore') + '\n')
                AO_fcsvOut.write (unicode(line, errors='ignore') +'~' + str(float(-2.5))+ '\n')
                AO_lTapple = ['minqinghu'+line,float(-2.5)]
                AO_lLexicon.append(AO_lTapple)
    AO_fInput.close
        
    # convert the tupple into a dictionary
    AO_dLexicon = dict(AO_lLexicon)

    # store the dictionary
    pickle.dump( AO_dLexicon, AO_fpklOut )
    
    AO_fpklOut.close
    AO_fcsvOut.close
    
if __name__ == '__main__':
   
    main()
