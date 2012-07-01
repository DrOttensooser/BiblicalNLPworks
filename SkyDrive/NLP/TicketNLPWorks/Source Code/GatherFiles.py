'# -*- coding: utf-8 -*-'

'''
This module analyses a XML like files with ticket information.
We analyse the document charcter by charcter.
The reson we do not use a tidy XML routine is that we suspect that the XML is not legal.
'''

__author__ = 'Dr Avner OTTENSOOSER <avner.ottensooser@gmail.com>'
__version__ = '$Revision: 0.01 $'

import urllib
import os.path
import re
import codecs
from nltk.tokenize import word_tokenize
import AO_mOpinionWords

# home folder
AO_sCompelationSite = 'C:\\Users\\Avner\\SkyDrive\\NLP\\OrwellNLPworks\\'

AO_sPlainTextPath = 'C:\\\Users\\Avner\\SkyDrive\\NLP\\TicketNLPWorks\\Data\\Text\\'
# ensure that the Plain Text  folder exists
if not os.path.exists(AO_sPlainTextPath):
    os.makedirs(AO_sPlainTextPath)

AO_sCSVPath = 'C:\\\Users\\Avner\\SkyDrive\\NLP\\TicketNLPWorks\\Data\\CSV\\'
# ensure that the Plain Text  folder exists
if not os.path.exists(AO_sCSVPath):
    os.makedirs(AO_sCSVPath)

AO_sSource     = 'C:\\\Users\\Avner\\SkyDrive\\NLP\\TicketNLPWorks\\Data\\XML\\CustomerNotes.xml'
AO_sProcessed  = AO_sCSVPath + 'CustomerNotes.CSV'


# Calculate the name of the files
#AO_sModulesPath   =  AO_sCompelationSite + 'Source Code'
#AO_sHTMLPath =  AO_sCompelationSite + 'Data\\HTML\\'
#AO_sEssayHTML = AO_sHTMLPath +'50OrwelAssays'

# regular expression used to remove HTML symbols
s = re.compile(r'&.*?;')


def AO_bProcessXMLexpression(AO_sXMLexpression, AO_iLevel, AO_sOut):
        
        # remove HTML symbols
        AO_sXMLexpression = s.sub(' ', AO_sXMLexpression)

        # remove spaces at the begining and end of the expression
        AO_sXMLexpression = AO_sXMLexpression.strip()

        # initiate the state machine
        AO_sState =''
        AO_bExpressionStarted=False
        AO_FieldType = -1
        
        if AO_sXMLexpression <> '':
            
            # use nltk to break the expression into words    
            AO_sStatement = word_tokenize(AO_sXMLexpression)

            # for all the words in the expression
            for i in range (0, len(AO_sStatement)):

                # An if ... elif ... elif ... sequence is a substitute for the switch or case statements found in other languages
                
                if AO_sStatement[i]=='CRISPProduction.dbo.account':
                    AO_AO_sState = 'Account'
                    
                elif AO_sStatement[i]=='\CRISPProduction.dbo.account':
                    AO_AO_sState = 'Start'

                # Here we capture field names    
                elif (AO_sStatement[i]<>"''") and (AO_bExpressionStarted==False):

                    if AO_sStatement[i] == "CompanyName=":
                        AO_FieldType = 0
                        #AO_sOut.write( "CompanyName ~ ") 

                    elif AO_sStatement[i] == "ID=":
                        AO_FieldType = 1
                        AO_sOut.write( "ID ~ ~ ~" )

                    elif AO_sStatement[i] == "Description=":
                         AO_sOut.write("Description ~ ")
                         AO_FieldType = 2

                    elif AO_sStatement[i] == "Severity=":
                        AO_sOut.write("Severity ~ ~ ~")
                        AO_FieldType = 3

                    elif AO_sStatement[i] == "PAAAO_TicketCategoryLOB=":
                        #AO_sOut.write("LOB ~ ")
                        AO_FieldType = 4

                    elif AO_sStatement[i] == "PAAAO_TicketNoteNoteDate=":
                        #AO_sOut.write("NoteDate ~ ")
                        AO_FieldType = 5

                    elif AO_sStatement[i] == "DiaryNote=":
                        AO_sOut.write("DiaryNote ~ ")
                        AO_FieldType = 6

                    elif AO_sStatement[i] == "PAAAO_TicketAccountAO_id=":
                        #AO_sOut.write("AccountAO_id ~ ")
                        AO_FieldType = 7

                    elif AO_sStatement[i] == "TicketDate=":
                        #AO_sOut.write("TicketDate ~ ")
                        AO_FieldType = 8

                    #else:
                        #AO_sOut.write( AO_sStatement[i] )
                        
                
                #is this the first word in an expression?
                elif (AO_sStatement[i]=="''") and (AO_bExpressionStarted==False):
                    AO_bExpressionStarted=True
                    AO_sExprssion = ""

                # is this just any word within the expression
                elif (AO_bExpressionStarted==True) and (AO_sStatement[i]<>"''"):
                    AO_sExprssion = AO_sExprssion + AO_sStatement[i] + " "

                #is this the last word in an expression?
                elif (AO_sStatement[i]=="''") and (AO_bExpressionStarted==True):

                    AO_bExpressionStarted=False

                    #DiaryNote or  Description
                    if  (AO_FieldType in [2,6]): # Description or DiaryNote
                        AO_lOpinion = AO_mOpinionWords.AO_lAssessOpinion(AO_sExprssion,"","")
                        AO_sOut.write( str(AO_lOpinion[0]) + "%~")
                        AO_sOut.write( str(AO_lOpinion[1]) + "%~")
                        AO_sOut.write( unicode(AO_sExprssion, errors='ignore') +'~')
                        AO_sOut.write( str(AO_lOpinion[3]) +'\n') # list the positive and negative words

                    elif (AO_FieldType in [1,3]): # if it is severity or ID
                        AO_sOut.write( "  " + AO_sExprssion +'\n') # the extra space will force excel to think that the ID is string

                    AO_sExprssion = ''
                    
        return ''

def main():

    AO_iIndet = 0
    AO_sPhrase = ''

    AO_fInput    = open(AO_sSource,  'r')
    AO_fOut      = codecs.open(AO_sProcessed,   'w', encoding='utf-8')
    AO_fOut.write("Type ~ Positive ~ Negative ~ Value ~ Keywords \n") # The file's header

    print "Reading "    + AO_sSource
    print "Generating " + AO_sProcessed

    # Here we read the ticket extract a character by character lookinf for start (<) and ends (>) of xml espressions
    # while not eof()
    while 1:
        AO_sChar = AO_fInput.read(1)
        if  AO_sChar == '':

            # this is end of file
            AO_sPhrase = AO_bProcessXMLexpression(AO_sPhrase,AO_iIndet,AO_fOut)
            break
                
        elif AO_sChar == '<':

            # This is the start of an XML exorssion
            AO_iIndet = AO_iIndet +1
            AO_sPhrase = AO_bProcessXMLexpression(AO_sPhrase,AO_iIndet,AO_fOut) 
            AO_sPhrase = ''
            
        elif AO_sChar == '>':

            # This is the end of a XML expression
            AO_iIndet = AO_iIndet -1
            AO_sPhrase = AO_bProcessXMLexpression(AO_sPhrase,AO_iIndet,AO_fOut)
            
        else:

            # this is just a charcater that we concatinate to the xml epression
            AO_sPhrase = AO_sPhrase + AO_sChar
            
    AO_fInput.close
    AO_fOut.close

    
if __name__ == '__main__':
   
    main()
