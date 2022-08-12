from kivy.uix.screenmanager import Screen
from authenticator import Authenticator
from dbclass import Reference, db_session, User, Phrase, Lang


db_url = """sqlite+pysqlite:///data/dbclass.sqlite"""




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
            
