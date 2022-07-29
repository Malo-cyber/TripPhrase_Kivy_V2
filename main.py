import json as js

from kivy.lang import Builder
from kivymd.app import MDApp
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.button import MDIconButton
from kivymd.uix.gridlayout import MDGridLayout
from kivymd.uix.label import MDLabel
from kivymd.uix.list import ImageLeftWidget, MDList
from phraseList import PhraseList
from kivy.uix.screenmanager import Screen, ScreenManager
import phraseList
from context_manager import SQLite
from dataclass import Phrase, Traduction, User
from importer import Importer
from authenticator import Authenticator
from kivymd.uix.menu import MDDropdownMenu
from kivymd.uix.card import MDCard
from importer import Importer

DATAFILE = r"./data/datasqlite3.db"
FLAG_PATH = '/Users/malorycouvet/programmation/Projects/TripPhrase_Kivy_V2/content/country_icon'

avail_context = ['Salutation','Restaurant_bar','Remerciement','Presentation','Direction','time','Numbers']

avail_lang = ['English', 'French', 'Slovenian','Croatian', 'Italian', 'Hungarian', 'Deutch', 'Finish']

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

sql_create_users_table = """CREATE TABLE IF NOT EXISTS users (
                                    username TEXT NOT NULL,
                                    email TEXT NOT NULL,
                                    password TEXT,
                                    favorite TEXT,
                                    lang TEXT,
                                    cur_lang TEXT
                                    
                                )"""

sql_get_last_trad_id = "SELECT * FROM traduction ORDER BY column DESC LIMIT 1;"

with SQLite(file_name=DATAFILE) as cur:
    cur.execute(sql_create_phrase_table)
    cur.execute(sql_create_traduction_table)
    cur.execute(sql_create_users_table)

class HomeScreen(Screen):
    

    def on_enter(self, *args):
        self.update()
        

    def update(self):
        if Authenticator.isAuthenticate:    
            self.ids.logged.text = f" Welcome {Authenticator.user.username}"
            self.ids.trad_lang.text = f"{Authenticator.user.current_lang}"

        if Authenticator.user.current_lang != '' :
            phraseList = PhraseList(
                lang_src = Authenticator.user.lang,
                lang_trg = Authenticator.user.current_lang,
                avail_context = avail_context
            )
            self.ids.scroll_view.clear_widgets()
            self.ids.scroll_view.add_widget(phraseList)
        else : 
            self.manager.current = 'langpopup'


    def select_lang_trg(self):
        self.manager.current = 'langpopup'
            
    def callback(self, txt):
        pass

class SelectLangPopUp(Screen):

    def on_enter(self, **kwargs):
        self.lang_items = [
            {
                "text": f"{lang}",
                "viewclass": "OneLineListItem",
                "on_release": lambda x= f"{lang}" : self.lang_callback(x),
            } for lang in avail_lang
        ]

        self.lang = MDDropdownMenu(
            caller = self.ids.lang_button_select,
            items=self.lang_items,
            width_mult=4,
        )
        
    def lang_callback(self, lang):
        self.ids.lang_button_select.text = lang
        self.lang.dismiss()


    def submit(self):     
        Authenticator.update_curlang(self.ids.lang_button_select.text)
        self.manager.current = 'home'


class SignInScreen(Screen):

    def submit(self):
        if self.ids.password1.text != self.ids.password2.text : 
            self.ids.password1.error = True
            self.ids.password2.error = True
            self.ids.password1.text = 'password incorect'
            self.ids.password2.text = 'password incorect'

        email = self.ids.email.text
        username = self.ids.username.text
        password = self.ids.password1.text

        user = User(email = email, username = username, password = password)

        if Authenticator.check_email(user):
            Authenticator.save_user(user)
            self.manager.current = 'profil'
        else : 
            self.ids.email.error = True
            self.ids.email.text = 'email already use'


class ProfilScreen(Screen):

    def on_enter(self, *args):
        self.lang_items = [
            {
                "text": f"{lang}",
                "viewclass": "OneLineListItem",
                "on_release": lambda x= f"{lang}" : self.lang_callback(x),
            } for lang in avail_lang
        ]

        self.lang = MDDropdownMenu(
                caller = self.ids.lang_button,
                items=self.lang_items,
                width_mult=4,
            )

    def lang_callback(self, lang):
        self.ids.lang_button.text = lang
        self.lang.dismiss()


    def submit(self):     
        Authenticator.update_lang(self.ids.lang_button.text)
        self.manager.current = 'home'
    

class LoginScreen(Screen):

    def submit(self):
        email = self.ids.email.text
        password = self.ids.password.text
        user = User(email = email, password = password)
        if Authenticator.load_user(user = user):
            self.manager.current = 'home'
        else : 
            self.ids.email.error = True
            self.ids.email.text = 'wrong email or password'
            self.ids.password.error = True
            self.ids.password.text = 'wrong email or password'
            

    def login_callback(self):

        username = self.ids.user.text
        password = self.ids.password.text

        self.ids.user.text = ''
        self.ids.password.text = ''

    def sign_in_callback():
        pass
        

class MainApp(MDApp):


    def Build(self):
        
        sm = ScreenManager()
        sm.add_widget(LoginScreen(name='login'))
        sm.add_widget(HomeScreen(name='home'))
        sm.add_widget(SignInScreen(name='signin'))
        sm.add_widget(ProfilScreen(name='profil'))
        sm.add_widget(SelectLangPopUp(name='langpopup'))

        #Set the color theme and palette
        self.theme_cls.theme_style = "Green"
        self.theme_cls.primary_palette = "White"

        return sm

    def on_start(self):

        #remove '#' on the next two line to load exemple data
        #importer = Importer(r'./data/dicty/Slovene_french/', 'Slovenian', 'French')
        #importer.create_instance()

        self.load_database()

        

    def load_database(self):
        """ Load and instanciate all Dataclass object from database collection"""
        
        #call the method DBall from dataclass to load data from database
        Phrase.DBall()
        Traduction.DBall()
        
    
    def callback(self):
        print(self.txt)

if __name__ == '__main__':
    
    MainApp().run()

   

