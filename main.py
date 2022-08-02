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


db_url = """sqlite+pysqlite:///data/dbclass.sqlite"""

class HomeScreen(Screen):
    
    def on_enter(self):

        self.ids.nav.switch_tab('Home')
        self.ids.addcontextbutton.close_stack()
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
                    self.ids.phrase_scroll_view.clear_widgets()
                    self.ids.phrase_scroll_view.add_widget(phraseList)
                        
                else : 
                    self.manager.current = 'langpopup'

    def select_lang_trg(self):
        self.manager.current = 'langpopup'
            
    def callback(self, txt):
        pass

class PhraseScrollView(ScrollView):
    pass

class AddContextButton(MDFloatingActionButtonSpeedDial):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.opt = {
                'Add a new context': 'plus',
                'Traduct an existing context in an other lang': 'border-color',
            }
    

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

class UpdateContext(Screen):

    def on_enter(self, **kwargs):
        lang_id = Authenticator.user.lang_id
        with db_session(db_url) as session:
            self.src_context_items = [
                {
                    "text": f"{phrase.content}",
                    "viewclass": "OneLineListItem",
                    "on_release": lambda x= f"{phrase.content}" : self.src_context_callback(x),
                } for phrase in Phrase.get_context_lang(lang_id,session)
            ]
            self.trg_lang_items = [
                {
                    "text": f"{lang.lang}",
                    "viewclass": "OneLineListItem",
                    "on_release": lambda x= f"{lang.lang}" : self.trg_lang_callback(x),
                } for lang in Lang.all(session)
            ]

            self.src_context = MDDropdownMenu(
                caller = self.ids.src_context_button,
                items=self.src_context_items,
                width_mult=4,
            )
            self.trg_lang = MDDropdownMenu(
                caller = self.ids.trg_lang_button,
                items=self.trg_lang_items,
                width_mult=4,
            )

    def src_context_callback(self, lang):
        self.ids.src_context_button.text = lang
        self.src_context.dismiss()

    def trg_lang_callback(self, lang):
        self.ids.trg_lang_button.text = lang
        self.trg_lang.dismiss()

    def submit(self):
        
        src_context = self.ids.src_context_button.text
        trg_lang = self.ids.trg_lang_button.text
        trg_content = self.ids.trg_content.text

        with db_session(db_url) as session :
            trg_lang_id = Lang.get_lang_id(trg_lang, session)
            ref_id = session.query(Phrase.reference_id).filter(Phrase.content == src_context).one()[0]
            context = Phrase(lang_id = trg_lang_id, content = trg_content, reference_id = ref_id)
            context.save(session)
            self.manager.current = 'home'

class AddContext(Screen):

    def on_enter(self, **kwargs):
        with db_session(db_url) as session:
            self.src_lang_items = [
                {
                    "text": f"{lang.lang}",
                    "viewclass": "OneLineListItem",
                    "on_release": lambda x= f"{lang.lang}" : self.src_lang_callback(x),
                } for lang in Lang.all(session)
            ]
            self.trg_lang_items = [
                {
                    "text": f"{lang.lang}",
                    "viewclass": "OneLineListItem",
                    "on_release": lambda x= f"{lang.lang}" : self.trg_lang_callback(x),
                } for lang in Lang.all(session)
            ]

            self.src_lang = MDDropdownMenu(
                caller = self.ids.src_lang_button,
                items=self.src_lang_items,
                width_mult=4,
            )
            self.trg_lang = MDDropdownMenu(
                caller = self.ids.trg_lang_button,
                items=self.trg_lang_items,
                width_mult=4,
            )
        
    def src_lang_callback(self, lang):
        self.ids.src_lang_button.text = lang
        self.src_lang.dismiss()

    def trg_lang_callback(self, lang):
        self.ids.trg_lang_button.text = lang
        self.trg_lang.dismiss()

    def submit(self):
        with db_session(db_url) as session :
            src_lang = self.ids.src_lang_button.text
            src_content = self.ids.src_content.text
            trg_lang = self.ids.trg_lang_button.text
            trg_content = self.ids.trg_content.text

            src_lang_id = Lang.get_lang_id(src_lang, session)
            trg_lang_id = Lang.get_lang_id(trg_lang, session)

            ref = Reference(context_id = 0)
            ref_id = ref.save_return_id(session)
        with db_session(db_url) as session :
            context = Phrase(lang_id = src_lang_id, content = src_content, reference_id = ref_id)
            context.save(session)
        with db_session(db_url) as session :
            context = Phrase(lang_id = trg_lang_id, content = trg_content, reference_id = ref_id)
            context.save(session)
            self.manager.current = 'home'

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
            self.root.current = 'add_context'
        elif instance.icon == 'border-color':
            self.root.current = 'update_context'
            
        

if __name__ == '__main__':
    
    MainApp().run()

   

