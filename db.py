
from ipaddress import AddressValueError
from multiprocessing import context
import sqlalchemy
from sqlalchemy import ForeignKey, PrimaryKeyConstraint, create_engine, select, update
from sqlalchemy import Column, String, Integer
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship



engine = create_engine("sqlite+pysqlite:///data/sqlalchemy.sqlite", echo=True, future=True)
Base = declarative_base()

class User(Base):
    __tablename__ = 'user'

    id = Column(Integer, primary_key=True)
    username = Column(String(30))
    password = Column(String)
    email = Column(String)
    lang_id = Column(String, ForeignKey('lang.id'))

    def __init__(self, username, password, email, lang_id):
        self.username = username
        self.password = password
        self.email = email
        self.lang_id = lang_id    

    def __repr__(self):
        return f"User(id={self.id!r}, username={self.username!r}, password={self.password!r}, email={self.email!r},  lang_id={self.lang_id!r}"


class Lang(Base):

    __tablename__ = 'lang'

    id = Column(String, primary_key = True)
    lang = Column(String)
    user = relationship("User")

    def __init__(self, id, lang):
        self.id = id
        self.lang = lang

    def __repr__(self):
        return f"Lang(id={self.id!r}, lang={self.lang!r})"

    @classmethod
    def get_lang_id(cls, lang):
        Session = sessionmaker(bind=engine)
        session = Session()
        return session.query(Lang.id).filter(Lang.lang == lang)

    @classmethod
    def get_lang_by_id(cls, lang_id):
        Session = sessionmaker(bind=engine)
        session = Session()
        return session.query(Lang.lang).filter(Lang.id == lang_id)


class Context(Base):

    __tablename__ = 'context'

    id = Column(Integer, primary_key = True)
    context = Column(String)
    prhase = relationship("Phrase")

    def __init__(self, id, context):
        self.id = id
        self.context = context

    def __repr__(self):
        return f"Lang(id={self.id!r}, lang={self.lang!r})"

    def save(self):
        Session = sessionmaker(bind=engine)
        session = Session()
        session.add(self)
        session.commit()

    def get_context_id(self):
        return self.id

    @classmethod
    def get_context_by_id(self):
        
        return session.query(Context.context).filter(Context.id == cont_id)



class Phrase(Base):

    __tablename__ = 'phrase'

    id = Column(Integer, primary_key = True)
    lang_id = Column(String, ForeignKey('lang.id'))
    content = Column(String)
    context_id = Column(Integer, ForeignKey('context.id'))
    trad_id = Column(Integer)

    def __init__(self, **kwargs):
        for key, value in kwargs.items():
                setattr(self, key, value)

    def __repr__(self):
        lang = Lang.get_lang_by_id(self.lang_id)
        context = Context.get_context_by_id(self.context_id)
        return f"Phrase(id={self.id}, lang={lang}, content = {self.content}, context = {context}, trad_id = {self.trad_id})"

    def save(self):
        Session = sessionmaker(bind=engine)
        session = Session()
        session.add(self)
        session.commit()

    def update(self, trad_id):
        
        Session = sessionmaker(bind=engine)
        session = Session()
        session.execute(
            update(Phrase).
            where(Phrase.id == f"{self.id}").
            values(trad_id = trad_id)
        )
    
    def get_trad(self, lang):
        Session = sessionmaker(bind=engine)
        session = Session()
        lang_id = Lang.get_lang_id(lang)
        return session.query(Phrase).filter(Phrase.trad_id == self.trad_id and Phrase.lang_id == lang_id )


Base.metadata.create_all(engine)


if __name__ == '__main__':

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
           

    create_instance()"""

    
    

    for cont in Context.get_context_id('Salutation').fetchone()
     