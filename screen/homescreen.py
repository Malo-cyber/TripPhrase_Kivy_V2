from phraseList import PhraseList
from kivy.uix.screenmanager import Screen

from authenticator import Authenticator
from dbclass import db_session


db_url = """sqlite+pysqlite:///data/dbclass.sqlite"""

class HomeScreen(Screen):
    
    def on_enter(self):

        self.ids.nav.switch_tab('Home')
        self.ids.addcontextbutton.close_stack()
        self.update()
        self.update_curr_context()

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
                    
    def update_curr_context(self):
        self.ids.curr_context.text = str(Authenticator.user.current_context)

    def select_lang_trg(self):
        self.manager.current = 'langpopup'
            
    def callback(self, txt):
        pass