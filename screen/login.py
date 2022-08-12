from kivy.uix.screenmanager import Screen
from authenticator import Authenticator
from dbclass import Reference, db_session, User, Phrase, Lang

db_url = """sqlite+pysqlite:///data/dbclass.sqlite"""

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