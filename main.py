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
from dataclass import Traduction, Phrase
import phraseList
import importer

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


class ButtonLang(OneLineIconListItem):
    def callback(self):
        print(f'{self.text}')


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

   

