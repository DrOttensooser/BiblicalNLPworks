'# -*- coding: utf-8 -*-'
'''
This module gathers the shakespeare Sonnets
from http://shakespeare.mit.edu/Poetry
and store them in plain text
'''
__author__ = 'Dr Avner OTTENSOOSER <avner.ottensooser@gmail.com>'
__version__ = '$Revision: 0.01 $'

import urllib
import os.path
import re
import codecs

# home folder
AO_sCompelationSite = 'C:\\Users\\Avner\\SkyDrive\\NLP\\ShakespeareNLPworks\\'

AO_sSonnetSource     = 'http://shakespeare.mit.edu/Poetry/sonnet.'

'''
MIT published the sonnets in files of this structure
http://shakespeare.mit.edu/Poetry/sonnet.I.html 
http://shakespeare.mit.edu/Poetry/sonnet.CLIV.html

'''

# Calculate the name of the files
AO_sModulesPath   =  AO_sCompelationSite + 'Source Code'
AO_sPlainTextPath =  AO_sCompelationSite + 'Data\\Plain Text\\'
AO_sHTMLPath =  AO_sCompelationSite + 'Data\\HTML\\'
AO_iLastSonette = 154


def main():

    import AO_mShakespeareWorksCommon 

    # ensure that the Plain Text  folder exists
    if not os.path.exists(AO_sPlainTextPath):
        os.makedirs(AO_sPlainTextPath)

    # ensure that the HTML  folder exists
    if not os.path.exists(AO_sHTMLPath):
        os.makedirs(AO_sHTMLPath)


    
    for j in range(1,AO_iLastSonette):
        
        AO_sRoman      = AO_mShakespeareWorksCommon.Arab2Roman(j)
        AO_sSonnetURL  = AO_sSonnetSource + AO_sRoman + '.html'
        AO_sSonnetHTML = AO_sHTMLPath + str(j) + ' Sonnet_' + AO_sRoman + '.html'
        AO_sSonnetTXT  = AO_sPlainTextPath + str(j) + ' Sonnet_' + AO_sRoman + '.txt'

        # see if we need to download the book at all
        if not os.path.isfile(AO_sSonnetHTML):
            # Download the sonnet from the net if need be
            urllib.urlretrieve(AO_sSonnetURL, AO_sSonnetHTML)
        print AO_sSonnetHTML

        # Opens the downloaded book
        AO_fInput    = open(AO_sSonnetHTML,  'r')
        AO_fOut      = codecs.open(AO_sSonnetTXT,   'w', encoding='utf-8')

        # for all the lines in the HTML file file
        for line in AO_fInput:
            # remove whight space
            line = line.strip()
            
            m = re.search("<BLOCKQUOTE>", line)

            if str(type(m)) == "<type '_sre.SRE_Match'>":
                line = line[m.end():]
                    
            m = re.search("<BR>", line)
            if str(type(m)) == "<type '_sre.SRE_Match'>":
                line = line[:m.start()]
                AO_fOut.write( line + "\n")
        AO_fOut.close
        AO_fInput.close
        
    
if __name__ == '__main__':
   
    main()
