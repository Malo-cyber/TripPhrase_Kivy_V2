
from cmath import phase
from logging import raiseExceptions
from tkinter import Button
from kivy.lang import Builder
from kivymd.app import MDApp
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.list import OneLineListItem, MDList, OneLineIconListItem,TwoLineListItem, ImageLeftWidget
from kivymd.uix.label import MDLabel
from kivymd.uix.gridlayout import MDGridLayout
from kivymd.uix.button import MDIconButton
import sqlite3
from sqlite3 import Error
import pandas as pd
import json as js


FLAG_PATH = '/Users/malorycouvet/programmation/Projects/TripPhrase_Kivy_V2/content/country_icon'

sql_create_phrase_table = """CREATE TABLE IF NOT EXISTS phrase (
                                    lang TEXT NOT NULL,
                                    content TEXT NOT NULL,
                                    context TEXT NOT NULL,
                                    trad_id INTEGER NOT NULL
                                    )"""

sql_create_traduction_table = """CREATE TABLE IF NOT EXISTS traduction (
                                    trad_count INTEGER NOT NULL,
                                    trad_list TEXT
                                    
                                )"""

sql_get_last_trad_id = "SELECT * FROM traduction ORDER BY column DESC LIMIT 1;"

try:
    conn = sqlite3.connect(r"./data/datasqlite3.db")
    print('DB connected')
    cur = conn.cursor()
    cur.execute(sql_create_phrase_table)
    cur.execute(sql_create_traduction_table)
    conn.commit()
    conn.close()

except Exception as err:
    print('Query Failed: \nError: %s' % (str(err)))
finally:
    conn.close()
print('Tables created')



class Phrase():

    phrase_id = ''
    trad_id = ''

    def __init__(self, **kwargs):
        for key, value in kwargs.items():
                setattr(self, key, value)
        if self.phrase_id != '':
            try:
                conn = sqlite3.connect(r"./data/datasqlite3.db")
                cur = conn.cursor()
                #chercher la liste des traductions disponible
                result = cur.execute(f"""
                    SELECT * FROM phrase
                    WHERE rowid = {self.phrase_id}
                """).fetchone()
                self.lang = result[0]
                self.content = result[1]
                self.context = result[2]
                self.trad_id = result[3]
            except Exception as err:
                print('Traduction retreive from database failed: \nError: %s' % (str(err)))
            finally:
                conn.close()

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
            self.phrase_id = cur.execute('select last_insert_rowid()').fetchone()[0]
        except Exception as err:
            print('Query Failed: \nError: %s' % (str(err)))
        finally:
            conn.close()

    def get_trad(self, lang):
        trad = Traduction(trad_id = self.trad_id)
        return trad.get_trad(lang)    



class Traduction():
    def __init__(self, **kwargs):
        self.trad_count = 0
        self.trad = ''
        self.trad_id = 0
        if len(kwargs) == 1:
            for key, value in kwargs.items():
                    setattr(self, key, value)
            try:
                conn = sqlite3.connect(r"./data/datasqlite3.db")
                cur = conn.cursor()
                #chercher la liste des traductions disponible
                result = cur.execute(f"""
                    SELECT * FROM traduction
                    WHERE rowid = {self.trad_id}
                """).fetchone()
                for e in result:
                    self.trad_count = result[0]
                    self.trad = result[1]
            except Exception as err:
                print('Traduction retreive from database failed: \nError: %s' % (str(err)))
            finally:
                conn.close()

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
        try:
            conn = sqlite3.connect(r"./data/datasqlite3.db")
            cur = conn.cursor()
            cur.execute(f"""
                UPDATE traduction 
                SET trad_list = '{self.trad}', trad_count = {self.trad_count}
                WHERE rowid = {self.trad_id}
                """)
            conn.commit()
            conn.close()
        except Exception as err:
            print('Query Failed: \nError: %s' % (str(err)))
        finally:
            conn.close()


    def save_trad(self):
        try:
            conn = sqlite3.connect(r"./data/datasqlite3.db")
            cur = conn.cursor()
            cur.execute(f'INSERT INTO traduction VALUES ({self.trad_count},"{self.trad}");')
            conn.commit()
            self.trad_id = cur.execute('select last_insert_rowid()').fetchone()[0]
            conn.close()
        except Exception as err:
            print('Query Failed in save_trad: \nError: %s' % (str(err)))
        finally:
            conn.close()
        
