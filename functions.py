from time import sleep

import httpx
# import deepl
from models import db, Noun, Verb, Adverb, Adjective, Pronoun


# auth_key = "371bc5b9-3443-48ae-8398-7dcdd7dfec98:fx"
# translator = deepl.Translator(auth_key)

class GetWord:
    def __init__(self):
        self.url = "https://spraakbanken4.it.gu.se/karp/v7/query/saldom"

    def noun(self, inflection_table, baseform):
        sg_indef_nom = sg_def_nom = pl_indef_nom = pl_def_nom = None

        # en_translation_ob = translator.translate_text(baseform, source_lang="SV", target_lang="EN-US")
        # en_translation = en_translation_ob.text

        for item in inflection_table:
            form_type = item.get("msd")
            form = item.get("writtenForm")
            if form_type == "sg indef nom":
                sg_indef_nom = form
                print(sg_indef_nom)
            elif form_type == "sg def nom":
                sg_def_nom = form
                print(sg_def_nom)
            elif form_type == "pl indef nom":
                pl_indef_nom = form
                print(pl_indef_nom)
            elif form_type == "pl def nom":
                pl_def_nom = form
                print(pl_def_nom)
            else:
                pass
        new_record = Noun(noun=baseform, en_translation="-", indefinite_singular=sg_indef_nom,
                          definite_singular=sg_def_nom, indefinite_plural=pl_indef_nom, definite_plural=pl_def_nom)
        db.session.add(new_record)
        db.session.commit()

    def adjective(self, inflection_table, baseform):
        pos_indef_sg_u_nom = pos_indef_sg_n_nom = pos_indef_pl_nom = None

        # en_translation_ob = translator.translate_text(baseform, source_lang="SV", target_lang="EN-US")
        # en_translation = en_translation_ob.text

        for item in inflection_table:
            form_type = item.get("msd")
            form = item.get("writtenForm")
            if form_type == "pos indef sg u nom":
                pos_indef_sg_u_nom = form
                print(pos_indef_sg_u_nom)
            elif form_type == "pos indef sg n nom":
                pos_indef_sg_n_nom = form
                print(pos_indef_sg_n_nom)
            elif form_type == "pos indef pl nom":
                pos_indef_pl_nom = form
                print(pos_indef_pl_nom)
            else:
                pass
        new_record = Adjective(noun=baseform, en_translation="-", common_singular=pos_indef_sg_u_nom,
                          neuter_singular=pos_indef_sg_n_nom, indefinite_plural=pos_indef_pl_nom)
        db.session.add(new_record)
        db.session.commit()

    def verb(self, inflection_table, baseform):
        pres_ind_aktiv = pret_ind_aktiv = sup_aktiv = imper = None

        # en_translation_ob = translator.translate_text(baseform, source_lang="SV", target_lang="EN-US")
        # en_translation = en_translation_ob.text

        for item in inflection_table:
            form_type = item.get("msd")
            form = item.get("writtenForm")
            if form_type == "pres ind aktiv":
                pres_ind_aktiv = form
                print(pres_ind_aktiv)
            elif form_type == "pret ind aktiv":
                pret_ind_aktiv = form
                print(pret_ind_aktiv)
            elif form_type == "sup aktiv":
                sup_aktiv = form
                print(sup_aktiv)
            elif form_type == "imper":
                imper = form
                print(imper)
            else:
                pass
        new_record = Verb(verb=baseform, en_translation="-", present=pres_ind_aktiv,
                          preterite=pret_ind_aktiv, supine=sup_aktiv, imperative=imper)
        db.session.add(new_record)
        db.session.commit()

    def pronoun(self, inflection_table, baseform):
        pres_ind_aktiv = pret_ind_aktiv = sup_aktiv = imper = None

        # en_translation_ob = translator.translate_text(baseform, source_lang="SV", target_lang="EN-US")
        # en_translation = en_translation_ob.text

        for item in inflection_table:
            form_type = item.get("msd")
            form = item.get("writtenForm")
            if form_type == "pres ind aktiv":
                pres_ind_aktiv = form
                print(pres_ind_aktiv)
            elif form_type == "pret ind aktiv":
                pret_ind_aktiv = form
                print(pret_ind_aktiv)
            elif form_type == "sup aktiv":
                sup_aktiv = form
                print(sup_aktiv)
            elif form_type == "imper":
                imper = form
                print(imper)
            else:
                pass
        new_record = Pronoun(verb=baseform, en_translation="-", present=pres_ind_aktiv,
                          preterite=pret_ind_aktiv, supine=sup_aktiv, imperative=imper)
        db.session.add(new_record)
        db.session.commit()

    def adverb(self, baseform):

        new_record = Adverb(verb=baseform, en_translation="-")
        db.session.add(new_record)
        db.session.commit()

    # proper_noun, adjective
    # nl - numeral

    def get_word(self):
        batch_size = 1000
        batch_from = 0

        while True:
            params = {
                "resource": "saldom",
                "size" : batch_size,
                "show" : ["baseform", "partOfSpeech", "inflectionTable"],
                "from" : batch_from
            }
            response = httpx.get(self.url, params=params)
            print(response, response.status_code)
            j_response = response.json()
            scope = j_response.get("hits")

            if not scope:
                print("aaaaaaa")
                print(response.request)
                break

            for result in scope:
                word = result.get("entry")
                pos = word.get("partOfSpeech")
                baseform = word.get("baseform")
                inflection_table = word.get("inflectionTable")
                if not inflection_table:
                    continue
                if pos == "nn":
                    self.noun(inflection_table, baseform)
                elif pos == "vbm":
                    self.verb(inflection_table, baseform)
                elif pos == "ab":
                    self.adverb(baseform)
                elif pos == "av":
                    self.adjective(inflection_table, baseform)
                else:
                    pass

            batch_from += batch_size

class GetTranslation:
    def __init__(self):
        self.url = "https://libretranslate.com/translate"

    def translate(self):
        params = {
            "q": "house",
            "source": "en",
            "target": "sv",
            "format": "text",
            "alternatives": 3,
            "api_key" : ""
        }

        responce = httpx.post(self.url, params=params)
        responce_j = responce.json()
        print(responce_j)

# translation = GetTranslation()
# translation.translate()

"""https://spraakbanken.gu.se/karp/?mode=saldom&lexicon=saldom&show=saldom:01HQMY8726SN5W354RSWEV9DFQ&tab=json&filter="""

# res = "https://spraakbanken4.it.gu.se/karp/v7/resources/"
#"https://spraakbanken4.it.gu.se/karp/v7/query/saldom"
# reso = httpx.get(res)
# resors = json.load(reso)
# print(resors)