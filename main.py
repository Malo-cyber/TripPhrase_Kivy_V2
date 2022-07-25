from enum import Flag
from operator import iconcat
from turtle import onclick
from kivy.lang import Builder
from kivymd.app import MDApp
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.list import OneLineListItem, MDList, OneLineIconListItem, ImageLeftWidget
from kivymd.uix.label import MDLabel
from kivymd.uix.gridlayout import MDGridLayout
from kivymd.uix.button import MDIconButton
import sqlite3
from sqlite3 import Error

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
                                    trad_name TEXT
                                );"""

sql_get_last_trad_id = "SELECT * FROM traduction ORDER BY column DESC LIMIT 1;"

class DBConnection:
    instance = None

    def __new__(cls, *args, **kwargs):
        if cls.instance is None:
            cls.instance = super().__new__(DBConnection)
            return cls.instance
        return cls.instance

    def __init__(self, db_name):
        self.name = db_name
        self.conn = self.connect()
        self.cursor = self.conn.cursor()
        self.conn.execute("PRAGMA foreign_keys = ON")

    def connect(self):
        try:
            return sqlite3.connect(self.name)
        except sqlite3.Error as e:
            pass

    def __del__(self):
        self.cursor.close()
        self.conn.close()

    def execute(self, sql_request):
        try:
            self.cursor.execute(sql_request)
            self.conn.commit()
        except Error as e:
            print(e)
            

class Importer:
    
    def __init__(self, path, lang_src, lang_trg, database):
        self.path = path
        self.lang_src = lang_src
        self.lang_trg = lang_trg
        self.database = database

    def read_data(self):
        import os
        FILE_PATH = self.path
        context = ''
        source_phrase = ''
        target_phrase = ''
        lang_src = self.lang_src
        lang_trg = self.lang_trg

        src_phrase = {}
        src_phraseList = []
        trg_phrase = {}
        trg_phraseList = []
        
        for file in os.listdir(FILE_PATH):
            if file.endswith('.txt'):
                context = file.replace('.txt','')
                with open(f'{FILE_PATH}/{file}') as f:
                    for line in f.readlines():
                        sub = line.split(':')
                        if len(sub)>1:
                            source_phrase = sub[0].lower().replace('\n','').strip()
                            target_phrase = sub[1].lower().replace('\n','').strip()
                            src_phrase = {'lang' : lang_src, 'content' : source_phrase, 'context' : context}
                            trg_phrase = {'lang' : lang_trg, 'content' : target_phrase, 'context' : context}
                            src_phraseList.append(src_phrase)
                            trg_phraseList.append(trg_phrase)

        return src_phraseList, trg_phraseList

    def create_trad_sql_insert(self, last_id):
        trad_name = f'{self.lang_src}_{self.lang_trg}_{last_id}'
        trad_sql_insert = f'INSERT INTO traduction (trad_name) VALUES ("{trad_name}")'
        return trad_sql_insert

    def create_phrase_sql_insert(trad_id, phrase):
        sql_insert_phrase = f"INSERT INTO phrase VALUES (:lang,:content,:context,:trad_id)'," + '{' + f"'lang' : {phrase['lang']},'content' : {phrase['content']},'context' : {phrase['context']}, 'trad_id : {trad_id}" + '}'
        return sql_insert_phrase

    def insert_data(self):
        src_phraseList, trg_phraseList = self.read_data()

        count = 0
        for phrase in src_phraseList:
            last_record = self.database.execute("SELECT * FROM traduction")
            print(last_record)
            count +=1
            sql_trad_insert = self.create_trad_sql_insert(count)
            print(sql_trad_insert)
            self.database.execute(sql_trad_insert)



class CountryList(MDList):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.gen_listItem()


    def gen_listItem(self):
        import os
        for file in os.listdir(FLAG_PATH):
            print('Prout')
            if file.endswith('.png'):
                country = file.replace('.png','')
                list_item = ButtonLang(
                    text = country
                    )
                image = ImageLeftWidget(source = f'{FLAG_PATH}/{country}.png')
                list_item.add_widget(image)
                self.add_widget(list_item)
    
    def langSelected(self):
        print('OK')

class ButtonLang(OneLineIconListItem):
    def callback(self):
        print(f'{self.text}')

class HomeScreen(MDBoxLayout):
    pass

class Phrase():
    def __init__(self, ):
        pass


class MainApp(MDApp):

    

    def Build(self):
        return HomeScreen()

    def on_start(self):
        database = DBConnection(r"./data/datasqlite3.db")
        database.execute(sql_create_phrase_table)
        database.execute(sql_create_traduction_table)
        SlFR = Importer('./data/dicty/Slovene_french', 'Slovenia', 'France', database)
        SlFR.insert_data()

if __name__ == '__main__':
    
    MainApp().run()
