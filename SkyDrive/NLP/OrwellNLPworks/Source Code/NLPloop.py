'# -*- coding: utf-8 -*-'
from __future__ import division

''' This module alalyses Shakespeare's Documents The module should be called after
actibvating the module GatherFiles.PY '''

__author__ = 'Dr Avner OTTENSOOSER <avner.ottensooser@gmail.com>'
__version__ = '$Revision: 0.01 $'

AO_ROOT_PATH         =  'C:\\Users\\Avner\\SkyDrive\\NLP\\'
AO_PROJECT_NAME      =  'OrwellNLPworks'
AO_DOCUMENT_NAME     =  "50 Essayss by Orwell"
AO_DOCUMENT_TYPE     =  "Essay"
AO_LAST_DOCUMENT     =  51

AO_sCommonPath       =  AO_ROOT_PATH + 'CommonWorks\\'
AO_sCommonCode       =  AO_sCommonPath + 'Source Code'
AO_sCompelationSite  =  AO_ROOT_PATH + AO_PROJECT_NAME + '\\'
AO_sModulesPath      =  AO_sCompelationSite + 'Source Code'
AO_sPlainTextPath    =  AO_sCompelationSite + 'Data\\Plain Text\\'
AO_s10ersFileName    =  AO_sCompelationSite + 'Data\\CSV\\10ers.CSV'
AO_s10erGraphsFolde  =  AO_sCompelationSite + 'Graphs\\10ers\\'
AO_sGraphsPass       =  AO_sCompelationSite + 'Graphs\\Volcublary comparison\\'
AO_sCSVfolder        =  AO_sCompelationSite + 'Data\\CSV\\'

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

import sys
sys.path.append(AO_sCommonCode)
import AO_mOpinionWords
import AO_mCommon 
import AO_mGradeDocumentReadability
import AO_mPopularWords
import AO_mShakespeareWorksCommon



