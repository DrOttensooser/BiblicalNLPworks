import re
# from array import *
# import icu
import unicodedata
import numpy            # available from http://www.lfd.uci.edu/~gohlke/pythonlibs/#numpy
from scipy import stats #                http://www.lfd.uci.edu/~gohlke/pythonlibs/#scipy
                        #                http://cran.r-project.org/bin/windows/base/
import string
from decimal import *

# the following is needed to import rpy
# install pywin http://sourceforge.net/projects/pywin32/files/pywin32/Build%20217/pywin32-217.win32-py2.7.exe/download
import sys
sys.path.append(r'C:\Program Files\R\R-2.12.1') # only r-2.12.1 
sys.path.append(r'C:\Python27\Lib\site-packages\win32')
import os
os.environ['RHOME']=(r'C:\Program Files\R\R-2.12.1')
from rpy import *      # available from http://sourceforge.net/projects/rpy/files/rpy/
r.library('lattice')
# r.library('ggplot2')

import codecs

import urllib

def main():

    
    codecs.BOM = codecs.BOM_UTF16_LE # The x86 platform is little-endian.

    AO_sAppVersion = '8'

    AO_fAcceptabePValue = 0.9849999

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
    WorkFileOut1     =  AO_sCompelationSite + 'Data\\CSV\\Matching Pairs.CSV'
    WorkFileOut2     =  AO_sCompelationSite + 'Data\\CSV\\Book  Chapter R summary.CSV'
    AO_sGraphDir     =  AO_sCompelationSite + 'Graphs\\'


    sys.path.append(AO_ModulesPass)
    import AO_mBookLoader
    
    # TODO check that the folder AO_sCompelationSite + 'Data\\CSV\\' exists
    
    AO_fOutput1  = codecs.open(WorkFileOut1,'w', encoding='utf-16')
    AO_fOutput1.write('Book A ~ Chapter A ~ Book B ~ Chapter B ~ P Value ~ statistic ' + '\n')
    AO_fOutput2  = codecs.open(WorkFileOut2,'w', encoding='utf-16'+ '\n')
    AO_fOutput2.write('Book  , Chapter, R summary')

    # these list will include only one chapter
    AO_lJchapter = []
    AO_lIchapter = []
    AO_lHchapter = []

    # for all the books in the J Bible    
    for AO_iJBook in range (0,len(AO_tBooks)):

        AO_sJBook = AO_tBooks[AO_iJBook][0]
        A0_iLastJBookChapter = AO_tBooks[AO_iJBook][2]
        AO_mJBookChapterXwords = AO_mBookLoader.AO_fLoadBook(AO_sJBook,AO_tBooks[AO_iJBook][1],A0_iLastJBookChapter,AO_tBooks[AO_iJBook][3])

        # for all the chapters in the J Bible
        for AO_iJChapter in range(1,A0_iLastJBookChapter +1):

            # clear the J list
            for m in range (1, len(AO_lJchapter)):
                n=AO_lJchapter.pop(1)

            k = 1    
            # find the non zero length words in the j chapter
            while AO_mJBookChapterXwords[AO_iJChapter][k] > 0:
                AO_lJchapter.append(int(AO_mJBookChapterXwords[AO_iJChapter][k]))
                k = k+1
                
            # call the R summary function to describe the J chapter. There is no summary of the I Chaptears as they are redundent
            AO_sJChapterSummary = r.summary(AO_lJchapter)

            # allow printing the graph for the first time.
            # if we ommit this variable, we get empty graphs
            AO_bPrintJGrapgh = 1
            AO_fOutput2.write(str(AO_iJBook) + "," + AO_sJBook + "," + str(AO_iJChapter) + "," +  str(AO_sJChapterSummary)  + '\n')




            # Here we compare all theAO_lHchapter chapters in the J book that follow the AO_iJChapter
            for AO_iHChapter in range(AO_iJChapter + 1,A0_iLastJBookChapter +1):

                # clear the H list
                for m in range (1, len(AO_lHchapter)):
                   n=AO_lHchapter.pop(1)
                # end for

                k = 1    
                # find the non zero length words in the H chapter
                while AO_mJBookChapterXwords[AO_iHChapter][k] > 0:
                    AO_lHchapter.append(int(AO_mJBookChapterXwords[AO_iHChapter][k]))
                    k = k+1
                # end while


                # Here we do statistical comparison of the H and J chapters

                # test for the mean
                b = r.wilcox_test(AO_lJchapter,AO_lHchapter,alternative="t",paired=0, exact = 0)
                # extract the data from the string R returned
                AO_sStatistic = "%.4f" % b['statistic']['W']
                AO_sP_value = "%.5f" % b['p.value']

                # store potential metches       
                if (1 > float(AO_sP_value) > float(AO_fAcceptabePValue)):
                    # as a paired
                    AO_fOutput1.write(AO_sJBook + '~' + str(AO_iJChapter) + '~' + AO_sJBook +'~'+ str(AO_iHChapter) +  '~' + str(AO_sP_value) + '~' + str(AO_sStatistic) + '\n')

                    AO_sHeader = AO_sJBook + ' ' + str(AO_iJChapter) + ' and ' + AO_sJBook + ' ' +str (AO_iHChapter) + " P Value = " + str(AO_sP_value)

                    # Debuging statement
                    print AO_sHeader

                    # Turn off the graph printing
                    if 1==1:  

                        # Otherwise the J book will be printed with every H and I book
                        if (AO_bPrintJGrapgh == 1):

                            # Open the R PNG driver
                            AO_sHeader = AO_sJBook + ' ' + str(AO_iJChapter)  
                            r.png(AO_sGraphDir + AO_sHeader +'.png',width=4*280,height=4*200)
                            r.par(mfrow=[4,4], pch=16)

                            r.hist(AO_lJchapter,r.seq(0, 12, 1), prob=1,col="red",main=  AO_sJBook +  ' Chapter ' + str(AO_iJChapter) ,xlab="number of characters in word")
                            AO_bPrintJGrapgh = 0
                            r.rug(AO_lJchapter)
                        #end if
                            
                        r.hist(AO_lHchapter,r.seq(0, 12, 1), prob=1,col="lightgreen"       ,main=  AO_sJBook +  ' Chapter ' + str(AO_iHChapter) + " P Value = " + str(AO_sP_value),xlab="number of characters in word")

                        
                        r.rug(AO_lHchapter)

                        
                    # End if graphs printing
                # end if - the P value is good enouph
            # end of the comparison of the chapters in the J book that follow t AO_iJChapter

            # The inner loop is also on all of the chpaters in all of the books in the bible
            # for all the books in the I Bible (Note we skip the reviewd books
            for AO_iIBook in range (AO_iJBook + 1 ,len(AO_tBooks)):
                AO_sIBook = AO_tBooks[AO_iIBook][0]
                A0_iLastIBookChapter = AO_tBooks[AO_iIBook][2]
                AO_mIBookChapterXwords = AO_mBookLoader.AO_fLoadBook(AO_sIBook,AO_tBooks[AO_iIBook][1],A0_iLastIBookChapter,AO_tBooks[AO_iIBook][3])

                # for all the chapters in the I book
                for AO_iIChapter in range(1,A0_iLastIBookChapter +1):

                    # ###########################################################
                    # This is the inermost part of the four times nested for loop
                    # ###########################################################
            
                    # clear the I list
                    for m in range (1, len(AO_lIchapter)):
                        n=AO_lIchapter.pop(1)
                    # end for    

                    k = 1    
                    # find the non zero length words in the j chapter
                    while AO_mIBookChapterXwords[AO_iIChapter][k] > 0:
                        AO_lIchapter.append(int(AO_mIBookChapterXwords[AO_iIChapter][k]))
                        k = k+1
                    # end while

                    # test for the mean
                    b = r.wilcox_test(AO_lJchapter,AO_lIchapter,alternative="t",paired=0, exact = 0)
                    # extract the data from the string R returned
                    AO_sStatistic = "%.4f" % b['statistic']['W']
                    AO_sP_value = "%.5f" % b['p.value']

                    # store potential metches       
                    if (1 > float(AO_sP_value) > float(AO_fAcceptabePValue)):
                        # as a paired
                        AO_fOutput1.write(AO_sJBook + '~' + str(AO_iJChapter) + '~' + AO_sIBook +'~'+ str(AO_iIChapter) +  '~' + str(AO_sP_value) + '~' + str(AO_sStatistic) + '\n')

                        AO_sHeader = AO_sJBook + ' ' + str(AO_iJChapter) + ' and ' + AO_sIBook + ' ' +str (AO_iIChapter) + " P Value = " + str(AO_sP_value)

                        # Debuging statement
                        print AO_sHeader

                        # Turn off the graph printing
                        if 1==1:  
                            # We need this if statemnt, otherwise the J book will be printed with every H and I book
                            if (AO_bPrintJGrapgh == 1):

                                # Open the R PNG driver
                                AO_sHeader = AO_sJBook + ' ' + str(AO_iJChapter)  
                                r.png(AO_sGraphDir + AO_sHeader +'.png',width=4*280,height=4*200)
                                r.par(mfrow=[4,4], pch=16)
                                
                                r.hist(AO_lJchapter,r.seq(0, 12, 1), prob=1,col="red"       ,main=  AO_sJBook +  ' Chapter ' + str(AO_iJChapter) ,xlab="number of characters in word")
                                AO_bPrintJGrapgh = 0
                                r.rug(AO_lJchapter)
                            #end if   

                            r.hist(AO_lIchapter,r.seq(0, 12, 1), prob=1,col="lightgreen",main=  AO_sIBook +  ' Chapter ' + str(AO_iIChapter) + " P Value = " + str(AO_sP_value),xlab="number of characters in word")
                            r.rug(AO_lIchapter)  
                        # End if graphs printing
                    # end if the P value is good enouph
                # For all of the I Chapters
            # For all of the I books
            
            # close the R PNG driver, if a graph was printed
            if (AO_bPrintJGrapgh == 0):
                r.dev_off()
            # enf if    
            
        # for all of the J chapters
    # for all of the J Books
    
    # Close the global shared files
    AO_fOutput1.close()
    AO_fOutput2.close()
    
if __name__ == '__main__':
   
    main()
