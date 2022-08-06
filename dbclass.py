
from ipaddress import AddressValueError
from multiprocessing import context
import sqlalchemy
from sqlalchemy import ForeignKey, PrimaryKeyConstraint, create_engine, select, update
from sqlalchemy import Column, String, Integer
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship
from contextlib import contextmanager
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker

db_url = """sqlite+pysqlite:///data/dbclass.sqlite"""

@contextmanager
def db_session(db_url):
    """ Creates a context with an open SQLAlchemy session.
    """
    engine = create_engine(db_url, echo=True, future=True)
    connection = engine.connect()
    db_session = sessionmaker(bind=engine)
    db_session = scoped_session(sessionmaker(autocommit=False, autoflush=False, bind=engine))
    yield db_session
    db_session.close()
    connection.close()


Base = declarative_base()

class User(Base):

    __tablename__ = 'user'

    id = Column(Integer, primary_key=True)
    username = Column(String(30))
    password = Column(String)
    email = Column(String)
    lang_id = Column(String)
    currlang_id = Column(String)
    
    current_context = ''

    def __init__(self, username, password, email, **kwargs):

        self.username = username
        self.password = password
        self.email = email
        

        for key, value in kwargs.items():
                setattr(self, key, value)
         
    def __repr__(self):
        return f"User(id={self.id!r}, username={self.username!r}, password={self.password!r}, email={self.email!r},  lang_id={self.lang_id!r}"

    def save(self, session):
        """Save the user and return its id"""
        session.add(self)
        session.commit()

        return self.id

    @classmethod
    def get_by_email(cls, email, session):
        result = session.query(User).filter(User.email == email)
        for r in result:
            if r:
                return r
            else:
                return False

    @classmethod
    def get_by_id(cls, id, session):
        result = session.query(User).filter(User.id == id)
        for r in result:
            if r:
                return r
            else:
                return False

    @classmethod
    def update_lang(cls, id, lang, session):
        session.execute(
            update(User).
            where(User.id == id).
            values(lang_id = lang)
        )
        session.commit()

    @classmethod
    def update_currlang(cls, id, value, session):
        session.execute(
            update(User).
            where(User.id == id).
            values(currlang_id = value)
        )
        session.commit()
        


class Lang(Base):

    __tablename__ = 'lang'

    id = Column(String, primary_key = True)
    lang = Column(String)
    

    def __init__(self, id, lang):
        self.id = id
        self.lang = lang

    def __repr__(self):
        return f"Lang(id={self.id!r}, lang={self.lang!r})"

    @classmethod
    def get_lang_id(cls, lang, session):
        result = session.query(Lang).filter(Lang.lang == lang)
        for r in result:
            return r.id

    @classmethod
    def get_lang_by_id(cls, lang_id, session):
        
        result = session.query(Lang.lang).filter(Lang.id == lang_id)
        for r in result:
            return r.lang

    @classmethod
    def all(cls, session):
        
        result = session.query(Lang).all()
        return result



class Reference(Base):

    __tablename__ = 'Reference'

    id = Column(Integer, primary_key = True)
    context_id = Column(Integer)

    def __init__(self, **kwargs):
            self.context_id = 0
            for key, value in kwargs.items():
                    setattr(self, key, value)

    def save_return_id(self, session):
        """ save and return id"""
        session.add(self)
        session.commit()
        return self.id


    @classmethod
    def get_ref_context(cls, context_id, session):
        """Return all the reference of phrase in particular context"""
        result = session.query(Reference).filter(Reference.context_id == context_id)
        return result


class Phrase(Base):
    """Class phrase and context"""

    __tablename__ = 'phrase'

    id = Column(Integer, primary_key = True)
    lang_id = Column(String, ForeignKey('lang.id'))
    content = Column(String)
    reference_id = Column(Integer)

    def __init__(self, **kwargs):

        for key, value in kwargs.items():
                setattr(self, key, value)

    def __repr__(self):

        lang = Lang.get_lang_by_id(self.lang_id)
        return f"Phrase(id={self.id}, lang={lang}, content = {self.content}, trad_id = {self.reference_id})"

    def save(self, session):

        session.add(self)
        session.commit()

    def get_trad(self, lang, session):

        return session.query(Phrase).filter(Phrase.reference_id == self.reference_id, Phrase.lang_id == lang ).scalar()
             

    @classmethod
    def get_context_lang(cls, lang_id, session):
        """Return all the context in one language"""
        
        context_ref_all =  session.query(Reference.id).filter(Reference.context_id == 0).all()
        context_id_all = [cont.id for cont in context_ref_all]
        context_phrase = session.query(Phrase).filter(Phrase.reference_id.in_(context_id_all), Phrase.lang_id == lang_id)

        return context_phrase

    @classmethod
    def get_phrase_context_lang(cls, context_ref_id, lang_id, session):
        """return list of phrase select by context and lang"""

        ref_context_all = session.query(Reference.id).filter(Reference.context_id == context_ref_id).all()
        phrase_ref_id = [cont.id for cont in ref_context_all]
        phrase_context_lang = session.query(Phrase).filter(Phrase.reference_id.in_(phrase_ref_id), Phrase.lang_id == lang_id).all()
        
        return phrase_context_lang

engine = create_engine(db_url)
Base.metadata.create_all(engine)


