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
                                    trad_id INTEGER PRIMARY KEY AUTOINCREMENT
                                );"""

class Database():


    def create_connection(db_file):
        """ create a database connection to a SQLite database """
        conn = None
        try:
            conn = sqlite3.connect(db_file)
            print(sqlite3.version)
        except Error as e:
            print(e)
        finally:
            if conn:
                conn.close()

    def create_table(conn, create_table_sql):
        """ create a table from the create_table_sql statement
        :param conn: Connection object
        :param create_table_sql: a CREATE TABLE statement
        :return:
        """
        try:
            c = conn.cursor()
            c.execute(create_table_sql)
        except Error as e:
            print(e)




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
        conn = sqlite3.connect(r"./data/datasqlite3.db")
        if conn is not None:
        # create projects table
            Database.create_table(conn, sql_create_phrase_table)

        # create tasks table
            Database.create_table(conn, sql_create_traduction_table)
        else:
            print("Error! cannot create the database connection.")
            pass


if __name__ == '__main__':
    Database.create_connection(r"./data/datasqlite3.db")
    MainApp().run()
