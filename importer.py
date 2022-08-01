from dbclass import *

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
                context = file.replace('.txt','')
                with open(f'{FILE_PATH}/{file}') as f:
                    for line in f.readlines():
                        sub = line.split(':')
                        if len(sub)>1:
                            source_phrase = sub[0].lower().replace('\n','').strip()
                            target_phrase = sub[1].lower().replace('\n','').strip()
                            traduction = {'lang_src' : lang_src, 'lang_trg' : lang_trg, 'context' : context, 'content_src' : source_phrase, 'content_trg' : target_phrase}
                            traductions.append(traduction)
                            
        return traductions

    def create_instance(self):
        traductions = self.read_data()
        for traduction in traductions:
            trad_obj = Traduction()
            trad_obj.save_trad()
            src_phrase = Phrase(lang = traduction['lang_src'], content = traduction['content_src'],context = traduction['context'],trad_id = trad_obj.trad_id)
            src_phrase.phrase_save()
            trad_obj.add_trad(src_phrase)
            trg_phrase = Phrase(lang = traduction['lang_trg'], content = traduction['content_trg'], context = traduction['context'],trad_id = trad_obj.trad_id)
            trg_phrase.phrase_save()
            trad_obj.add_trad(trg_phrase)
