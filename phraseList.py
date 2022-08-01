
from ast import IsNot
from multiprocessing import context
from kivymd.uix.list import OneLineListItem, MDList, TwoLineListItem
import sqlite3
from dbclass import db_session, Phrase

db_url = """sqlite+pysqlite:///data/dbclass.sqlite"""

class PhraseList(MDList):

    def __init__(self, lang_src,lang_trg, **kwargs):
        super().__init__(**kwargs)
        self.lang_src = lang_src
        self.lang_trg = lang_trg

        for key, value in kwargs.items():
                setattr(self, key, value)

        self.gen_contextItems()

    def context_callback(self, text):
        self.current_context = self.contexts[f'{text}']
        self.clear()
        self.gen_listItem()
       
    def retour_callback(self):
        self.current_context = None
        self.clear()
        self.gen_contextItems()

    def clear(self):
        self.clear_widgets()
    
    def gen_contextItems(self):
        self.contexts = {}
        with db_session(db_url) as session:
            for cont in Phrase.get_context_lang(self.lang_src, session):
                self.contexts[f'{cont.content}'] = cont.reference_id
                list_item = ButtonContext(
                    text = cont.content,
                )
                self.add_widget(list_item)
            
    def gen_listItem(self):
        context = self.current_context
        lang = self.lang_src

        with db_session(db_url) as session:
            phrase_list = Phrase.get_phrase_context_lang(context, lang, session)

            retourButton = ReturnButton(
                    text = 'retour'
                )
            self.add_widget(retourButton)

            for phrase in phrase_list:
                traduction = phrase.get_trad(self.lang_trg, session)
                phrase_button = ButtonPhrase(
                    text = phrase.content,
                    secondary_text = traduction.content
                )
                self.add_widget(phrase_button)

            retourButton = ReturnButton(
                text = 'retour'
            )
            self.add_widget(retourButton)
            
            


class ButtonContext(OneLineListItem):
    pass

class ReturnButton(OneLineListItem):
    pass

class ButtonPhrase(TwoLineListItem):
    def callback(self):
        print(f'{self.text}')

if __name__ == '__main__':
    for cont in Context.all():
        print(cont.context)