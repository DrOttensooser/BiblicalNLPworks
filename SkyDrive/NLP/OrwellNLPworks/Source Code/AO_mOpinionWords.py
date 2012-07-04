'# -*- coding: utf-8 -*-'
from __future__ import division
'''
This compares the topmost popolar words in the first Doccumente to al other Doccuments.
'''
__author__ = 'Dr Avner OTTENSOOSER <avner.ottensooser@gmail.com>'
__version__ = '$Revision: 1 $'

import re
import AO_mShakespeareWorksCommon

# home folder
AO_sCompelationSite = 'C:\\Users\\Avner\\SkyDrive\\NLP\\TicketNLPWorks\\'
# Calculate the name of the files
AO_sModulesPath        =  AO_sCompelationSite + 'Source Code'
AO_sPlainTextPath      =  AO_sCompelationSite + 'Data\\Plain Text\\'
AO_sOpinionFolder      =  AO_sCompelationSite + 'Data\\Opion-Lexicon-English\\'
AO_sPostiveWordsFile   =  AO_sOpinionFolder   + 'positive-words.txt'
AO_sNegativeWordsFile  =  AO_sOpinionFolder   + 'negative-words.txt'
AO_sNegationWordsFile  =  AO_sOpinionFolder   + 'negation-words.txt'
AO_sEmphasiseWordsFile =  AO_sOpinionFolder   + 'emphasise-words.txt'

# regular expression used to add space at the end of some words
s = re.compile(r'~')

# This will load list of negation words (no not ...)
AO_lNegationWords = []
AO_fInput = open(AO_sNegationWordsFile)
for line in AO_fInput:
    # remove whight space
    line = line.strip().lower()
    if len(line) > 0:
        if line[0] <> ";":
            line = s.sub(' ', line) #Add space at the end of a word ending with tilda ~
            AO_lNegationWords.append(line)
AO_fInput.close
#AO_setNegationWords = set ( AO_lNegationWords)
print str(len(AO_lNegationWords)) + " negation words loaded from " + AO_sNegationWordsFile



# This will load list of emphsaise words (very extrimimly ...)
AO_lEmphasisWords  = []
AO_fInput = open(AO_sEmphasiseWordsFile)
for line in AO_fInput:
    # remove whight space
    line = line.strip().lower()
    if len(line) > 0:
        if line[0] <> ";":
            line = s.sub(' ', line) #Add space at the end of a word ending with tilda ~
            AO_lEmphasisWords.append(line)
AO_fInput.close
#AO_setEmphasisWords = set ( AO_lEmphasisWords)
print str(len(AO_lEmphasisWords)) + " emphasis words loaded from " + AO_sEmphasiseWordsFile

# This will load list of positive words
AO_lPositiveWords = []
AO_fInput = open(AO_sPostiveWordsFile)
for line in AO_fInput:
    # remove whight space
    line = line.strip().lower()
    if len(line) > 0:
        if line[0] <> ";":
            AO_lPositiveWords.append(line)
AO_fInput.close
AO_setPositiveWords = set ( AO_lPositiveWords)

print str(len(AO_setPositiveWords)) + " positive words loaded from " + AO_sPostiveWordsFile

# This will load list of negative words
AO_lNegativeWords = []
AO_fInput = open(AO_sNegativeWordsFile)
for line in AO_fInput:
    # remove whight space
    line = line.strip().lower()
    if len(line) > 0:
        if line[0] <> ";":
            AO_lNegativeWords.append(line)
AO_fInput.close
AO_setNegativeWords = set ( AO_lNegativeWords)

print str(len(AO_lNegativeWords)) + " Negative words loaded from " + AO_sNegativeWordsFile

'''
This function
Input   - A document
Process - Lookup of all the words in the document within the positive and negative word lists
Output  - An array with Percent Pocitive Words
                        Percent Negative Words
                        Some of the above
                        Simmery line with the above percents and tagged list of all the opionion words in teh documents 

        
'''

