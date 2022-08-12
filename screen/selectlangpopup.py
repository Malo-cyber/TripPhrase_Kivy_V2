
from kivy.uix.screenmanager import Screen

from authenticator import Authenticator
from kivymd.uix.menu import MDDropdownMenu


from dbclass import Reference, db_session, User, Phrase, Lang


db_url = """sqlite+pysqlite:///data/dbclass.sqlite"""


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