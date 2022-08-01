from ast import boolop
from sqlite3 import dbapi2
from context_manager import SQLite
from db import Context, Phrase, User, Lang



DATAFILE = r"./data/datasqlite3.db"

class Authenticator():

    isAuthenticate : bool
    user_id : int

    @classmethod
    def check_email(cls, email):
        return User.check_email(email)

    @classmethod
    def save_user(cls, user : User):
        cls.isAuthenticate  = True
        cls.user_id = user.save()
        

    @classmethod
    def load_user(cls, email, password):
        result = User.authenticate(email)
        if result:
            if result.password != password:
                return False
            else : 
                cls.isAuthenticate = True
                cls.user_id = result.id
                return True
        else:
            return False

    @classmethod
    def update_lang(cls, lang):
        lang = Lang.get_lang_id(lang)
        User.update_lang(cls.user_id, lang)

    @classmethod
    def update_curlang(cls, lang):
        cls.user.currlang_id = Lang.get_lang_id(lang)
        cls.user.update_currlang('currlang_id', cls.user.currlang_id)

    @classmethod
    def get_user_name(cls):
        result = User.get_user_by_id(cls.user_id)
        if result:
            return result.username

    @classmethod    
    def get_user_currlang(cls):
        result = User.get_user_by_id(cls.user_id)
        if result:
            return result.currlang_id

if __name__ == '__main__':

    pass