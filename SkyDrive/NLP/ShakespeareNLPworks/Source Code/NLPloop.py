'# -*- coding: utf-8 -*-'
from __future__ import division
'''
This module alalyses Shakespeare's Sonnets
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
AO_sCompelationSite = 'C:\\Users\\Avner\\SkyDrive\\NLP\\ShakespeareNLPworks\\'


# Calculate the name of the files
AO_sModulesPath      =  AO_sCompelationSite + 'Source Code'
AO_sPlainTextPath    =  AO_sCompelationSite + 'Data\\Plain Text\\'
AO_s10ersFileName    =  AO_sCompelationSite + 'Data\\CSV\\10ers.CSV'
AO_s10erGraphsFolde  =  AO_sCompelationSite +'Graphs\\10ers\\'
AO_sGraphsPass       =  AO_sCompelationSite +'Graphs\\Volcublary comparison\\'
AO_iLastSonette = 154

import AO_mShakespeareWorksCommon 

def main():

    # Clear the 10ers file
    if  os.path.exists(AO_s10ersFileName):
        os.remove(AO_s10ersFileName)

    # ##############################
    # Graph 1 - Lingusitc Diversity#
    # ##############################

    # This will include one floating point element per one chapter
    AO_lLigusticDiversity = []

    # for all the sonnetes
    for j in range(1,AO_iLastSonette):

        # this  will include all the words in one Sonnete
        AO_sSonette = ""
        
        AO_sRoman      = AO_mShakespeareWorksCommon.Arab2Roman(j)
        AO_sSonnetTXT  = AO_sPlainTextPath + str(j) + ' Sonnet_' + AO_sRoman + '.txt'
        print AO_sRoman

        # Opens the already downloaded sonette
        AO_fInput    = codecs.open(AO_sSonnetTXT,  'r', encoding='utf-8')

        # for all the lines in the sonnete 
        for line in AO_fInput:
            # remove whight space
            line = line.strip()
            AO_sSonette = AO_sSonette + line + " "
        # for all the lines in each sonnete
    
        # summerise the sonnete 
        # load the text sonnete NLTK
        tokens = nltk.word_tokenize(AO_sSonette)
        text = nltk.Text(tokens)
        # find the texttual diversity
        vocab = set(text)
        vocab_size = len(vocab)
        if len(set(text)) > 0: 
            AO_lLigusticDiversity.append(len(text)/len(set(text)))
        AO_fInput.close
    # for all the Sonnets

    


    AO_fMean = r.mean(AO_lLigusticDiversity)
    AO_fSd = r.sd(AO_lLigusticDiversity)
    # plot a triangle for each Sonnet's linguistic diversity
    # No 0 Sonnet 
    x = np.arange(1, len(AO_lLigusticDiversity)+1, 1);
    y = AO_lLigusticDiversity

    

    # Analyse the vecror for 10ers
    AO_l10erStart = AO_mShakespeareWorksCommon.AO_lMTLookForLowPobabilirty(y,"Sonnets",'Linguistic Divercity',AO_fMean,AO_s10ersFileName)

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

    

    plt.ylabel( 'Linguistic Divercity' )
    plt.xlabel( 'Sonnets' )

    plt.title('Shakespeare Sonnets')

    plt.grid(True)
    AO_sPlotFile = AO_sGraphsPass + "Shakespeare Sonnets " + ' 1 Linguistic Divercity.png'
 
    plt.savefig(AO_sPlotFile)
    plt.close()

    '''
    if AO_l10erStart[0] > 0:
        shutil.copyfile(AO_sPlotFile,AO_s10ersGraphsPass + "Shakespeare Sonnets " + ' 1 Linguistic Divercity.png'


    '''

if __name__ == '__main__':
   
    main()
