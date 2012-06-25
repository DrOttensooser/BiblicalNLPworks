'# -*- coding: utf-8 -*-'
'''
This module gathers the Orwell Essays
from http://gutenberg.net.au/ebooks03/0300011h.html
and store them in plain text
'''
__author__ = 'Dr Avner OTTENSOOSER <avner.ottensooser@gmail.com>'
__version__ = '$Revision: 0.01 $'

import urllib
import os.path
import re
import codecs

# home folder
AO_sCompelationSite = 'C:\\Users\\Avner\\SkyDrive\\NLP\\OrwellNLPworks\\'

AO_sSource     = 'http://gutenberg.net.au/ebooks03/0300011h.html'

'''
MIT published the Essays in files of this structure
http://Orwell.mit.edu/Poetry/Essay.I.html 
http://Orwell.mit.edu/Poetry/Essay.CLIV.html

'''

# Calculate the name of the files
AO_sModulesPath   =  AO_sCompelationSite + 'Source Code'
AO_sPlainTextPath =  AO_sCompelationSite + 'Data\\Plain Text\\'
AO_sHTMLPath =  AO_sCompelationSite + 'Data\\HTML\\'
AO_sEssayHTML = AO_sHTMLPath +'50OrwelAssays'

def AO_sProcessHeader(AO_sLine):
    m = re.search('<p><a name="part', AO_sLine)
    if str(type(m)) == "<type '_sre.SRE_Match'>":
        AO_sStatus = 'Body'
    else:
        AO_sStatus = 'Header'
    return AO_sStatus

def AO_sProcessFooter(AO_sLine):
    AO_sStatus = 'Footer'
    return AO_sStatus

def main():

    # ensure that the Plain Text  folder exists
    if not os.path.exists(AO_sPlainTextPath):
        os.makedirs(AO_sPlainTextPath)

    # ensure that the HTML  folder exists
    if not os.path.exists(AO_sHTMLPath):
        os.makedirs(AO_sHTMLPath)

    # see if we need to download the book at all
    if not os.path.isfile(AO_sEssayHTML):
        # Download the Essay from the net if need be
        urllib.urlretrieve(AO_sSource, AO_sEssayHTML)

    # Open the downloaded book
    AO_fInput    = open(AO_sEssayHTML,  'r')
    AO_iCurrentAssay = 1
    AO_sAssay=''

    # for all the lines in the HTML file
    AO_sReaderState='Header'
    for line in AO_fInput:
        # remove whight space
        line = line.strip() + " "
        if AO_sReaderState == 'Header':
            AO_sReaderState = AO_sProcessHeader(line)
                          
        elif AO_sReaderState == 'Footer':
             AO_sReaderState = AO_sProcessFooter(line)
        elif AO_sReaderState ==  'Body':
            m = re.search('<p><a name="part', line)
            if str(type(m)) == "<type '_sre.SRE_Match'>":
                AO_sPlainTextFile = AO_sPlainTextPath + 'o' + str(AO_iCurrentAssay) + '.txt'
                AO_fOut = codecs.open(AO_sPlainTextFile,   'w', encoding='utf-8')
                AO_fOut.write(AO_sAssay)
                AO_fOut.close
                AO_sAssay = ""
                AO_iCurrentAssay = AO_iCurrentAssay + 1
            else:
                m = re.search('<p>', line)
                if str(type(m)) == "<type '_sre.SRE_Match'>":
                    n = re.search('</p>', line)
                    if str(type(n)) == "<type '_sre.SRE_Match'>":
                        # This is the case of a one line paragraph
                        AO_sAssay = AO_sAssay + "\n" + line[m.end():n.start()] + "\n"
                    else:
                        # This is the case og the first line in a multi line paragraph
                        AO_sAssay = AO_sAssay + "\n" + line[m.end():]
                else:
                    m = re.search('</p>', line)
                    if str(type(m)) == "<type '_sre.SRE_Match'>":
                        AO_sAssay = AO_sAssay + line[:m.start()] + "\n"
                    else:
                        m = re.search('<h2>THE END</h2>',line)
                        if str(type(m)) == "<type '_sre.SRE_Match'>":
                            AO_sReaderState =  'Footer'
                            AO_sPlainTextFile = AO_sPlainTextPath + 'o' + str(AO_iCurrentAssay) + '.txt'
                            AO_fOut = codecs.open(AO_sPlainTextFile,   'w', encoding='utf-8')
                            AO_fOut.write(AO_sAssay)
                            AO_fOut.close
                        else:
                            m = re.search('<h2>',line)
                            if str(type(m)) == "<type '_sre.SRE_Match'>":
                                line = line[m.end():]
                                m = re.search('</h2>',line)
                                if str(type(m)) == "<type '_sre.SRE_Match'>":
                                    AO_sAssay =  line[:m.start()] + "\n"  + "\n"
                            else:
                                AO_sAssay = AO_sAssay + line 
        else:
            print 'Unexpeted state reached - which is niether Header, Body or Fotter'
    AO_fInput.close
if __name__ == '__main__':
   
    main()
