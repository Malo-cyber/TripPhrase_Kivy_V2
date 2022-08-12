from kivy.uix.screenmanager import Screen
from authenticator import Authenticator
from kivymd.uix.menu import MDDropdownMenu


from dbclass import Reference, db_session, User, Phrase, Lang

db_url = """sqlite+pysqlite:///data/dbclass.sqlite"""



class UpdateContext(Screen):

    def on_enter(self, **kwargs):
        lang_id = Authenticator.user.lang_id
        with db_session(db_url) as session:
            self.src_context_items = [
                {
                    "text": f"{phrase.content}",
                    "viewclass": "OneLineListItem",
                    "on_release": lambda x= f"{phrase.content}" : self.src_context_callback(x),
                } for phrase in Phrase.get_context_lang(lang_id,session)
            ]
            self.trg_lang_items = [
                {
                    "text": f"{lang.lang}",
                    "viewclass": "OneLineListItem",
                    "on_release": lambda x= f"{lang.lang}" : self.trg_lang_callback(x),
                } for lang in Lang.all(session)
            ]

            self.src_context = MDDropdownMenu(
                caller = self.ids.src_context_button,
                items=self.src_context_items,
                width_mult=4,
            )
            self.trg_lang = MDDropdownMenu(
                caller = self.ids.trg_lang_button,
                items=self.trg_lang_items,
                width_mult=4,
            )

    def src_context_callback(self, lang):
        self.ids.src_context_button.text = lang
        self.src_context.dismiss()

    def trg_lang_callback(self, lang):
        self.ids.trg_lang_button.text = lang
        self.trg_lang.dismiss()

    def submit(self):
        
        src_context = self.ids.src_context_button.text
        trg_lang = self.ids.trg_lang_button.text
        trg_content = self.ids.trg_content.text

        with db_session(db_url) as session :
            trg_lang_id = Lang.get_lang_id(trg_lang, session)
            ref_id = session.query(Phrase.reference_id).filter(Phrase.content == src_context).one()[0]
            context = Phrase(lang_id = trg_lang_id, content = trg_content, reference_id = ref_id)
            context.save(session)
            self.manager.current = 'home'