

import json as js
from context_manager import SQLite
import sqlite3

DATAFILE = r"./data/datasqlite3.db"

class User():
   
    def __init__(self, **kwargs):

        self.username = ''
        self.password = ''
        self.email = ''
        self.lang = ''
        self.favorite = ''
        self.current_lang = ''

        for key, value in kwargs.items():
                setattr(self, key, value)
    
    

class IterTrad(type):
    def __iter__(cls):
        return iter(cls._allTrad)

class Traduction(metaclass=IterTrad):
    _allTrad  = []

    @classmethod
    def DBall(cls):
        """Load data from database and instanciates all objects"""
        with SQLite(file_name=DATAFILE) as cur:
            result = cur.execute("""
                SELECT rowid, trad_count, trad_list FROM traduction
            """).fetchall()
            for e in result:
                trad = Traduction(trad_id = e[0], trad_count = e[1], trad = e[2])

    def __init__(self, **kwargs):

        self._allTrad.append(self)
        self.trad_count = 0
        self.trad = ''
        self.trad_id = 0

        for key, value in kwargs.items():
                setattr(self, key, value)

    def get_trad(self, lang):
        """if avail return phrase instance in the language demands """
        trad_avail = js.loads(self.trad)
        try:
            for phrase in Phrase :
                if phrase.phrase_id == trad_avail[lang] : 
                    return phrase
        except:
            return Phrase(content = 'Error - Traduction unavailable', lang = lang, context = phrase.context)

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

    def __init__(self, **kwargs):

        self.phrase_id = ''
        self.trad_id = ''

        for key, value in kwargs.items():
                setattr(self, key, value)

    @classmethod
    def DBall(cls):
        """Load data from database and instanciates all objects"""
        with SQLite(file_name=DATAFILE) as cur:
            result = cur.execute("""
                SELECT rowid, lang, content, context, trad_id FROM phrase
            """).fetchall()
            for e in result:
                phrase = Phrase(phrase_id = e[0], lang = e[1], content = e[2], context = e[3], trad_id = e[4])
    
    def set_tradId(self):
        pass


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
        for trad in Traduction : 
            if trad.trad_id == self.trad_id:
                return trad.get_trad(lang)

if __name__ == '__main__':

    pass