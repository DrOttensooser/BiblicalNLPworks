'# -*- coding: utf-8 -*-'
from __future__ import division
'''
This module alalyses Shakespeare's Essays
The module should be called after actibvating the module GatherFiles.PY
'''
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
AO_sCompelationSite = 'C:\\Users\\Avner\\SkyDrive\\NLP\\OrwellNLPworks\\'
# Calculate the name of the files
AO_sModulesPath      =  AO_sCompelationSite + 'Source Code'
AO_sModulesPath      =  AO_sCompelationSite + 'Source Code'
AO_sPlainTextPath    =  AO_sCompelationSite + 'Data\\Plain Text\\'
AO_s10ersFileName    =  AO_sCompelationSite + 'Data\\CSV\\10ers.CSV'
AO_s10erGraphsFolde  =  AO_sCompelationSite + 'Graphs\\10ers\\'
AO_sGraphsPass       =  AO_sCompelationSite + 'Graphs\\Volcublary comparison\\'
AO_iLastEssay = 50

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

    # for all the Essayes
    for j in range(1,AO_iLastEssay):

        # this  will include all the words in one Essaye
        AO_sEssay = ""     
        AO_sEssayTXT  = AO_sPlainTextPath + 'o' + str(j) + '.txt'

        # Opens the already downloaded Essay
        AO_fInput    = codecs.open(AO_sEssayTXT,  'r', encoding='utf-8')

        # for all the lines in the Essaye 
        for line in AO_fInput:
            # remove whight space
            line = line.strip()
            AO_sEssay = AO_sEssay + line + " "
           
        # summerise the Essaye 
        # load the text Essaye NLTK
        
        tokens = nltk.word_tokenize(AO_sEssay)
        text = nltk.Text(tokens)
        # find the texttual diversity
        vocab = set(text)
        vocab_size = len(vocab)
        if len(set(text)) > 0: 
            AO_lLigusticDiversity.append(len(text)/len(set(text)))
        AO_fInput.close
    # for all the Essays

    


    AO_fMean = r.mean(AO_lLigusticDiversity)
    AO_fSd = r.sd(AO_lLigusticDiversity)
    # plot a triangle for each Essay's linguistic diversity
    # No 0 Essay 
    x = np.arange(1, len(AO_lLigusticDiversity)+1, 1);
    y = AO_lLigusticDiversity

    # Analyse the vecror for 10ers
    AO_l10erStart = AO_mShakespeareWorksCommon.AO_lMTLookForLowPobabilirty(y,"Essays",AO_sLable,AO_fMean,AO_s10ersFileName)

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
    plt.xlabel( 'Essays' )

    plt.title('Orwell Essays')

    plt.grid(True)
    AO_sPlotFile = AO_sGraphsPass + "50  Essays by Orwell " + ' 1 ' + AO_sLable+ '.png'
 
    plt.savefig(AO_sPlotFile)
    plt.close()

    '''
    if AO_l10erStart[0] > 0:
        shutil.copyfile(AO_sPlotFile,AO_s10ersGraphsPass + "50  Essays by Orwell " + ' 1 Linguistic Divercity.png'


    '''


    # ##################################
    # Graph 2                          #
    AO_sLable = 'Vocabulaty Commomality'
    # ##################################

    # This will include one floating point element per one chapter
    AO_lVocabulatyCommomality = AO_mPopularWords.AO_fPopularWords (AO_iLastEssay)

    
    AO_fMean = r.mean(AO_lVocabulatyCommomality)
    AO_fSd = r.sd(AO_lVocabulatyCommomality)
    # plot a triangle for each Essay's linguistic diversity
    # No 0 Essay 
    x = np.arange(1, len(AO_lVocabulatyCommomality)+1, 1);
    y = AO_lVocabulatyCommomality
    #the first Essay is by definition 100, so we ignore it
    x[0] = AO_fMean
    

    # Analyse the vecror for 10ers
    #AO_l10erStart = AO_mShakespeareWorksCommon.AO_lMTLookForLowPobabilirty(y,"Essays",'Linguistic Divercity',AO_fMean,AO_s10ersFileName)

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
    plt.xlabel( 'Essays' )

    plt.title('50  Essays by Orwell')

    plt.grid(True)
    AO_sPlotFile = AO_sGraphsPass + "50  Essays by Orwell " + ' 2 ' + AO_sLable +'.png'
 
    plt.savefig(AO_sPlotFile)
    plt.close()

    '''
    if AO_l10erStart[0] > 0:
        shutil.copyfile(AO_sPlotFile,AO_s10ersGraphsPass + "50  Essays by Orwell " + ' 1 Linguistic Divercity.png'


    '''


    # #######################
    # Graph 3
    AO_sLable = 'Grade Level'
    # #######################

    # This will include one floating point element per one chapter
    AO_lGradeLevel = []

    # for all the Essayes
    for j in range(1,AO_iLastEssay):


        AO_sEssayTXT  = AO_sPlainTextPath + 'o' + str(j) +  '.txt'
        AO_sEssay = ''

        # Opens the already downloaded Essay
        AO_fInput    = codecs.open(AO_sEssayTXT,  'r', encoding='utf-8')

        # for all the lines in the Essaye 
        for line in AO_fInput:
            # remove whight space
            line = line.strip()
            AO_sEssay = AO_sEssay + line + " "

        #Calculate the grade level of the Essaye
        AO_lTemp = AO_mGradeDocumentReadability.AO_fGradeDocument(AO_sEssay)
        print AO_lTemp
        if len(AO_lTemp) > 0:
            AO_lGradeLevel.append(AO_lTemp[5][1])
        else:
            AO_lGradeLevel.append(14)
        AO_fInput.close
    # for all the Essays

    


    AO_fMean = r.mean(AO_lGradeLevel)
    AO_fSd = r.sd(AO_lGradeLevel)
    # plot a triangle for each Essay's linguistic diversity
    # No 0 Essay 
    x = np.arange(1, len(AO_lGradeLevel)+1, 1);
    y = AO_lGradeLevel

    # Analyse the vecror for 10ers
    #AO_l10erStart = AO_mShakespeareWorksCommon.AO_lMTLookForLowPobabilirty(y,"Essays",AO_sLable,AO_fMean,AO_s10ersFileName)

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
    plt.xlabel( 'Essays' )

    plt.title('50  Essays by Orwell')

    plt.grid(True)
    AO_sPlotFile = AO_sGraphsPass + "50  Essays by Orwell " + ' 3 ' +AO_sLable +'.png'
 
    plt.savefig(AO_sPlotFile)
    plt.close()

    '''
    if AO_l10erStart[0] > 0:
        shutil.copyfile(AO_sPlotFile,AO_s10ersGraphsPass + "50  Essays by Orwell " + ' 1 Linguistic Divercity.png'


    '''

    # #######################
    # Graph 4
    AO_sLable = 'Reading Ease'
    # #######################

    # This will include one floating point element per one chapter
    AO_lGradeLevel = []

    # for all the Essayes
    for j in range(1,AO_iLastEssay):

        # this  will include all the words in one Essaye
        AO_sEssayTXT  = AO_sPlainTextPath + 'o' + str(j) +  '.txt'
        AO_sEssay = ''

        # Opens the already downloaded Essay
        AO_fInput    = codecs.open(AO_sEssayTXT,  'r', encoding='utf-8')

        # for all the lines in the Essaye 
        for line in AO_fInput:
            # remove whight space
            line = line.strip()
            AO_sEssay = AO_sEssay + line + " "

        #Calculate the grade level of the Essaye
        AO_lTemp = AO_mGradeDocumentReadability.AO_fGradeDocument(AO_sEssay)
        if len(AO_lTemp) > 0:
            AO_lGradeLevel.append(AO_lTemp[6][1])
        else:
            AO_lGradeLevel.append(50)
        AO_fInput.close
    # for all the Essays

    


    AO_fMean = r.mean(AO_lGradeLevel)
    AO_fSd = r.sd(AO_lGradeLevel)
    # plot a triangle for each Essay's linguistic diversity
    # No 0 Essay 
    x = np.arange(1, len(AO_lGradeLevel)+1, 1);
    y = AO_lGradeLevel

    # Analyse the vecror for 10ers
    #AO_l10erStart = AO_mShakespeareWorksCommon.AO_lMTLookForLowPobabilirty(y,"Essays",AO_sLable,AO_fMean,AO_s10ersFileName)

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
    plt.xlabel( 'Essays' )

    plt.title('50  Essays by Orwell')

    plt.grid(True)
    AO_sPlotFile = AO_sGraphsPass + "50  Essays by Orwell " + ' 3 ' +AO_sLable +'.png'
 
    plt.savefig(AO_sPlotFile)
    plt.close()

    '''
    if AO_l10erStart[0] > 0:
        shutil.copyfile(AO_sPlotFile,AO_s10ersGraphsPass + "50  Essays by Orwell " + ' 1 Linguistic Divercity.png'


    '''

if __name__ == '__main__':
   
    main()
