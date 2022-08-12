import dbclass
from dbclass import Reference, db_session, User, Phrase, Lang


db_url = """sqlite+pysqlite:///data/dbclass.sqlite"""

class Importer:
    
    def __init__(self, path, lang_src, lang_trg):
        self.path = path
        self.lang_src = lang_src
        self.lang_trg = lang_trg
      

    def read_data(self):
        import os
        FILE_PATH = self.path
        context = ''
        source_phrase = ''
        target_phrase = ''
        lang_src = self.lang_src
        lang_trg = self.lang_trg

        traductions = []
        
        for file in os.listdir(FILE_PATH):
            if file.endswith('.txt'):
                context_trg = file.split('_')[0]
                context_src = file.split('_')[1].replace('.txt','')
                with open(f'{FILE_PATH}/{file}') as f:
                    for line in f.readlines():
                        sub = line.split(':')
                        if len(sub)>1:
                            source_phrase = sub[0].lower().replace('\n','').strip()
                            target_phrase = sub[1].lower().replace('\n','').strip()
                            traduction = {'lang_src' : lang_src, 'lang_trg' : lang_trg, 'context_src' : context_src, 'context_trg' : context_trg, 'content_src' : source_phrase, 'content_trg' : target_phrase}
                            traductions.append(traduction)
                            
        return traductions

    def create_instance(self):
        traductions = self.read_data()
        
        for traduction in traductions:
            ref_id = ''
            print(traduction)

            #retrouver les context id
            with db_session(db_url) as session :
                r = session.query(Phrase.reference_id).filter(Phrase.content == traduction['context_src'], Phrase.lang_id == traduction['lang_src']).scalar()
                if r :
                    print(f'Phrase.ref_id = {r} - for Phrase.content == {traduction["context_src"]}')
                    ref_id = r
                    
                    
                r = session.query(Phrase.reference_id).filter(Phrase.content == traduction['context_trg'], Phrase.lang_id == traduction['lang_trg']).scalar()
                if r :
                    print(f'Phrase.ref_id = {r} - for Phrase.content == {traduction["context_trg"]}')
                    ref_id = r
                    
                    

            if ref_id == '':
                with db_session(db_url) as session:
                        ref = Reference(context_id = 0)
                        ref_id = ref.save_return_id(session)

                with db_session(db_url) as session:
                    phrase = Phrase(lang_id = traduction['lang_trg'], content = traduction['context_trg'], reference_id = ref_id)
                    phrase.save(session)

                with db_session(db_url) as session:
                    phrase = Phrase(lang_id = traduction['lang_src'], content = traduction['context_src'], reference_id = ref_id)
                    phrase.save(session)


            with db_session(db_url) as session:
                        ref = Reference(context_id = ref_id)
                        ref_id = ref.save_return_id(session)
            with db_session(db_url) as session : 
                    phrase = Phrase(lang_id = traduction['lang_src'], content = traduction['content_src'], reference_id = ref_id)
                    phrase.save(session)
            with db_session(db_url) as session : 
                    phrase = Phrase(lang_id = traduction['lang_trg'], content = traduction['content_trg'], reference_id = ref_id)
                    phrase.save(session)

if __name__ == '__main__':

    importe = Importer('./data/dicty/Slovene_french', 'sl', 'fr')
    importe.create_instance()
    