'# -*- coding: utf-8 -*-'

'''
This module pickels the WordSentiNet lexicon as a dictiinary whose key is a word and its payload is an array of Ppart Of speach, Postive and Negative valus.
'''

__author__ = 'Dr Avner OTTENSOOSER <avner.ottensooser@gmail.com>'
__version__ = '$Revision: 0.01 $'

AO_ROOT_PATH         =  'C:\\Users\\Avner\\SkyDrive\\NLP\\'
AO_DOCUMENT_NAME     =  "WordSentiNet"
AO_DOCUMENT_TYPE     =  "Word"
AO_sCommonPath       =  AO_ROOT_PATH + 'CommonWorks\\'
AO_sCompelationPath  =  AO_sCommonPath + 'Source Code'
AO_sCommonCode       =  AO_sCompelationPath
AO_sCSVPath          =  AO_sCompelationPath + 'Data\\CSV\\'
AO_sSource           =  AO_sCommonPath + 'Data\\Opion-Lexicon-English\\SentiWordNet_3.txt'
AO_sCSVfileName      =  AO_sCommonPath + 'Data\\Opion-Lexicon-English\\SentiWordNet_3.csv'
AO_sPickelfileName   =  AO_sCommonPath + 'Data\\Opion-Lexicon-English\\SentiWordNet_3.pkl'

AO_dLexicon = {}

import urllib
import os.path
import sys
import re
import codecs
import os
import nltk
import rpy
import numpy as np
import matplotlib.pyplot as plt
import shutil
from rpy import *
from nltk.tokenize import word_tokenize
import AO_mOpinionWords
import AO_mCommon 
import AO_mGradeDocumentReadability
import AO_mPopularWords
import AO_mShakespeareWorksCommon
import pickle

'''
0 1        2   3   4         5 6              7
a 01115635 0.4 0.6 veritable 2 unquestionable 2 bona_fide#2 authentic#2	not counterfeit or copied; "an authentic signature"; "a bona fide manuscript"; "an unquestionable antique"; "photographs taken in a veritable bull ring" 
'''

def main():

    AO_fInput    = open(AO_sSource,  'r')
    AO_fcsvOut   = codecs.open(AO_sCSVfileName,   'w', encoding='utf-8')
    AO_fpklOut   = open(AO_sPickelfileName, 'wb')
    
    AO_lLexicon  =[]
    
    AO_fcsvOut.write("POS ~")
    AO_fcsvOut.write("PosScore ~")
    AO_fcsvOut.write("NegScore ~")
    AO_fcsvOut.write("Term \n")
  
    # for all the lines in the lexicon
    for line in AO_fInput:
        # remove whight space
        line = line.strip() + " "
        # break the document into individual words (tokenize)
        if len(line) > 0:
            if line[0] <> "#": # ignore the comments at the header
                AO_lTokens = AO_mShakespeareWorksCommon.AO_lTokenize(line)
                if len(AO_lTokens) > 6:
                    
                    # if it is not a nutral expression
                    if (AO_lTokens[2] <> '0') or (AO_lTokens[3] <> '0'):
                        AO_fcsvOut.write(  AO_lTokens[0] + "~")
                        AO_fcsvOut.write(  AO_lTokens[2] + "~")
                        AO_fcsvOut.write(  AO_lTokens[3] + "~")
                        AO_fcsvOut.write(  AO_lTokens[4] + "\n")

                        AO_lLexicon.append([AO_lTokens[4],[AO_lTokens[0] ,  float(AO_lTokens[2])*5 , (-5) *  float(AO_lTokens[3])]])
                        
                        if len(AO_lTokens) > 7:
                            if AO_lTokens[7].isdigit():
                                AO_fcsvOut.write(  AO_lTokens[0] + "~") 
                                AO_fcsvOut.write(  AO_lTokens[2] + "~")
                                AO_fcsvOut.write(  AO_lTokens[3] + "~")
                                AO_fcsvOut.write(  AO_lTokens[6] + "\n")

                                AO_lLexicon.append([AO_lTokens[6],[AO_lTokens[0] ,  float(AO_lTokens[2])*5 , (-5) *  float(AO_lTokens[3])]])

                                if len(AO_lTokens) > 9:    
                                    if AO_lTokens[9].isdigit():
                                        AO_fcsvOut.write(   AO_lTokens[0] + "~")
                                        AO_fcsvOut.write(   AO_lTokens[2] + "~")
                                        AO_fcsvOut.write(   AO_lTokens[3] + "~")
                                        AO_fcsvOut.write(   AO_lTokens[8] + "\n")

                                        AO_lLexicon.append([AO_lTokens[8],[AO_lTokens[0] ,  float(AO_lTokens[2])*5 , (-5) *  float(AO_lTokens[3])]])

                                        if len(AO_lTokens) > 11:    
                                            if AO_lTokens[11].isdigit():
                                                AO_fcsvOut.write( AO_lTokens[0] + "~")
                                                AO_fcsvOut.write( AO_lTokens[2] + "~")
                                                AO_fcsvOut.write( AO_lTokens[3] + "~")
                                                AO_fcsvOut.write( AO_lTokens[10] + "\n")

                                                AO_lLexicon.append([AO_lTokens[10],[AO_lTokens[0] ,  float(AO_lTokens[2])*5 , (-5) *  float(AO_lTokens[3])]])

                                                if len(AO_lTokens) > 13:    
                                                    if AO_lTokens[13].isdigit():
                                                        AO_fcsvOut.write(AO_lTokens[0] + "~")
                                                        AO_fcsvOut.write(AO_lTokens[2] + "~")
                                                        AO_fcsvOut.write(AO_lTokens[3] + "~")
                                                        AO_fcsvOut.write(AO_lTokens[12] + "\n")

                                                        AO_lLexicon.append([AO_lTokens[12],[AO_lTokens[0] ,  float(AO_lTokens[2])*5 , (-5) *  float(AO_lTokens[3])]])
                                
    # convert teh tupple into a dictionary
    AO_dLexicon = dict(AO_lLexicon)

    # store the dictionary
    pickle.dump( AO_dLexicon, AO_fpklOut )
    
    AO_fpklOut.close
    AO_fcsvOut.close
    AO_fInput.close
if __name__ == '__main__':
   
    main()
