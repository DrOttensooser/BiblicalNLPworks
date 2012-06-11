import sys
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
    import AO_mCorpus


    # for all the books in the J Bible    
    for AO_iJBook in range (0,len(AO_tBooks)):

        AO_sJBook = AO_tBooks[AO_iJBook][0]
        A0_iLastJBookChapter = AO_tBooks[AO_iJBook][2]
        print(AO_sJBook)
        AO_bLoaded = AO_mCorpus.AO_fCorpus(AO_sJBook,AO_tBooks[AO_iJBook][1],A0_iLastJBookChapter,AO_tBooks[AO_iJBook][3])     
    # for all of the J Books
    
if __name__ == '__main__':
   
    main()
