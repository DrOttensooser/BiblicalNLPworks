'# -*- coding: utf-8 -*-'
from __future__ import division

''' This module alalyses Shakespeare's Documents The module should be called after
actibvating the module GatherFiles.PY '''

__author__ = 'Dr Avner OTTENSOOSER <avner.ottensooser@gmail.com>'
__version__ = '$Revision: 0.01 $'

import urllib
import os.path
import re
import codecs
import os
import nltk
import rpy
import numpy as np
import matplotlib.pyplot as plt
import shutil
from rpy import *

# home folder
AO_sCompelationSite =   'C:\\Users\\Avner\\SkyDrive\\NLP\\OrwellNLPworks\\'
AO_sDocumentName     =  "50 Essayss by Orwell"
AO_sDocumentsType    =  "Essays"
AO_iLastDocument        =  50

# Calculate the name of the files
AO_sModulesPath      =  AO_sCompelationSite + 'Source Code'
AO_sModulesPath      =  AO_sCompelationSite + 'Source Code'
AO_sPlainTextPath    =  AO_sCompelationSite + 'Data\\Plain Text\\'
AO_s10ersFileName    =  AO_sCompelationSite + 'Data\\CSV\\10ers.CSV'
AO_s10erGraphsFolde  =  AO_sCompelationSite + 'Graphs\\10ers\\'
AO_sGraphsPass       =  AO_sCompelationSite + 'Graphs\\Volcublary comparison\\'


import AO_mShakespeareWorksCommon , AO_mGradeDocumentReadability, AO_mPopularWords

