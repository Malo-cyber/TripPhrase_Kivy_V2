

from dbclass import db_session, User, Lang



class Authenticator():

    isAuthenticate : bool
    user : User

    @classmethod
    def check_email(cls, email, session):
        """Check if email already exist or not in the sign in process"""
        return User.get_by_email(email, session)

    @classmethod
    def save_user(cls, user : User, session):
        cls.isAuthenticate  = True
        cls.user = user
        cls.user.id = user.save(session)

    @classmethod
    def load_user(cls, email, password, session):
        result = User.get_by_email(email, session)
        if result:
            if result.password != password:
                return False
            else : 
                cls.isAuthenticate = True
                cls.user = result
                return True
        else:
            return False

    @classmethod
    def update_lang(cls, lang, session):
        lang_id = Lang.get_lang_id(lang,session )
        User.update_lang(cls.user.id, lang_id, session)

    @classmethod
    def update_curlang(cls, lang, session):
        cls.user.currlang_id = Lang.get_lang_id(lang, session)
        cls.user.update_currlang(cls.user.id, cls.user.currlang_id, session)

    @classmethod
    def get_user(cls, session):
        result = User.get_by_id(cls.user.id, session)
        if result:
            return result

    @classmethod
    def get_user_name(cls, session):
        result = User.get_by_id(cls.user.id, session)
        if result:
            return result.username

    @classmethod    
    def get_user_currlang(cls, session):
        currlang = Lang.get_lang_by_id(cls.user.currlang_id, session)
        return currlang
            

if __name__ == '__main__':

    pass