def main():

    # Clear the 10ers file
    if  os.path.exists(AO_s10ersFileName):
        os.remove(AO_s10ersFileName)

    # ###############################
    # Graph 1 -
    AO_sLable = 'Lingusitc Diversity'
    # ###############################

    AO_sCSVfile = AO_sCSVfolder + AO_DOCUMENT_NAME + "-" + AO_sLable + ".CSV"
    AO_fCSV = codecs.open(AO_sCSVfile,   'w', encoding='utf-8')
    # write the header of the CSV file
    AO_fCSV.write(AO_DOCUMENT_TYPE + ' ~ ')
    AO_fCSV.write(AO_sLable)
    AO_fCSV.write('\n')

    # This will include one floating point element per one chapter
    AO_lLigusticDiversity = []

    # for all the Documentes
    for j in range(1,AO_LAST_DOCUMENT+1):

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

            # write the CSV file
            AO_fCSV.write(str(j) + ' ~ ')
            AO_fCSV.write(str(len(text)/len(set(text))) + ' ~ ')
            AO_fCSV.write('\n')
            
        

    


    AO_fMean = r.mean(AO_lLigusticDiversity)
    AO_fSd = r.sd(AO_lLigusticDiversity)
    # plot a triangle for each Document's linguistic diversity
    # No 0 Document 
    x = np.arange(1, AO_LAST_DOCUMENT +1, 1);
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
    plt.xlabel( AO_DOCUMENT_TYPE )

    plt.title(AO_DOCUMENT_NAME)

    plt.grid(True)
    AO_sPlotFile = AO_sGraphsPass + AO_DOCUMENT_NAME + ' 1 ' + AO_sLable+ '.png'
 
    plt.savefig(AO_sPlotFile)
    plt.close()
    AO_fInput.close()
    AO_fCSV.close()
    '''
    if AO_l10erStart[0] > 0:
        shutil.copyfile(AO_sPlotFile,AO_s10ersGraphsPass + AO_DOCUMENT_NAME + ' 1 Linguistic Divercity.png'


    '''


    # ##################################
    # Graph 2                          #
    AO_sLable = 'Vocabulaty Commomality'
    # ##################################

    print AO_DOCUMENT_NAME + " "  + AO_sLable

    AO_sCSVfile = AO_sCSVfolder + AO_DOCUMENT_NAME + "-" + AO_sLable + ".CSV"
    AO_fCSV = codecs.open(AO_sCSVfile,   'w', encoding='utf-8')
    # write the header of the CSV file
    AO_fCSV.write(AO_DOCUMENT_TYPE + ' ~ ')
    AO_fCSV.write(AO_sLable)
    AO_fCSV.write('\n')
    
    # This will include one floating point element per one chapter
    AO_lVocabulatyCommomality = []
    AO_lVocabulatyCommomality = AO_mPopularWords.AO_fPopularWords (AO_LAST_DOCUMENT,AO_DOCUMENT_NAME,AO_DOCUMENT_TYPE,AO_ROOT_PATH)

    # write the CSV file
    for k in range (0,len(AO_lVocabulatyCommomality)):
        AO_fCSV.write(str(k) + ' ~ ')
        AO_fCSV.write(str(AO_lVocabulatyCommomality[k]) + ' ~ ')
        AO_fCSV.write('\n')
     
    
    AO_fMean = r.mean(AO_lVocabulatyCommomality)
    
    #the first Document is by definition 100, so we ignore it otherwise the 100 will effevt the graph
    AO_lVocabulatyCommomality[0] = AO_fMean 
    AO_fSd = r.sd(AO_lVocabulatyCommomality)

    # plot a triangle for each Document's linguistic diversity
    # No 0 Document 
    x = np.arange(1, AO_LAST_DOCUMENT +1, 1);
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
    plt.xlabel( AO_DOCUMENT_TYPE )

    plt.title(AO_DOCUMENT_NAME)

    plt.grid(True)
    AO_sPlotFile = AO_sGraphsPass + AO_DOCUMENT_NAME + ' 2 ' + AO_sLable +'.png'
 
    plt.savefig(AO_sPlotFile)
    plt.close()
    AO_fInput.close()
    AO_fCSV.close()
    '''
    if AO_l10erStart[0] > 0:
        shutil.copyfile(AO_sPlotFile,AO_s10ersGraphsPass + AO_DOCUMENT_NAME + ' 1 Linguistic Divercity.png'


    '''


    # ######################################
    # Graph 3
    AO_sLable = 'Flesch Kincaid Grade level'
    # ######################################

    print AO_DOCUMENT_NAME + " "  + AO_sLable

    AO_sCSVfile = AO_sCSVfolder + AO_DOCUMENT_NAME + "-" + AO_sLable + ".CSV"
    AO_fCSV = codecs.open(AO_sCSVfile,   'w', encoding='utf-8')

    # This will include one floating point element per one chapter
    AO_lGradeLevel = []

    # for all the Documentes
    for j in range(1,AO_LAST_DOCUMENT +1):
       

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

            # write the CSV file    
            
            if j==1:
                # write the header of the CSV file
                AO_fCSV.write(AO_DOCUMENT_TYPE + ' ~ ')
                for k in range (0, len(AO_lTemp)):
                    AO_fCSV.write(AO_lTemp[k][0] + ' ~ ')
                AO_fCSV.write('\n')

            # write the spreadsheet line    
            AO_fCSV.write(str(j) + ' ~ ')          
            for k in range (0, len(AO_lTemp)):
                AO_fCSV.write(str(AO_lTemp[k][1]) + ' ~ ')
            AO_fCSV.write('\n')
            
        else:
            AO_lGradeLevel.append(14)
    # for all the Documents
 

    AO_fMean = r.mean(AO_lGradeLevel)
    AO_fSd = r.sd(AO_lGradeLevel)
    # plot a triangle for each Document's linguistic diversity
    # No 0 Document 
    x = np.arange(1, AO_LAST_DOCUMENT +1, 1);
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
    plt.xlabel( AO_DOCUMENT_TYPE )

    plt.title(AO_DOCUMENT_NAME)

    plt.grid(True)
    AO_sPlotFile = AO_sGraphsPass + AO_DOCUMENT_NAME + ' 3 ' +AO_sLable +'.png'
 
    plt.savefig(AO_sPlotFile)

    plt.close()
    AO_fInput.close()
    AO_fCSV.close()
    '''
    if AO_l10erStart[0] > 0:
        shutil.copyfile(AO_sPlotFile,AO_s10ersGraphsPass + AO_DOCUMENT_NAME + ' 1 Linguistic Divercity.png'


    '''

    # #######################
    # Graph 4
    AO_sLable = 'Reading Ease'
    # #######################

    print AO_DOCUMENT_NAME + " "  + AO_sLable

    # This will include one floating point element per one chapter
    AO_lGradeLevel = []

    # for all the Documentes
    for j in range(1,AO_LAST_DOCUMENT +1):

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
    # for all the Documents

    


    AO_fMean = r.mean(AO_lGradeLevel)
    AO_fSd = r.sd(AO_lGradeLevel)
    # plot a triangle for each Document's linguistic diversity
    # No 0 Document 
    x = np.arange(1, AO_LAST_DOCUMENT +1, 1);
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
    plt.xlabel( AO_DOCUMENT_TYPE )

    plt.title(AO_DOCUMENT_NAME)

    plt.grid(True)
    AO_sPlotFile = AO_sGraphsPass + AO_DOCUMENT_NAME + ' 4 ' +AO_sLable +'.png'
 
    plt.savefig(AO_sPlotFile)
    plt.close()
    AO_fInput.close()
    AO_fCSV.close()
    '''
    if AO_l10erStart[0] > 0:
        shutil.copyfile(AO_sPlotFile,AO_s10ersGraphsPass + AO_DOCUMENT_NAME + ' 1 Linguistic Divercity.png'


    '''



    # ############################
    # Graph 5
    AO_sLable = 'Opinions Analysis'
    # #############################

    print AO_DOCUMENT_NAME + " "  + AO_sLable

    AO_sCSVfile = AO_sCSVfolder + AO_DOCUMENT_NAME + "-" + AO_sLable + ".CSV"
    AO_fCSV = codecs.open(AO_sCSVfile,   'w', encoding='utf-8')
    # write the header of the CSV file
    AO_fCSV.write(AO_DOCUMENT_TYPE + ' ~ Pos ~ Neg ~ Sum ~ Terms: ~')
    AO_fCSV.write(AO_sLable)
    AO_fCSV.write('\n')
    
    AO_lPoitives = []
    AO_lNegatives = []
    AO_lNet = []
   
    

    # for all the Documentes
    for j in range(1,AO_LAST_DOCUMENT +1):

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

        AO_lOpinion = AO_mOpinionWords.AO_lAssessOpinion(AO_sDocument)

        AO_lPoitives.append(AO_lOpinion[0])
        AO_lNegatives.append(AO_lOpinion[1])
        AO_lNet.append(AO_lOpinion[2])

        AO_fCSV.write(str(j) + ' ~ ' + str(AO_lOpinion[0]) + ' ~ ' + str(AO_lOpinion[1]) + ' ~ ' + str(AO_lOpinion[2]) + ' ~ ' + AO_lOpinion[3])
        AO_fCSV.write('\n')
        

    
    


    AO_fMean = r.mean(AO_lNet)  
    AO_fSd = r.sd(AO_lNet)
    # plot a triangle for each Document's linguistic diversity
    # No 0 Document 
    x = np.arange(1, AO_LAST_DOCUMENT +1, 1);
    y = AO_lPoitives

    # Analyse the vecror for 10ers
    #AO_l10erStart = AO_mShakespeareWorksCommon.AO_lMTLookForLowPobabilirty(y,"Documents",AO_sLable,AO_fMean,AO_s10ersFileName)

    # if there are 10ers
    #if AO_l10erStart[0] > 0:
    #    fig10erA, = plt.plot([AO_l10erStart[0],AO_l10erStart[0]], [r.min(AO_lGradeLevel),r.max(AO_lLigusticDiversity)])
    #    fig10erB, = plt.plot([AO_l10erStart[1],AO_l10erStart[1]], [r.min(AO_lGradeLevel),r.max(AO_lGradeLevel)])

    # plot!
    figP, = plt.plot(x, y, 'm^') # Magenta  triangle_up

    y = AO_lNegatives
    figN, = plt.plot(x, y, 'gv') # Green  triangle_down

    y = AO_lNet

    figM, = plt.plot(x, y, 'kx') # Black Xs

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
    plt.xlabel( AO_DOCUMENT_TYPE )

    plt.title(AO_DOCUMENT_NAME)

    plt.grid(True)
    AO_sPlotFile = AO_sGraphsPass + AO_DOCUMENT_NAME + ' 5 ' +AO_sLable +'.png'
 
    plt.savefig(AO_sPlotFile)
    plt.close()
    AO_fInput.close()
    AO_fCSV.close()
if __name__ == '__main__':
   
    main()
