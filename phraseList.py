
from ast import IsNot
from kivymd.uix.list import OneLineListItem, MDList, TwoLineListItem
import sqlite3
from db import Context, Phrase, User, Lang

class PhraseList(MDList):

    def __init__(self, lang_src,lang_trg, **kwargs):
        super().__init__(**kwargs)
        self.lang_src = lang_src
        self.lang_trg = lang_trg

        for key, value in kwargs.items():
                setattr(self, key, value)

        self.gen_contextItems()

    def context_callback(self, text):
        self.current_context = text
        self.clear()
        self.gen_listItem()
       
    def retour_callback(self):
        self.current_context = None
        self.clear()
        self.gen_contextItems()

    def clear(self):
        self.clear_widgets()
    
    def gen_contextItems(self):
        for cont in Context.all():
            list_item = ButtonContext(
                text = cont.context
            )
            self.add_widget(list_item)
            
    def gen_listItem(self):
        context = Context.get_context_id(self.current_context)
        lang = Lang.get_lang_id(self.lang_src)

        phrase_list = Phrase.get_context_lang_phrase_list(context, lang)

        retourButton = ReturnButton(
                text = 'retour'
            )
        self.add_widget(retourButton)

        for phrase in phrase_list:
            traduction = phrase.get_trad(self.lang_trg)
            for trad in traduction:
                phrase_button = ButtonPhrase(
                    text = phrase.content,
                    secondary_text = trad.content
                )
                if traduction.phrase_id == '':
                    del traduction
        
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