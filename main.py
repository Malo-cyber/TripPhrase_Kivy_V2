import json as js
from turtle import onclick

from kivy.lang import Builder
from kivymd.app import MDApp
from phraseList import PhraseList
from kivy.uix.screenmanager import Screen, ScreenManager
from importer import Importer
from authenticator import Authenticator
from kivymd.uix.menu import MDDropdownMenu
from kivymd.uix.card import MDCard
from kivymd.uix.button import MDFloatingActionButtonSpeedDial
from kivy.uix.scrollview import ScrollView

from dbclass import Reference, db_session, User, Phrase, Lang
from homescreen import HomeScreen
from selectlangpopup import SelectLangPopUp
from signin import SignInScreen
from login import LoginScreen
from profil import ProfilScreen
from updatecontext import UpdateContext
from addphrase import AddPhrase
from addcontext import AddContext

db_url = """sqlite+pysqlite:///data/dbclass.sqlite"""

class PhraseScrollView(ScrollView):
    pass

class AddContextButton(MDFloatingActionButtonSpeedDial):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.opt = {
                'Add new phrase ' : 'plus-circle',
                'Traduct an existing phrase' : 'pen',
                'Add a new context': 'plus',
                'Traduct an existing context in an other lang': 'border-color',
                
            }


class MainApp(MDApp):

    def Build(self):
        
        sm = ScreenManager()
        sm.add_widget(LoginScreen(name='login'))
        sm.add_widget(HomeScreen(name='home'))
        sm.add_widget(SignInScreen(name='signin'))
        sm.add_widget(ProfilScreen(name='profil'))
        sm.add_widget(SelectLangPopUp(name='langpopup'))
        sm.add_widget(AddContext(name='add_context'))
        sm.add_widget(UpdateContext(name='update_context'))
        sm.add_widget(AddPhrase(name='add_phrase'))

        #Set the color theme and palette
        self.theme_cls.theme_style = "Green"
        self.theme_cls.primary_palette = "White"

        return sm
            
    def add_context_callback(self, instance):
        if instance.icon == 'plus':
            self.root.current = 'add_context'
        elif instance.icon == 'border-color':
            self.root.current = 'update_context'
        elif instance.icon == 'plus-circle':
            self.root.current = 'add_phrase'
            
        

if __name__ == '__main__':
    
    MainApp().run()

   

