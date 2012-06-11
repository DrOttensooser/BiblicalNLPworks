# Author: Dr. Avner OTTENSOOSER
# Copyrights: Creative Commons
import sys
import numpy as np
import matplotlib.pyplot as plt
from rpy import *
def main():

    # Book Taple = Nice Name, Short Name, Last Chapter, Last verse in the last chapter

    # TODO - put this in a database

    AO_tBooks=[('Genesis',      'Gen',        50,26),
               ('Exodus',       'Ex',         40,38),
               ('Leviticus',    'Lev',        27,34),
               ('Numbers',      'Num',        36,13),
               ('Deuteronomy',  'Deut',       34,12),
               ('Joshua',       'Josh',       24,33),
               ('Judges',       'Judg',       21,25),
               ('Samuel 1',     '1 Sam',     31,13),
               ('Samuel 2',     '2 Sam',     24,24),
               ('Kings 1',      '1 Kings',   22,54),
               ('Kings 2',      '2 Kings',   22,54),
               ('Isaia',        'Isa',        66,24),
               ('Jeremiah',     'Jer',        52,34),
               ('Ezekiel',      'Ezek',       48,35),
               ('Hosea',        'Hos',        14,10),
               ('Joel',         'Joel',        4,21),
               ('Amos',         'Am',          9,15),
               ('Obadiah',      'Ob',          1,21),
               ('Jonah',        'Jon',         4,11),
               ('Micah',        'Mic',         7,20),
               ('Nahum',        'Nah',         3,19),
               ('Habakkuk',     'Hab',         3,19),
               ('Zephaniah',    'Zeph',        3,20),
               ('Haggai',       'Hag',         2,23),
               ('Zechariah',    'Zech',       14,21),
               ('Malachi',      'Mal',         3,24),
               ('Psalms',       'Ps',         150,6),
               ('Proverbs',     'Prov',       31,22),
               ('Job',          'Job',        42,17),
               ('Song of Songs','Song',        8,14),
               ('Ruth',         'Ruth',        4,22),
               ('Lamentations', 'Lam',         5,22),
               ('Ecclesiastes', 'Eccl',       12,14),
               ('Esther',       'Esth',       10,3),
               ('Daniel',       'Dan',        12,13),
               ('Ezra',         'Ezra',       10,44),
               ('Nehemiah',     'Neh',        13,31),
               ('Chronicles 1', '1 Chr',      29,30),
               ('Chronicles 2', '2 Chr',      36,23)
              ]              

    # home folder
    AO_sCompelationSite = 'C:\\Users\\Avner\\SkyDrive\\NLP\\BiblicalNLPworks\\'

    # Calculate the name of the files
    AO_ModulesPass   =  AO_sCompelationSite + 'Source Code'

    sys.path.append(AO_ModulesPass)
    import AO_mNLTK, AO_mPopularWords


    # for all the books in the J Bible    
    for AO_iJBook in range (0,len(AO_tBooks)):

        AO_sJBook = AO_tBooks[AO_iJBook][0]
        A0_iLastJBookChapter = AO_tBooks[AO_iJBook][2]
        print(AO_sJBook)
        AO_lLigusticDiversity = AO_mNLTK.AO_fNLP(AO_sJBook,AO_tBooks[AO_iJBook][1],A0_iLastJBookChapter,AO_tBooks[AO_iJBook][3])
        AO_lCommonWordUsage = AO_mPopularWords.AO_fPopularWords(AO_sJBook,AO_tBooks[AO_iJBook][1],A0_iLastJBookChapter,AO_tBooks[AO_iJBook][3])
        # for l in range (0, len( AO_lLigusticDiversity)):
        #    print str(AO_lLigusticDiversity[l]) + " "
        #print "\n"


        #########################################
        # Graph 1
        #########################################

        if AO_lLigusticDiversity > 1:
            AO_fSd = r.sd(AO_lLigusticDiversity)
        else:
            AO_lLigusticDiversity = 0
            
        AO_fMean = r.mean(AO_lLigusticDiversity)

        # plot a triangle for each chapter's linguistic diversity
        # No 0 chapter 
        x = np.arange(1, len(AO_lLigusticDiversity)+1, 1);
        y = AO_lLigusticDiversity
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


        plt.legend([fig1, fig2,fig3,fig4], ["Chapter", "mean","mean+2sd","mean-2sd"])
        
        plt.ylabel( 'Linguistic Divercity' )
        plt.xlabel( 'Chapter' )
        plt.title(AO_sJBook)
        plt.grid(True)
        AO_sPlotFile = 'C:\\Users\\Avner\\SkyDrive\\NLP\\BiblicalNLPworks\\Graphs\\' + AO_sJBook + ' Linguistic Divercity.png'
        plt.savefig(AO_sPlotFile)
        plt.close()



        #########################################
        # Graph 2
        #########################################
        
        if len(AO_lCommonWordUsage) > 1:
            AO_fSd = r.sd(AO_lCommonWordUsage[1:len(AO_lCommonWordUsage)])
        else:
            AO_fSd = 0
            
        AO_fMean = r.mean(AO_lCommonWordUsage[1:len(AO_lCommonWordUsage)])

        # if we leave it at 400 it will bdly effect the graph
        AO_lCommonWordUsage[0] = AO_fMean 

        # plot a triangle for each chapter's linguistic diversity
        # No 0 chapter 
        x = np.arange(1, len(AO_lCommonWordUsage)+1, 1);
        y = AO_lCommonWordUsage
        fig1, = plt.plot(x, y, 's')

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


        plt.legend([fig1, fig2,fig3,fig4], ["Chapter", "mean","mean+2sd","mean-2sd"])
        
        plt.ylabel( 'Vocabulaty Commomality' )
        plt.xlabel( 'Chapter' )
        plt.title(AO_sJBook)
        plt.grid(True)
        AO_sPlotFile = 'C:\\Users\\Avner\\SkyDrive\\NLP\\BiblicalNLPworks\\Graphs\\' + AO_sJBook + ' Vocabulaty Commomality .png'
        plt.savefig(AO_sPlotFile)
        plt.close()



        #########################################
        # sub Graph 3
        #########################################

        AO_lLigusticDiversity = AO_mNLTK.AO_fNLP(AO_sJBook,AO_tBooks[AO_iJBook][1],A0_iLastJBookChapter,AO_tBooks[AO_iJBook][3])


        plt.figure(1)
        plt.subplot(211)

        if len(AO_lLigusticDiversity) > 1:
            AO_fSd = r.sd(AO_lLigusticDiversity)
        else:
            AO_fSd = 0
            
        AO_fMean = r.mean(AO_lLigusticDiversity)

        # plot a triangle for each chapter's linguistic diversity
        # No 0 chapter 
        x = np.arange(1, len(AO_lLigusticDiversity)+1, 1);
        y = AO_lLigusticDiversity
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


        plt.legend([fig1, fig2,fig3,fig4], ["Chapter", "mean","mean+2sd","mean-2sd"])
        
        plt.ylabel( 'Linguistic Divercity' )
        # plt.xlabel( 'Chapter' )
        plt.title(AO_sJBook)
        plt.grid(True)
        # AO_sPlotFile = 'C:\\Users\\Avner\\SkyDrive\\NLP\\BiblicalNLPworks\\Graphs\\' + AO_sJBook + ' Linguistic Divercity.png'
        # plt.savefig(AO_sPlotFile)
        # plt.close()



        #########################################
        # sub Graph 4
        #########################################

        AO_lCommonWordUsage = AO_mPopularWords.AO_fPopularWords(AO_sJBook,AO_tBooks[AO_iJBook][1],A0_iLastJBookChapter,AO_tBooks[AO_iJBook][3])

        plt.subplot(212)

        if len(AO_lCommonWordUsage) > 1:
            AO_fSd = r.sd(AO_lCommonWordUsage[1:len(AO_lCommonWordUsage)])
        else:
            AO_fSd = 0
            
        AO_fMean = r.mean(AO_lCommonWordUsage[1:len(AO_lCommonWordUsage)])

        # if we leave it at 400 it will bdly effect the graph
        AO_lCommonWordUsage[0] = AO_fMean 

        # plot a triangle for each chapter's linguistic diversity
        # No 0 chapter 
        x = np.arange(1, len(AO_lCommonWordUsage)+1, 1);
        y = AO_lCommonWordUsage
        fig1, = plt.plot(x, y, 's')

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


        plt.legend([fig1, fig2,fig3,fig4], ["Chapter", "mean","mean+2sd","mean-2sd"])
        
        plt.ylabel( 'Vocabulaty Commomality' )
        plt.xlabel( 'Chapter' )
        # plt.title(AO_sJBook)
        plt.grid(True)
        AO_sPlotFile = 'C:\\Users\\Avner\\SkyDrive\\NLP\\BiblicalNLPworks\\Graphs\\' + AO_sJBook + '-NLTK.png'
        plt.savefig(AO_sPlotFile)
        plt.close()

        
    # for all of the J Books
    
if __name__ == '__main__':
   
    main()
