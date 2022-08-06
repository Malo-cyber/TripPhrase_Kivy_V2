from kivy.uix.screenmanager import Screen, ScreenManager
from authenticator import Authenticator
from kivymd.uix.menu import MDDropdownMenu


from dbclass import Reference, db_session, User, Phrase, Lang

db_url = """sqlite+pysqlite:///data/dbclass.sqlite"""




class AddContext(Screen):

    def on_enter(self, **kwargs):
        lang_id = Authenticator.user.lang_id
        currlang_id = Authenticator.user.currlang_id

        with db_session(db_url) as session:
            self.src_lang_items = [
                {
                    "text": f"{lang.lang}",
                    "viewclass": "OneLineListItem",
                    "on_release": lambda x= f"{lang.lang}" : self.src_lang_callback(x),
                } for lang in Lang.all(session)
            ]
            self.trg_lang_items = [
                {
                    "text": f"{lang.lang}",
                    "viewclass": "OneLineListItem",
                    "on_release": lambda x= f"{lang.lang}" : self.trg_lang_callback(x),
                } for lang in Lang.all(session)
            ]

            self.src_lang = MDDropdownMenu(
                caller = self.ids.src_lang_button,
                items=self.src_lang_items,
                width_mult=4,
            )
            self.trg_lang = MDDropdownMenu(
                caller = self.ids.trg_lang_button,
                items=self.trg_lang_items,
                width_mult=4,
            )

            self.ids.src_lang_button.text = Lang.get_lang_by_id(lang_id, session)
            self.ids.trg_lang_button.text = Lang.get_lang_by_id(currlang_id, session)
        
    def src_lang_callback(self, lang):
        self.ids.src_lang_button.text = lang
        self.src_lang.dismiss()

    def trg_lang_callback(self, lang):
        self.ids.trg_lang_button.text = lang
        self.trg_lang.dismiss()

    def submit(self):
        with db_session(db_url) as session :
            src_lang = self.ids.src_lang_button.text
            src_content = self.ids.src_content.text
            trg_lang = self.ids.trg_lang_button.text
            trg_content = self.ids.trg_content.text

            src_lang_id = Lang.get_lang_id(src_lang, session)
            trg_lang_id = Lang.get_lang_id(trg_lang, session)

            ref = Reference(context_id = 0)
            ref_id = ref.save_return_id(session)
        with db_session(db_url) as session :
            context = Phrase(lang_id = src_lang_id, content = src_content, reference_id = ref_id)
            context.save(session)
        with db_session(db_url) as session :
            context = Phrase(lang_id = trg_lang_id, content = trg_content, reference_id = ref_id)
            context.save(session)
            self.manager.current = 'home'