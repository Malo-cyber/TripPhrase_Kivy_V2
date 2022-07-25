from logging import raiseExceptions
import sqlite3
from sqlite3 import Error
import pandas as pd


FLAG_PATH = '/Users/malorycouvet/programmation/Projects/TripPhrase_Kivy_V2/content/country_icon'

sql_create_phrase_table = """CREATE TABLE IF NOT EXISTS phrase (
                                    phrase_id INTEGER PRIMARY KEY AUTOINCREMENT,
                                    lang TEXT NOT NULL,
                                    content TEXT NOT NULL,
                                    context TEXT NOT NULL,
                                    trad_id INTEGER NOT NULL,
                                    FOREIGN KEY (trad_id) 
                                        REFERENCES traduction (trad_id)
                                    );"""

sql_create_traduction_table = """CREATE TABLE IF NOT EXISTS traduction (
                                    trad_id INTEGER PRIMARY KEY AUTOINCREMENT,
                                    trad_count INTEGER NOT NULL
                                    trad_list TEXT
                                    
                                );"""

try:
    conn = sqlite3.connect(r"./data/datasqlite3.db")
    cur = conn.cursor()
    cur.execute(sql_create_phrase_table)
    cur.execute(sql_create_traduction_table)
except raiseExceptions as e:
    print(e)
finally:
    conn.close()


sql_get_last_trad_id = "SELECT * FROM traduction ORDER BY column DESC LIMIT 1;"

class Phrase():
    def __init__(self, lang, content, context, traduction):
        self.phrase_id = ''
        self.lang = lang
        self.content = content
        self.context = context
        self.trad_id = traduction.trad_id

    def phrase_save(self):
        try:
            conn = sqlite3.connect(r"./data/datasqlite3.db")
            cur = conn.cursor()
            cur.execute('INSERT INTO phrase VALUES (:lang,:content,:context,:trad_id)',
                {
                    'lang' : self.lang,
                    'content' : self.content,
                    'context' : self.context,
                    'trad_id' : self.trad_id
                }
            )
            conn.commit()
            self.phrase_id = cur.execute('select last_insert_rowid()').fetchone()
        except raiseExceptions as e:
             print(e)
        finally:
            conn.close()
            

class Traduction():
    def __init__(self):
        self.trad_count = 0
        self.trad = {}
        self.trad_id = ''

    def add_trad(self, phrase):
        self.trad_count += 1
        self.trad[f'{phrase.lang}'] = phrase.phrase_id
        try:
            conn = sqlite3.connect(r"./data/datasqlite3.db")
            cur = conn.cursor()
            cur.execute('UPDATE traduction SET (:trad_list) WHERE (:trad_id)',
                {
                    'trad_list' : self.trad,
                    'trad_id' : self.trad_id
                }
            )
            conn.commit()
            conn.close()
        except raiseExceptions as e:
            print(e)
        finally:
            conn.close()


    
    def save_trad(self):
        try:
            conn = sqlite3.connect(r"./data/datasqlite3.db")
            cur = conn.cursor()
            cur.execute('INSERT INTO traduction VALUES (:trad_id, :trad_count)',
                {
                    'trad_count' : self.trad_count
                }
            )
            conn.commit()
            self.trad_id = cur.execute('select last_insert_rowid()').fetchone()
            conn.close()
        except raiseExceptions as e:
            print(e)
        finally:
            conn.close()
        

def read_data(self):
        import os
        FILE_PATH = self.path
        context = ''
        source_phrase = ''
        target_phrase = ''
        lang_src = self.lang_src
        lang_trg = self.lang_trg

        traductions = []
        
        for file in os.listdir(FILE_PATH):
            if file.endswith('.txt'):
                context = file.replace('.txt','')
                with open(f'{FILE_PATH}/{file}') as f:
                    for line in f.readlines():
                        sub = line.split(':')
                        if len(sub)>1:
                            source_phrase = sub[0].lower().replace('\n','').strip()
                            target_phrase = sub[1].lower().replace('\n','').strip()
                            traduction = {'lang_src' : lang_src, 'lang_trg' : lang_trg, 'context' : context, 'content_src' : source_phrase, 'content_trg' : target_phrase}
                            traductions.append(traduction)
