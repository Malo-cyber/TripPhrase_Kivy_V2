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

from dbclass import db_session, User, Phrase, Lang


db_url = """sqlite+pysqlite:///data/dbclass.sqlite"""

class HomeScreen(Screen):
    

    def on_enter(self, *args):
        self.ids.nav.switch_tab('Home')
        opt =  {
        'Add a new context': 'plus',
        'Traduct an existing context in an other lang': 'border-color',
        }
        add_context_button = AddContextButton(
            data = opt,
            pos_hint={"center_x": .9, "center_y": .1},
            root_button_anim = True
        )

        self.ids.nav_home.add_widget(add_context_button)
        self.update()
        
    
        

    def update(self):
        if Authenticator.isAuthenticate:
            with db_session(db_url) as session:    
                self.ids.logged.text = f" Welcome {Authenticator.get_user_name(session)}"
                lang = Authenticator.get_user_currlang(session)
                self.ids.trad_lang.text = f"{lang}"

                if Authenticator.get_user_currlang(session) != None :
                    phraseList = PhraseList(
                        lang_src = Authenticator.user.lang_id,
                        lang_trg = Authenticator.user.currlang_id,
                    )
                    self.ids.scroll_view.clear_widgets()
                    self.ids.scroll_view.add_widget(phraseList)
                else : 
                    self.manager.current = 'langpopup'

    def select_lang_trg(self):
        self.manager.current = 'langpopup'
            
    def callback(self, txt):
        pass

class AddContextButton(MDFloatingActionButtonSpeedDial):
    pass

class SelectLangPopUp(Screen):

    def on_enter(self, **kwargs):
        with db_session(db_url) as session:
            self.lang_items = [
                {
                    "text": f"{lang.lang}",
                    "viewclass": "OneLineListItem",
                    "on_release": lambda x= f"{lang.lang}" : self.lang_callback(x),
                } for lang in Lang.all(session)
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
        with db_session(db_url) as session:   
            Authenticator.update_curlang(self.ids.lang_button_select.text, session)
            self.manager.current = 'home'


class SignInScreen(Screen):

    def submit(self):
        if self.ids.password1.text != self.ids.password2.text : 
            self.ids.password1.error = True
            self.ids.password2.error = True
            self.ids.password1.text = 'password incorect'
            self.ids.password2.hint_text = 'password incorect'

        email = self.ids.email.text
        username = self.ids.username.text
        password = self.ids.password1.text

        with db_session(db_url) as session:
            if Authenticator.check_email(email, session):
                self.ids.email.error = True
                self.ids.email.hint_text = 'email already use'
            else : 
                user = User(username,password, email)
                Authenticator.save_user(user, session)
                self.manager.current = 'profil'
            


class ProfilScreen(Screen):

    def on_enter(self, *args):
        with db_session(db_url) as session:
            self.lang_items = [
                {
                    "text": f"{lang.lang}",
                    "viewclass": "OneLineListItem",
                    "on_release": lambda x= f"{lang.lang}" : self.lang_callback(x),
                } for lang in Lang.all(session)
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
        with db_session(db_url) as session: 
            Authenticator.update_lang(self.ids.lang_button.text, session)
            self.manager.current = 'home'
    

class LoginScreen(Screen):

    def submit(self):
        email = self.ids.email.text
        password = self.ids.password.text
        
        with db_session(db_url) as session:
            if Authenticator.load_user(email, password, session):
                self.manager.current = 'home'
            else : 
                self.ids.email.error = True
                self.ids.email.hint_text = 'wrong email or password'
                self.ids.password.error = True
                self.ids.password.hint_text = 'wrong email or password'
            

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
        
        pass

        

    def load_database(self):
        """ Load and instanciate all Dataclass object from database collection"""
        
        #call the method DBall from dataclass to load data from database
        """Phrase.DBall()
        Traduction.DBall()"""
        
    
    def add_context_callback(self, instance):
        if instance.icon == 'plus':
            self.manager.current = 'add'
        elif instance.icon == 'border-color':
            pass

if __name__ == '__main__':
    
    MainApp().run()

   

