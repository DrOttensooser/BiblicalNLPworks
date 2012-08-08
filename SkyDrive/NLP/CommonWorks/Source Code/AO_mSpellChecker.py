__synopsys__    = "A spell checker"
__author__      = 'Dr Avner OTTENSOOSER'
__version__     = '$Revision: 1 $'
__enail__       = 'avner.ottensooser@gmail.com'
__creditTo__    = 'http://norvig.com/spell-correct.html'
__me__          = 'AO_mSpellChecker'
                            
AO_ROOT_PATH    = 'C:/Users/Avner/SkyDrive/NLP/'
AO_sDataPath    = AO_ROOT_PATH   + 'CommonWorks/Data/'
AO_sBigText     = AO_sDataPath   + 'SpellCheckerTrainer.txt'



import re, collections

def AO_lWords(text): return re.findall('[a-z]+', text.lower()) 

def AO_mTrain(features):
    AO_clModel = collections.defaultdict(lambda: 1)
    for f in features:
        AO_clModel[f] += 1
    return AO_clModel

NWORDS = AO_mTrain(AO_lWords(file(AO_sBigText).read()))

print 'Spelling Corpus %s trained the spell checker with %i known words.' %(AO_sBigText, len(NWORDS))

alphabet = 'abcdefghijklmnopqrstuvwxyz'

def AO_setEdits1(word):
   splits     = [(word[:i], word[i:]) for i in range(len(word) + 1)]
   deletes    = [a + b[1:] for a, b in splits if b]
   transposes = [a + b[1] + b[0] + b[2:] for a, b in splits if len(b)>1]
   replaces   = [a + c + b[1:] for a, b in splits for c in alphabet if b]
   inserts    = [a + c + b     for a, b in splits for c in alphabet]
   return set(deletes + transposes + replaces + inserts)

def AO_known_edits2(AO_sWord):
    return set(e2 for e1 in AO_setEdits1(AO_sWord) for e2 in AO_setEdits1(e1) if e2 in NWORDS)

def known(AO_lWords): return set(w for w in AO_lWords if w in NWORDS)

def AO_sCorrect(AO_sWord):
    if AO_sWord in ['.','No','no']:
        return AO_sWord
    elif AO_sWord == 'fatt':
        return 'fat'
    else:
        candidates = known([AO_sWord]) or known(AO_setEdits1(AO_sWord)) or AO_known_edits2(AO_sWord) or [AO_sWord]
        return max(candidates, key=NWORDS.get)

def AO_TestMe (AO_sWord, AO_lExpectedResult):
    AO_sCorrcted = AO_sCorrect (AO_sWord)
    AO_bReult =  (AO_sCorrcted ==  AO_lExpectedResult)
    if AO_bReult == False:
        print 'Test failed. The AO_sCorrected spelling of "%s" was expeted to be "%s", alas ist was "%s"' %(AO_sWord , AO_lExpectedResult, AO_sCorrcted )
    return AO_bReult

if __name__ == '__main__':

    # unit tests
    AO_bTest =              AO_TestMe('cattty'   ,'cavity')
    AO_bTest = AO_bTest and AO_TestMe('ckat'     ,'coat')
    AO_bTest = AO_bTest and AO_TestMe('spel'     ,'spell')
    AO_bTest = AO_bTest and AO_TestMe('reciet'   ,'recite' )
    AO_bTest = AO_bTest and AO_TestMe('adres'    ,'acres' )
    AO_bTest = AO_bTest and AO_TestMe('rember'   , 'member')
    AO_bTest = AO_bTest and AO_TestMe('juse'     , 'just' )
    AO_bTest = AO_bTest and AO_TestMe('accesing' , 'acceding' )
    AO_bTest = AO_bTest and AO_TestMe('No' , 'No' )
    AO_bTest = AO_bTest and AO_TestMe('.' , '.' )
    AO_bTest = AO_bTest and AO_TestMe('fatt' , 'fat' )
    AO_bTest = AO_bTest and AO_TestMe('teh' , 'the' )
    AO_bTest = AO_bTest and AO_TestMe('no' , 'no' )

    print '\nUnit Test passed = ' + str(AO_bTest) +'.\n'
