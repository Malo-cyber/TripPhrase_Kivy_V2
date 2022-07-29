
import sqlalchemy
from sqlalchemy import ForeignKey, create_engine, select
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


class Lang()
    pass
    



Base.metadata.create_all(engine)


if __name__ == '__main__':

    import json as js
    lang_list = []
    Session = sessionmaker(bind=engine)
    session = Session()

    stmt = select(Lang).where(Lang.id.in_(["en", "fr"]))

    for instance in session.scalars(stmt):
       print(instance)

 

   
    

