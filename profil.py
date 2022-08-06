from kivy.uix.screenmanager import Screen, ScreenManager
from authenticator import Authenticator
from kivymd.uix.menu import MDDropdownMenu


from dbclass import Reference, db_session, User, Phrase, Lang


db_url = """sqlite+pysqlite:///data/dbclass.sqlite"""

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
    