def AO_lAssessOpinion (AO_sDocument,AO_sDocumentName,AO_sDocumentsType):

    # print AO_sDocument
    
    AO_lOpinion=[0,0,"","",""]
    AO_iPosWords = 0
    AO_iNegWords = 0
    AO_sLine = ""
    
    # we only work with lower case
    AO_sDocument=AO_sDocument.lower()
    
    # break the document into individual words (tokenize)
    AO_lTokens = AO_mShakespeareWorksCommon.AO_lTokenize(AO_sDocument)

    # for all the individual words in the document
    for j in range(0, len(AO_lTokens)):
        
        # if the word is a positive word
        if AO_lTokens[j] in AO_setPositiveWords:
            AO_bNegationFound  = False # the word was not found to be negated, yet
            AO_bEmphasiseFound = False # the word was not found to be emphasised yet
            
            # see if the privious word negated the j word
            if j > 0: # is these is a privious word at all
                
                # now we try all the negation words
                
                for k in range (0,len(AO_lNegationWords)):
                       
                    # now we check for "Not good". Note that the negation word may have a space so unimpresive will also be caught
                    if AO_lNegationWords[k] + AO_lTokens[j] == AO_lTokens[j-1] + AO_lTokens[j]:
                        AO_iNegWords = AO_iNegWords + 1 # a negation of a positive word is negative
                        AO_sLine = AO_sLine + 'notP: ' + AO_lNegationWords[k] + AO_lTokens[j] +' ~ '
                        AO_bNegationFound = True
                        break
                    
                    #endif word was negated
                    
                #end for all the negation words
                    
                # now we try all the emphasise words
                
                for k in range (0,len(AO_lEmphasisWords)):
                    
                    # now we check for "Very good". Note that the negation word may have a space so unimpresive will also be caught
                    if AO_lEmphasisWords[k] + AO_lTokens[j] == AO_lTokens[j-1] + AO_lTokens[j]:
                        AO_iPosWords = AO_iPosWords + 2 # double the scoring
                        AO_sLine = AO_sLine + 'emphP: ' + AO_iPosWords[k] + AO_lTokens[j] +' ~ '
                        AO_bEmphasiseFound = True
                        break
                    
                    # endif word was emphasied
                    
                # end for all the possible emphasise words
            
            # if the positve word was not negated
            
            if (AO_bNegationFound == False)  and (AO_bEmphasiseFound == False):
                AO_iPosWords = AO_iPosWords + 1
                AO_sLine = AO_sLine + 'P: ' + AO_lTokens[j] +' ~ '
                
             # endif - word was not emphasised or negated
                        
        # endif positive  word
        
        # if the word is a negative words
        if AO_lTokens[j] in AO_lNegativeWords:
            
            # now we chceck word pairs, starting ofcourse with the second word
            AO_bNegationFound   = False # the word was not found to be negated, yet
            AO_bEmphasiseFound = False # the word was not found to be emphasised yet
            if j > 0:
                
                # now we try all the negation words
                
                for k in range (0,len(AO_lNegationWords)):
                    
                    # now we check for "Not bad". Note that the negation word may have a space so unexpiring will also be caught
                    if AO_lNegationWords[k] + AO_lTokens[j] == AO_lTokens[j-1] + AO_lTokens[j]:
                        AO_iPosWords = AO_iPosWords + 1 # not bad is positive
                        AO_sLine = AO_sLine + 'notN: ' + AO_lNegationWords[k] + AO_lTokens[j] +' ~ '
                        AO_bNegationFound = True
                        break
                    
                    #endif word was negated
                    
                #end for all the negation words
                    
                # now we try all the emphasise words
               
                for k in range (0,len(AO_lEmphasisWords)):
                    
                    # now we check for "Very good". Note that the negation word may have a space so unimpresive will also be caught
                    if AO_lEmphasisWords[k] + AO_lTokens[j] == AO_lTokens[j-1] + AO_lTokens[j]:
                        AO_iNegWords = AO_iNegWords + 2 # double the scoring
                        AO_sLine = AO_sLine + 'emphN: ' + AO_iPosWords[k] + AO_lTokens[j] +' ~ '
                        AO_bEmphasiseFound = True
                        break
                    
                   # end if word was emphasied
                    
                # end for all the emphasise words
                    
            # if the negative word was not negated    
            if (AO_bNegationFound == False) and (AO_bEmphasiseFound == False):
                AO_iNegWords = AO_iNegWords + 1
                AO_sLine = AO_sLine + 'N: ' + AO_lTokens[j] +' ~ '
            
            # endif - word was not emphasised or negated
        
        # endif negarive word
        
    # for all the words in the document
    
    if len(AO_lTokens) > 0:
        
        a =  ( AO_iPosWords / len(AO_lTokens))*100
        b =  (-AO_iNegWords / len(AO_lTokens))*100
        c = a+ b
        
        AO_lOpinion=[a,b,c,AO_sLine]
                     
    return AO_lOpinion 
    
# end of function
