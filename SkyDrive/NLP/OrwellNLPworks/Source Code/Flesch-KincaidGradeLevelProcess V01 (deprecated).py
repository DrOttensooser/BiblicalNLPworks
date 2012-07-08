#!/usr/bin/env python
from __future__ import division
from curses.ascii import isdigit # http://www.lfd.uci.edu/~gohlke/pythonlibs/#pyicu
import json
import sys
import datetime
# import re

from django.utils.datastructures import SortedDict # http://www.lfd.uci.edu/~gohlke/pythonlibs/#django
from django.contrib.localflavor.us.us_states import STATE_CHOICES
from nltk import sent_tokenize, regexp_tokenize
from nltk.corpus import cmudict
#from sunlight import capitolwords as cw # http://pypi.python.org/pypi/python-sunlightapi/
#from sunlight import congress

SYLLABLE_AVG = 1.66
STARTING_CONGRESS = 104
CURRENT_CONGRESS = 112
PER_PAGE = 1000
DICT = cmudict.dict()
LEGISLATORS = {}

'''
for leg in congress.legislators():
    if leg['bioguide_id']:
        LEGISLATORS[leg['bioguide_id']] = leg
STATES = [state[0] for state in STATE_CHOICES]
'''

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


def AO_iSylables(AO_sWord):

'''
This function returns a count of the sylbles is a word.
'''

    return [len(list(y for y in x if isdigit(y[-1]))) for x in DICT[AO_sWord.lower()]][0]


def AO_fGradeDocument(AO_sDocument)
'''
This function calculates the Flesch Kincaid Grade Level of a document
'''
	AO_lWords = [AO_lWords for AO_lWords in AO_lTokenize(AO_sDocument) if (len(AO_lWords) > 1) or (AO_lWords.lower() in ['a', 'i'])]
        AO_lSentences = sent_tokenize(AO_sDocument)
        AO_lSyllables = []
        AO_lMisses = []
        for AO_sWord in AO_lWords:
            try:
                AO_lSyllables.append(AO_iSylables(AO_sWord))
            except KeyError:
                AO_lMisses.append(word)

        AO_iWord_count = len(AO_lWords)
        AO_iSentence_count = len(AO_lSentences)

        # pad syllable count out to word count
        Ao_iWordsMissing_syllables = AO_iWord_count - len(AO_lSyllables)
        for i in range(Ao_iWordsMissing_syllables):
            AO_lSyllables.append(SYLLABLE_AVG)
			AO_iMssing_syllables = AO_iMssing_syllables + SYLLABLE_AVG
        AO_iSyllable_count = sum(AO_lSyllables)
        if AO_iWord_count > 0 and AO_iSentence_count > 0:
            AO_sResults = 
			{
                'words': AO_iWord_count,
                'syllables': AO_iSyllable_count,
                'missed_count': AO_iMssing_syllables,
                'missed_pct': AO_iMssing_syllables / AO_iWord_count,
                'sentences': AO_iSentence_count,
                'grade_level': (0.39 * (AO_iWord_count / AO_iSentence_count)) + (11.8 * (AO_iSyllable_count / AO_iWord_count)) - 15.59,
                'reading_ease': 206.835 - (1.015 * (AO_iWord_count / AO_iSentence_count)) - (84.6 * (AO_iSyllable_count / AO_iWord_count)),
            }
	return AO_sResults
	
if __name__ == '__main__':


        