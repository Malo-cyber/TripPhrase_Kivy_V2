from ast import boolop
from context_manager import SQLite
from dataclass import User

DATAFILE = r"./data/datasqlite3.db"

class Authenticator():

    isAuthenticate : bool
    user : User

    @classmethod
    def check_email(cls, user : User):
        with SQLite(file_name=DATAFILE) as cur:
            result = cur.execute(f"""
                SELECT email FROM users
                WHERE email = "{user.email}"
            """).fetchone()
        if result != None:
            return False
        else:
            return True

    @classmethod
    def save_user(cls, user : User):
        with SQLite(file_name=DATAFILE) as cur:
            cur.execute('INSERT INTO users VALUES(:username, :email, :password, :lang, :favorite, :cur_lang)',
            {
                'username' : user.username,
                'email' : user.email,
                'password': user.password,
                'lang' : user.lang,
                'favorite' : user.favorite,
                'cur_lang' : user.current_lang
            }
        )
        cls.isAuthenticate  = True
        cls.user = user

    @classmethod
    def load_user(cls, user : User):
        with SQLite(file_name=DATAFILE) as cur:
            result = cur.execute(f"""
                SELECT * FROM users
                WHERE email = "{user.email}"
            """).fetchone()
        if result:
            if result[2] != user.password:
                return False
            else : 
                cls.isAuthenticate = True
                cls.user = User(username = result[0], email = result[1], password = [2], favorite = result[3], lang = result[4], current_lang = result[5])
                return True
        else:
            return False

    @classmethod
    def update_lang(cls, lang):
        cls.user.lang = lang
        with SQLite(file_name=DATAFILE) as cur:
            cur.execute(f"""
                UPDATE users 
                SET lang = '{lang}'
                WHERE email = "{cls.user.email}"
             """)

    @classmethod
    def update_curlang(cls, lang):
        cls.user.current_lang = lang
        with SQLite(file_name=DATAFILE) as cur:
            cur.execute(f"""
                UPDATE users 
                SET cur_lang = '{lang}'
                WHERE email = "{cls.user.email}"
             """)




if __name__ == '__main__':

    user = User(username = 'Malo', email = 'm.couvet@icloud.com')

    with SQLite(file_name=DATAFILE) as cur:
        cur.execute('INSERT INTO users VALUES(:username, :email, :password, :lang, :favorite, :cur_lang)',
            {
                'username' : user.username,
                'email' : user.email,
                'password': user.password,
                'lang' : user.lang,
                'favorite' : user.favorite,
                'cur_lang' : user.current_lang
            }
        )


    if Authenticator.check_email(user):
        print('email disponible')
    else :
        print('already exist')