if __name__ == '__main__':


    with db_session(db_url) as session:
        user = User.get_by_id(5, session)
        user.current_context = 'Presentation'
        print(user.current_context)
    """with db_session(db_url) as session:
       
        for cont in Phrase.get_context_lang('en', session):
            print(cont.content)"""
    """import json as js
    lang_list = []

    Session = sessionmaker(bind=engine)
    session = Session()

    langues = {}

    with open("./data/lang/langue.txt") as f:
        langues = js.loads(f.read())

    for key, value in langues.items():
        lang = Lang(value, key)
        session.add(lang)

    session.commit()"""

    """ref = Reference(context_id = 0)
    id_ref = ref.save_return_id()
    phrase = Phrase(lang_id = 'fr', content = 'Salutation', reference_id = id_ref)
    phrase.save()
    phrase = Phrase(lang_id = 'en', content = 'Welcome', reference_id = id_ref)
    phrase.save()
    ref = Reference(context_id = 1)
    id_ref = ref.save_return_id()
    phrase = Phrase(lang_id = 'fr', content = 'Bonjour', reference_id = id_ref)
    phrase.save()
    phrase = Phrase(lang_id = 'en', content = 'Hello', reference_id = id_ref)
    phrase.save()
    phrase = Phrase(lang_id = 'es', content = 'Hola', reference_id = id_ref)
    phrase.save()
    phrase = Phrase(lang_id = 'sl', content = 'Dober dan', reference_id = id_ref)
    phrase.save()
    ref = Reference(context_id = 0)
    id_ref = ref.save_return_id()
    phrase = Phrase(lang_id = 'fr', content = 'Se plaindre', reference_id = id_ref)
    phrase.save()
    phrase = Phrase(lang_id = 'en', content = 'Complain', reference_id = id_ref)
    phrase.save()
    phrase = Phrase(lang_id = 'es', content = 'Quejarse', reference_id = id_ref)
    phrase.save()
    ref = Reference(context_id = id_ref)
    id_ref = ref.save_return_id()
    phrase = Phrase(lang_id = 'fr', content = 'Putain', reference_id = id_ref)
    phrase.save()
    phrase = Phrase(lang_id = 'en', content = 'Fuck', reference_id = id_ref)
    phrase.save()
    phrase = Phrase(lang_id = 'es', content = 'Joder', reference_id = id_ref)
    phrase.save()
    phrase = Phrase(lang_id = 'sl', content = 'Kurba', reference_id = id_ref)
    phrase.save()
    phrase = Phrase(lang_id = 'fi', content = 'Perquele', reference_id = id_ref)
    phrase.save()
    """
    
    
    """result = Phrase.get_context_lang_phrase(3, 'fr')
    for r in result :   
        print(r)
    """

    """result = Reference.get_ref_context(1)
    for r in result:
        print(result)"""

    
    
    

    """

    Session = sessionmaker(bind=engine)
    session = Session()

    langues = {}

    with open("./data/lang/langue.txt") as f:
        langues = js.loads(f.read())

    for key, value in langues.items():
        lang = Lang(value, key)
        session.add(lang)

    session.commit()

    avail_context = {'1' : 'Salutation','2' : 'Restaurant_bar','3' : 'Remerciement','4' : 'Presentation','5' : 'Direction','6' : 'time', '7' : 'Numbers'}

    for key, value in avail_context.items() :
        context = Context(key, value)
        context.save()

    
    def read_data(lang_src, lang_trg):
        import os
        FILE_PATH = "./data/dicty/Slovene_french"
        context = ''
        source_phrase = ''
        target_phrase = ''
        traductions = []
        for file in os.listdir(FILE_PATH):
            if file.endswith('.txt'):
                context = file.replace('.txt','')
                with open(f'{FILE_PATH}/{file}', encoding="utf8") as f:
                    for line in f.readlines():
                        sub = line.split(':')
                        if len(sub)>1:
                            source_phrase = sub[0].lower().replace('\n','').strip()
                            target_phrase = sub[1].lower().replace('\n','').strip()
                            traduction = {'lang_src' : lang_src, 'lang_trg' : lang_trg, 'context' : context, 'content_src' : source_phrase, 'content_trg' : target_phrase}
                            traductions.append(traduction)
                            
        return traductions
    
    
    def create_instance():
        traductions = read_data('sl', 'fr')
        trad_id = 0
        for traduction in traductions:
            for key, value in avail_context.items():
                if value == traduction['context']:
                    context_id = key
            
            src_phrase = Phrase(lang_id = traduction['lang_src'], content = traduction['content_src'],context_id = context_id,trad_id = trad_id)
            src_phrase.save()
            trg_phrase = Phrase(lang_id = traduction['lang_trg'], content = traduction['content_trg'], context_id = context_id,trad_id = trad_id)
            trg_phrase.save()
            trad_id +=1
           

    create_instance()
    """
    """result = Context.get_context_by_id(id = 3)
    print(result)
    result = Context.get_context_id('Remerciement')
    print(result)"""
    
    """Session = sessionmaker(bind=engine)
    session = Session()
    for r in session.query(Phrase).all():
        print(r)"""

    """for cont in Context.all():
        print(cont)"""
    """phrases = []
    for phrase in Phrase.get_context_lang_phrase_list(4, 'fr'):
        print(phrase)
        for r in phrase.get_trad('Slovenian'):
            print(r)
            """