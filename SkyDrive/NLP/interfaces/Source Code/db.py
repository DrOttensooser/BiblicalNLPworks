'# -*- coding: utf-8 -*-'

''' this nodule creates a database'''

__author__ = 'Dr Avner OTTENSOOSER <avner.ottensooser@gmail.com>'
__version__ = '$Revision: 0.01 $'


AO_ROOT_PATH        =  'C:\\Users\\Avner\\SkyDrive\\NLP\\'
AO_PROJECT_NAME     =  'interfaces'
AO_DATABASE         = AO_ROOT_PATH + AO_PROJECT_NAME + '\\Data\\Database\\flaskr.db'

import sqlite3

def init_db():
    AO_DBconnnection    = sqlite3.connect(AO_DATABASE)
    AO_DBcursor         = AO_DBconnnection.cursor()
    AO_DBcursor.execute('''
                        drop table if exists entries;
                        ''')

    AO_DBcursor.execute('''
                        create table entries(   id integer primary key autoincrement,
                                                title string not null,
                                                text string not null
                                            );
                        ''')
    
    AO_DBconnnection.commit()
    AO_DBconnnection.close()
    
if __name__ == '__main__':

    init_db()
