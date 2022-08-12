from kivy.uix.screenmanager import Screen, ScreenManager
from authenticator import Authenticator
from kivymd.uix.menu import MDDropdownMenu

from dbclass import Reference, db_session, User, Phrase, Lang


db_url = """sqlite+pysqlite:///data/dbclass.sqlite"""



class AddPhrase(Screen):

    def on_leave(self):
        self.ids.src_content.text = ''
        self.ids.trg_content.text = ''

    def on_enter(self, **kwargs):
        lang_id = Authenticator.user.lang_id
        currlang_id = Authenticator.user.currlang_id
        with db_session(db_url) as session:
            self.lang_items = [
                {
                    "text": f"{lang.lang}",
                    "viewclass": "OneLineListItem",
                    "on_release": lambda x= f"{lang.lang}" : self.src_lang_callback(x),
                } for lang in Lang.all(session)
            ]
            self.src_lang = MDDropdownMenu(
                caller = self.ids.src_lang_button,
                items=self.lang_items,
                width_mult=4,
            )
            self.ids.src_lang_button.text = Lang.get_lang_by_id(lang_id, session)

            self.trg_lang = MDDropdownMenu(
                caller = self.ids.trg_lang_button,
                items=self.lang_items,
                width_mult=4,
            )
            self.ids.trg_lang_button.text = Lang.get_lang_by_id(currlang_id, session)

            self.context_items = [
                {
                    "text": f"{phrase.content}",
                    "viewclass": "OneLineListItem",
                    "on_release": lambda x= f"{phrase.content}" : self.src_context_callback(x),
                } for phrase in Phrase.get_context_lang(lang_id,session)
            ]
            self.src_context = MDDropdownMenu(
                caller = self.ids.src_context_button,
                items=self.context_items,
                width_mult=4,
            )
            try:
                if Authenticator.user.current_context != '':
                    self.ids.src_context_button.text = Authenticator.user.current_context
            except:
                self.ids.src_context_button.text = 'Select the context'
    
    def src_context_callback(self, lang):
        self.ids.src_context_button.text = lang
        self.src_context.dismiss()

    def trg_lang_callback(self, lang):
        self.ids.trg_lang_button.text = lang
        self.trg_lang.dismiss()

    def src_lang_callback(self, lang):
        self.ids.src_lang_button.text = lang
        self.src_lang.dismiss()

    def submit(self):
        with db_session(db_url) as session :
            src_lang = self.ids.src_lang_button.text
            src_content = self.ids.src_content.text
            trg_lang = self.ids.trg_lang_button.text
            trg_content = self.ids.trg_content.text
            context_content = self.ids.src_context_button.text

            src_lang_id = Lang.get_lang_id(src_lang, session)
            trg_lang_id = Lang.get_lang_id(trg_lang, session)

            context_id = session.query(Phrase.reference_id).filter(Phrase.content == context_content, Phrase.lang_id == src_lang_id ).one()[0]
            ref = Reference(context_id = context_id)
            ref_id = ref.save_return_id(session)
        with db_session(db_url) as session :
            phrase_src = Phrase(lang_id = src_lang_id, content = src_content, reference_id = ref_id)
            phrase_src.save(session)
        with db_session(db_url) as session :
            phrase_trg = Phrase(lang_id = trg_lang_id, content = trg_content, reference_id = ref_id)
            phrase_trg.save(session)
            self.manager.current = 'home'

    