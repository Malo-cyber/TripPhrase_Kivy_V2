

import json as js
from context_manager import SQLite
import sqlite3

DATAFILE = r"./data/datasqlite3.db"


class Traduction():

    def __init__(self, **kwargs):
        self.trad_count = 0
        self.trad = ''
        self.trad_id = 0
        if len(kwargs) == 1:
            for key, value in kwargs.items():
                    setattr(self, key, value)
            with SQLite(file_name=DATAFILE) as cursor:
                result = cursor.execute(f"""
                    SELECT * FROM traduction
                    WHERE rowid = {self.trad_id}
                """).fetchone()
                for e in result:
                    self.trad_count = result[0]
                    self.trad = result[1]

    def get_trad(self, lang):
        trad_avail = js.loads(self.trad)
        trad_phrase = Phrase(phrase_id = trad_avail[lang])
        return trad_phrase
        
    def add_trad(self, phrase):
        self.trad_count = self.trad_count + 1
        current_trad = self.trad.replace('{', '').replace('}', '')
        trad_to_add = f'"{phrase.lang}" : {phrase.phrase_id}'
        if current_trad == '':
            new_trad = '{' + f"{trad_to_add}" + '}'
        else : 
            new_trad = '{' + current_trad + ',' + trad_to_add + '}'

        self.trad = new_trad
        
        with SQLite(file_name=DATAFILE) as cursor:
            cursor.execute(f"""
                UPDATE traduction 
                SET trad_list = '{self.trad}', trad_count = {self.trad_count}
                WHERE rowid = {self.trad_id}
                """)
        

    def save_trad(self):
        with SQLite(file_name=DATAFILE) as cursor:
            cursor.execute(f'INSERT INTO traduction VALUES ({self.trad_count},"{self.trad}");')
            self.trad_id = cursor.execute('select last_insert_rowid()').fetchone()[0]
            pass
        

class Phrase():

    phrase_id = ''
    trad_id = ''

    def __init__(self, **kwargs):
        for key, value in kwargs.items():
                setattr(self, key, value)
        if self.phrase_id != '':
            with SQLite(file_name=DATAFILE) as cursor:
                #chercher la liste des traductions disponible
                result = cursor.execute(f"""
                    SELECT * FROM phrase
                    WHERE rowid = {self.phrase_id}
                """).fetchone()
                self.lang = result[0]
                self.content = result[1]
                self.context = result[2]
                self.trad_id = result[3]
                
           

    def phrase_save(self):
        with SQLite(file_name=DATAFILE) as cursor:
            #chercher la liste des traductions disponible
            cursor.execute('INSERT INTO phrase VALUES (:lang,:content,:context,:trad_id)',
            {
                'lang' : self.lang,
                'content' : self.content,
                'context' : self.context,
                'trad_id' : self.trad_id
            })
        
            self.phrase_id = cursor.execute('select last_insert_rowid()').fetchone()[0]
                
            

    def get_trad(self, lang):
        trad = Traduction(trad_id = self.trad_id)
        return trad.get_trad(lang)    