def main():

    # Clear the 10ers file
    if  os.path.exists(AO_s10ersFileName):
        os.remove(AO_s10ersFileName)

    # ###############################
    # Graph 1 -
    AO_sLable = 'Lingusitc Diversity'
    # ###############################

    # This will include one floating point element per one chapter
    AO_lLigusticDiversity = []

    # for all the Documentes
    for j in range(1,AO_iLastDocument+1):

        # this  will include all the words in one Documente
        AO_sDocument = ""     
        AO_sDocumentTXT  = AO_sPlainTextPath + 'o' + str(j) + '.txt'

        # Opens the already downloaded Document
        AO_fInput    = codecs.open(AO_sDocumentTXT,  'r', encoding='utf-8')

        # for all the lines in the Documente 
        for line in AO_fInput:
            # remove whight space
            line = line.strip()
            AO_sDocument = AO_sDocument + line + " "
           
        # summerise the Documente 
        # load the text Documente NLTK
        
        tokens = nltk.word_tokenize(AO_sDocument)
        text = nltk.Text(tokens)
        # find the texttual diversity
        vocab = set(text)
        vocab_size = len(vocab)
        if len(set(text)) > 0: 
            AO_lLigusticDiversity.append(len(text)/len(set(text)))
        AO_fInput.close
    # for all the Documents

    


    AO_fMean = r.mean(AO_lLigusticDiversity)
    AO_fSd = r.sd(AO_lLigusticDiversity)
    # plot a triangle for each Document's linguistic diversity
    # No 0 Document 
    x = np.arange(1, AO_iLastDocument +1, 1);
    y = AO_lLigusticDiversity

    # Analyse the vecror for 10ers
    AO_l10erStart = AO_mShakespeareWorksCommon.AO_lMTLookForLowPobabilirty(y,"Documents",AO_sLable,AO_fMean,AO_s10ersFileName)

    # if there are 10ers
    if AO_l10erStart[0] > 0:
        fig10erA, = plt.plot([AO_l10erStart[0],AO_l10erStart[0]], [r.min(AO_lLigusticDiversity),r.max(AO_lLigusticDiversity)])
        fig10erB, = plt.plot([AO_l10erStart[1],AO_l10erStart[1]], [r.min(AO_lLigusticDiversity),r.max(AO_lLigusticDiversity)])

    # plot!
    fig1, = plt.plot(x, y, 'g^')

    # plot a line at the mean
    for m in range (0, len(x)):
        y[m]=AO_fMean
    fig2, = plt.plot(x, y)

    
    # plot upper control  line at two standard deviations
    for m in range (0, len(x)):
        y[m]=2*AO_fSd + AO_fMean
    fig3, =plt.plot(x, y)

     

    #  plot lower control  line at two standard deviations
    for m in range (0, len(x)):
        y[m] = AO_fMean - 2*AO_fSd 
    fig4, = plt.plot(x, y)

    

    plt.ylabel( AO_sLable )
    plt.xlabel( AO_sDocumentsType )

    plt.title(AO_sDocumentName)

    plt.grid(True)
    AO_sPlotFile = AO_sGraphsPass + AO_sDocumentName + ' 1 ' + AO_sLable+ '.png'
 
    plt.savefig(AO_sPlotFile)
    plt.close()

    '''
    if AO_l10erStart[0] > 0:
        shutil.copyfile(AO_sPlotFile,AO_s10ersGraphsPass + AO_sDocumentName + ' 1 Linguistic Divercity.png'


    '''


    # ##################################
    # Graph 2                          #
    AO_sLable = 'Vocabulaty Commomality'
    # ##################################

    # This will include one floating point element per one chapter
    AO_lVocabulatyCommomality = []
    AO_lVocabulatyCommomality = AO_mPopularWords.AO_fPopularWords (AO_iLastDocument)
    
    AO_fMean = r.mean(AO_lVocabulatyCommomality)
    
    #the first Document is by definition 100, so we ignore it otherwise the 100 will effevt the graph
    AO_lVocabulatyCommomality[0] = AO_fMean 
    AO_fSd = r.sd(AO_lVocabulatyCommomality)

    # plot a triangle for each Document's linguistic diversity
    # No 0 Document 
    x = np.arange(1, AO_iLastDocument +1, 1);
    y = AO_lVocabulatyCommomality

    
    

    # Analyse the vecror for 10ers
    #AO_l10erStart = AO_mShakespeareWorksCommon.AO_lMTLookForLowPobabilirty(y,"Documents",'Linguistic Divercity',AO_fMean,AO_s10ersFileName)

    # if there are 10ers
    #if AO_l10erStart[0] > 0:
    #    fig10erA, = plt.plot([AO_l10erStart[0],AO_l10erStart[0]], [r.min(AO_lLigusticDiversity),r.max(AO_lLigusticDiversity)])
    #    fig10erB, = plt.plot([AO_l10erStart[1],AO_l10erStart[1]], [r.min(AO_lLigusticDiversity),r.max(AO_lLigusticDiversity)])

    # plot!
    fig1, = plt.plot(x, y, 'g^')

    # plot a line at the mean
    for m in range (0, len(x)):
        y[m]=AO_fMean
    fig2, = plt.plot(x, y)

    
    # plot upper control  line at two standard deviations
    for m in range (0, len(x)):
        y[m]=2*AO_fSd + AO_fMean
    fig3, =plt.plot(x, y)

     

    #  plot lower control  line at two standard deviations
    for m in range (0, len(x)):
        y[m] = AO_fMean - 2*AO_fSd 
    fig4, = plt.plot(x, y)

    

    plt.ylabel( AO_sLable )
    plt.xlabel( AO_sDocumentsType )

    plt.title(AO_sDocumentName)

    plt.grid(True)
    AO_sPlotFile = AO_sGraphsPass + AO_sDocumentName + ' 2 ' + AO_sLable +'.png'
 
    plt.savefig(AO_sPlotFile)
    plt.close()

    '''
    if AO_l10erStart[0] > 0:
        shutil.copyfile(AO_sPlotFile,AO_s10ersGraphsPass + AO_sDocumentName + ' 1 Linguistic Divercity.png'


    '''


    # #######################
    # Graph 3
    AO_sLable = 'Grade Level'
    # #######################

    # This will include one floating point element per one chapter
    AO_lGradeLevel = []

    # for all the Documentes
    for j in range(1,AO_iLastDocument +1):


        AO_sDocumentTXT  = AO_sPlainTextPath + 'o' + str(j) +  '.txt'
        AO_sDocument = ''

        # Opens the already downloaded Document
        AO_fInput    = codecs.open(AO_sDocumentTXT,  'r', encoding='utf-8')

        # for all the lines in the Documente 
        for line in AO_fInput:
            # remove whight space
            line = line.strip()
            AO_sDocument = AO_sDocument + line + " "

        #Calculate the grade level of the Documente
        AO_lTemp = AO_mGradeDocumentReadability.AO_fGradeDocument(AO_sDocument)
        if len(AO_lTemp) > 0:
            AO_lGradeLevel.append(AO_lTemp[5][1])
        else:
            AO_lGradeLevel.append(14)
        AO_fInput.close
    # for all the Documents

    


    AO_fMean = r.mean(AO_lGradeLevel)
    AO_fSd = r.sd(AO_lGradeLevel)
    # plot a triangle for each Document's linguistic diversity
    # No 0 Document 
    x = np.arange(1, AO_iLastDocument +1, 1);
    y = AO_lGradeLevel

    # Analyse the vecror for 10ers
    #AO_l10erStart = AO_mShakespeareWorksCommon.AO_lMTLookForLowPobabilirty(y,"Documents",AO_sLable,AO_fMean,AO_s10ersFileName)

    # if there are 10ers
    #if AO_l10erStart[0] > 0:
    #    fig10erA, = plt.plot([AO_l10erStart[0],AO_l10erStart[0]], [r.min(AO_lGradeLevel),r.max(AO_lLigusticDiversity)])
    #    fig10erB, = plt.plot([AO_l10erStart[1],AO_l10erStart[1]], [r.min(AO_lGradeLevel),r.max(AO_lGradeLevel)])

    # plot!
    fig1, = plt.plot(x, y, 'g^')

    # plot a line at the mean
    for m in range (0, len(x)):
        y[m]=AO_fMean
    fig2, = plt.plot(x, y)

    
    # plot upper control  line at two standard deviations
    for m in range (0, len(x)):
        y[m]=2*AO_fSd + AO_fMean
    fig3, =plt.plot(x, y)

     

    #  plot lower control  line at two standard deviations
    for m in range (0, len(x)):
        y[m] = AO_fMean - 2*AO_fSd 
    fig4, = plt.plot(x, y)

    

    plt.ylabel( AO_sLable )
    plt.xlabel( AO_sDocumentsType )

    plt.title(AO_sDocumentName)

    plt.grid(True)
    AO_sPlotFile = AO_sGraphsPass + AO_sDocumentName + ' 3 ' +AO_sLable +'.png'
 
    plt.savefig(AO_sPlotFile)
    plt.close()

    '''
    if AO_l10erStart[0] > 0:
        shutil.copyfile(AO_sPlotFile,AO_s10ersGraphsPass + AO_sDocumentName + ' 1 Linguistic Divercity.png'


    '''

    # #######################
    # Graph 4
    AO_sLable = 'Reading Ease'
    # #######################

    # This will include one floating point element per one chapter
    AO_lGradeLevel = []

    # for all the Documentes
    for j in range(1,AO_iLastDocument +1):

        # this  will include all the words in one Documente
        AO_sDocumentTXT  = AO_sPlainTextPath + 'o' + str(j) +  '.txt'
        AO_sDocument = ''

        # Opens the already downloaded Document
        AO_fInput    = codecs.open(AO_sDocumentTXT,  'r', encoding='utf-8')

        # for all the lines in the Documente 
        for line in AO_fInput:
            # remove whight space
            line = line.strip()
            AO_sDocument = AO_sDocument + line + " "

        #Calculate the grade level of the Documente
        AO_lTemp = AO_mGradeDocumentReadability.AO_fGradeDocument(AO_sDocument)
        if len(AO_lTemp) > 0:
            AO_lGradeLevel.append(AO_lTemp[6][1])
        else:
            AO_lGradeLevel.append(50)
        AO_fInput.close
    # for all the Documents

    


    AO_fMean = r.mean(AO_lGradeLevel)
    AO_fSd = r.sd(AO_lGradeLevel)
    # plot a triangle for each Document's linguistic diversity
    # No 0 Document 
    x = np.arange(1, AO_iLastDocument +1, 1);
    y = AO_lGradeLevel

    # Analyse the vecror for 10ers
    #AO_l10erStart = AO_mShakespeareWorksCommon.AO_lMTLookForLowPobabilirty(y,"Documents",AO_sLable,AO_fMean,AO_s10ersFileName)

    # if there are 10ers
    #if AO_l10erStart[0] > 0:
    #    fig10erA, = plt.plot([AO_l10erStart[0],AO_l10erStart[0]], [r.min(AO_lGradeLevel),r.max(AO_lLigusticDiversity)])
    #    fig10erB, = plt.plot([AO_l10erStart[1],AO_l10erStart[1]], [r.min(AO_lGradeLevel),r.max(AO_lGradeLevel)])

    # plot!
    fig1, = plt.plot(x, y, 'g^')

    # plot a line at the mean
    for m in range (0, len(x)):
        y[m]=AO_fMean
    fig2, = plt.plot(x, y)

    
    # plot upper control  line at two standard deviations
    for m in range (0, len(x)):
        y[m]=2*AO_fSd + AO_fMean
    fig3, =plt.plot(x, y)

     

    #  plot lower control  line at two standard deviations
    for m in range (0, len(x)):
        y[m] = AO_fMean - 2*AO_fSd 
    fig4, = plt.plot(x, y)

    

    plt.ylabel( AO_sLable )
    plt.xlabel( AO_sDocumentsType )

    plt.title(AO_sDocumentName)

    plt.grid(True)
    AO_sPlotFile = AO_sGraphsPass + AO_sDocumentName + ' 3 ' +AO_sLable +'.png'
 
    plt.savefig(AO_sPlotFile)
    plt.close()

    '''
    if AO_l10erStart[0] > 0:
        shutil.copyfile(AO_sPlotFile,AO_s10ersGraphsPass + AO_sDocumentName + ' 1 Linguistic Divercity.png'


    '''

if __name__ == '__main__':
   
    main()