class Importer:
    
    def __init__(self, path, lang_src, lang_trg):
        self.path = path
        self.lang_src = lang_src
        self.lang_trg = lang_trg

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
                            
        return traductions

    def create_instance(self):
        traductions = self.read_data()
        for traduction in traductions:
            trad_obj = Traduction()
            trad_obj.save_trad()
            src_phrase = Phrase(lang = traduction['lang_src'], content = traduction['content_src'],context = traduction['context'],trad_id = trad_obj.trad_id)
            src_phrase.phrase_save()
            trad_obj.add_trad(src_phrase)
            trg_phrase = Phrase(lang = traduction['lang_trg'], content = traduction['content_trg'], context = traduction['context'],trad_id = trad_obj.trad_id)
            trg_phrase.phrase_save()
            trad_obj.add_trad(trg_phrase)

            

class CountryList(MDList):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.gen_listItem()


    def gen_listItem(self):
        import os
        for file in os.listdir(FLAG_PATH):
            if file.endswith('.png'):
                country = file.replace('.png','')
                list_item = ButtonLang(
                    text = country
                    )
                image = ImageLeftWidget(source = f'{FLAG_PATH}/{country}.png')
                list_item.add_widget(image)
                self.add_widget(list_item)

class ButtonContext(OneLineListItem):
    pass
class ReturnButton(OneLineListItem):
    pass

class ButtonPhrase(TwoLineListItem):
    def callback(self):
        print(f'{self.text}')

class ButtonLang(OneLineIconListItem):
    def callback(self):
        print(f'{self.text}')

class PhraseList(MDList):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.gen_contextItems()

    def context_callback(self, text):
        self.clear()
        self.gen_listItem(text)
        
    def retour_callback(self):
        self.clear()
        self.gen_contextItems()

    def clear(self):
        self.clear_widgets()
    
    def gen_contextItems(self):
        avail_context = ['Salutation','Restaurant_bar','Remerciement','Presentation','Direction','time','Numbers']
        for cont in avail_context:
            list_item = ButtonContext(
                text = cont
            )
            self.add_widget(list_item)
    
    def gen_listItem(self, context):
        phrase_list = self.get_context_lang_phrase_list(context, 'French')
        retourButton = ReturnButton(
                text = 'retour'
            )
        self.add_widget(retourButton)
        for phrase in phrase_list:
            phrase.get_trad('Slovenian')
            phrase_button = ButtonPhrase(
                text = phrase.content,
                secondary_text = phrase.get_trad('Slovenian').content
            )
            self.add_widget(phrase_button)
        retourButton = ReturnButton(
            text = 'retour'
        )
        self.add_widget(retourButton)
            
            
        

    def get_context_lang_phrase_list(self, context, lang):
        phrase_list = []
        try:
            conn = sqlite3.connect(r"./data/datasqlite3.db")
            cur = conn.cursor()
            result = cur.execute(f"""
                SELECT * FROM phrase
                WHERE context = '{context}' AND lang = '{lang}'
            """).fetchall()
            for e in result:
                phrase = Phrase(lang = e[0], content = e[1], context = e[2], trad_id = e[3] )
                phrase_list.append(phrase)
        except Exception as err:
            print('Query Failed in get-context-lang-phrase: \nError: %s' % (str(err)))
        finally:
            conn.close()
        return phrase_list



class HomeScreen(MDBoxLayout):
    def callback(self, txt):
        print(txt)
    



class MainApp(MDApp):


    def Build(self):
        return HomeScreen()

    def on_start(self):
        pass
       
    
    def callback(self):
        print(self.txt)

if __name__ == '__main__':
    
    MainApp().run()

   

