'# -*- coding: utf-8 -*-'
from __future__ import division

'''
This module includes routines that are shared by the NLPShakespeareWorks project
'''
__author__ = 'Dr Avner OTTENSOOSER <avner.ottensooser@gmail.com>'
__version__ = '$Revision: 0.01 $'


from curses.ascii import isdigit # http://www.lfd.uci.edu/~gohlke/pythonlibs/#pyicu
import json
import sys
import datetime
# import re

from django.utils.datastructures import SortedDict # http://www.lfd.uci.edu/~gohlke/pythonlibs/#django
from django.contrib.localflavor.us.us_states import STATE_CHOICES
from nltk import sent_tokenize, regexp_tokenize
from nltk.corpus import cmudict

def AO_lTokenize(AO_sText):

    '''
    Thid function gets a text as uts input and breakes it into a list of words.
    It is adapted From Natural Language Processing with Python
    '''

    regex = r'''(?xi)
    (?:H|S)\.\ ?(?:(?:J|R)\.\ )?(?:Con\.\ )?(?:Res\.\ )?\d+ # Bills
  | ([A-Z]\.)+                                              # Abbreviations (U.S.A., etc.)
  | ([A-Z]+\&[A-Z]+)                                        # Internal ampersands (AT&T, etc.)
  | (Mr\.|Dr\.|Mrs\.|Ms\.)                                  # Mr., Mrs., etc.
  | \d*\.\d+                                                # Numbers with decimal points.
  | \d\d?:\d\d                                              # Times.
  | \$?[,\.0-9]+\d                                          # Numbers with thousands separators, (incl currency).
  | (((a|A)|(p|P))\.(m|M)\.)                                # a.m., p.m., A.M., P.M.
  | \w+((-|')\w+)*                                          # Words with optional internal hyphens.
  | \$?\d+(\.\d+)?%?                                        # Currency and percentages.
  | (?<=\b)\.\.\.(?=\b)                                     # Ellipses surrounded by word borders
  | [][.,;"'?():-_`]
    '''
    # Strip punctuation from this one; solr doesn't know about any of it
    AO_lTokens = regexp_tokenize(AO_sText, regex)
    # tokens = [re.sub(r'[.,?!]', '', token) for token in tokens]  # instead of this we just test word length
    return AO_lTokens


def Arab2Roman(AO_iArab):

    '''
        Convert Arab numeral to Roman Numeral.
        Based on snippet in http://www.daniweb.com/software-development/python/code/216865/roman-numerals-python
    '''
    
    numerals = { 1 : "I", 4 : "IV", 5 : "V", 9 : "IX", 10 : "X", 40 : "XL",50 : "L", 90 : "XC", 100 : "C", 400 : "CD", 500 : "D", 900 : "CM", 1000 : "M" }
    AO_sRoman = ''
    for value, numeral in sorted(numerals.items(), reverse=True):
        while AO_iArab >= value:
            AO_sRoman = AO_sRoman + numeral
            AO_iArab = AO_iArab - value
    return AO_sRoman

def AO_lMTLookForLowPobabilirty(AO_lVector,AO_sBook,AO_sLable,AO_fMean,AO_s10ersFileName):
# Input   - Statistic vector,Book name,Statistic Name. Statistic avarage
# Process - Scan for 10 or more elements above or below the avarage
# Otput  - A record for each 10er. 
    AO_l10erStart = [-1,-1]   
    # do not bother looking for 10ers in small books
    if len(AO_lVector) > 10:
        AO_i10erCount = 0
        AO_sPriviousReading = 'Above Avarage'
        for i in range(0,len(AO_lVector)):
            if AO_sPriviousReading == "Above Avarage":
                if (AO_lVector[i] >= AO_fMean):  
                   AO_i10erCount = AO_i10erCount +1
                else:
                    if AO_i10erCount >= 10:
                        AO_fCSV = open(AO_s10ersFileName,'a')
                        AO_fCSV.write( AO_sBook + " 2 ~ " + AO_sLable + " ~ " + str(AO_i10erCount) + " ~ " + str(i-AO_i10erCount) + " ~ " + str(i) + " ~ " + str(AO_fMean) + "\n")
                        AO_fCSV.close()
                        AO_l10erStart = [i-AO_i10erCount + 2,i]
                    AO_i10erCount = 1
                    AO_sPriviousReading = "Below Avarage"
                
            else: # if the privious point was below avarage
                if (AO_lVector[i] <= AO_fMean):
                    AO_i10erCount = AO_i10erCount +1
                
                else:
                    if AO_i10erCount >= 10:
                        AO_fCSV = open(AO_s10ersFileName,'a')
                        AO_fCSV.write( AO_sBook + " 2 ~ " + AO_sLable + " ~ " + str(AO_i10erCount) + " ~ " + str(i-AO_i10erCount) + " ~ " + str(i) + " ~ " + str(AO_fMean) + "\n")
                        AO_fCSV.close()
                        AO_l10erStart = [i-AO_i10erCount + 2,i]
                    AO_i10erCount = 1
                    AO_sPriviousReading = "Above Avarage"
            # end if
        # end for 
        # this capture a 10er that lasts until the last chapter       
        if AO_i10erCount >= 10:
            AO_fCSV = open(AO_s10ersFileName,'a')
            AO_fCSV.write( AO_sBook + " 2 ~ " + AO_sLable + " ~ " + str(AO_i10erCount) + " ~ " + str(i-AO_i10erCount) + " ~ " + str(i) + " ~ " + str(AO_fMean) + "\n")
            AO_fCSV.close()  
            AO_l10erStart = [i-AO_i10erCount + 2,i]
    # print AO_l10erStart        
    return AO_l10erStart
