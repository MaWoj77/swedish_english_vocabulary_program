from time import sleep

from flask import flash
import httpx
import deepl

from models import db, Noun, Verb, Adverb, Adjective, ProperNoun, Numeral, Interjection, Preposition

auth_key = "371bc5b9-3443-48ae-8398-7dcdd7dfec98:fx"
translator = deepl.Translator(auth_key)

class GetWord:
    def __init__(self):
        self.url = "https://spraakbanken4.it.gu.se/karp/v7/query/saldom"

    def noun(self, inflection_table, baseform):
        sg_indef_nom = sg_def_nom = pl_indef_nom = pl_def_nom = None

        for item in inflection_table:
            form_type = item.get("msd")
            form = item.get("writtenForm")
            if form_type == "sg indef nom":
                sg_indef_nom = form
            elif form_type == "sg def nom":
                sg_def_nom = form
            elif form_type == "pl indef nom":
                pl_indef_nom = form
            elif form_type == "pl def nom":
                pl_def_nom = form
            else:
                pass
        new_record = Noun(baseform=baseform, en_translation="-", indefinite_singular=sg_indef_nom,
                          definite_singular=sg_def_nom, indefinite_plural=pl_indef_nom, definite_plural=pl_def_nom)
        db.session.add(new_record)
        db.session.commit()

    def adjective(self, inflection_table, baseform):
        pos_indef_sg_u_nom = pos_indef_sg_n_nom = pos_indef_pl_nom = None

        for item in inflection_table:
            form_type = item.get("msd")
            form = item.get("writtenForm")
            if form_type == "pos indef sg u nom":
                pos_indef_sg_u_nom = form
            elif form_type == "pos indef sg n nom":
                pos_indef_sg_n_nom = form
            elif form_type == "pos indef pl nom":
                pos_indef_pl_nom = form
            else:
                pass
        new_record = Adjective(baseform=baseform, en_translation="-", common_singular=pos_indef_sg_u_nom,
                          neuter_singular=pos_indef_sg_n_nom, indefinite_plural=pos_indef_pl_nom)
        db.session.add(new_record)
        db.session.commit()

    def verb(self, inflection_table, baseform):
        pres_ind_aktiv = pret_ind_aktiv = sup_aktiv = imper = None

        for item in inflection_table:
            form_type = item.get("msd")
            form = item.get("writtenForm")
            if form_type == "pres ind aktiv":
                pres_ind_aktiv = form
            elif form_type == "pret ind aktiv":
                pret_ind_aktiv = form
            elif form_type == "sup aktiv":
                sup_aktiv = form
            elif form_type == "imper":
                imper = form
            else:
                pass
        new_record = Verb(baseform=baseform, en_translation="-", present=pres_ind_aktiv,
                          preterite=pret_ind_aktiv, supine=sup_aktiv, imperative=imper)
        db.session.add(new_record)
        db.session.commit()

    def adverb(self, baseform):

        new_record = Adverb(baseform=baseform, en_translation="-")
        db.session.add(new_record)
        db.session.commit()

    def proper_noun(self, baseform):

        new_record = ProperNoun(baseform=baseform, en_translation="-")
        db.session.add(new_record)
        db.session.commit()

    def numeral(self, baseform):

        new_record = Numeral(baseform=baseform, en_translation="-")
        db.session.add(new_record)
        db.session.commit()

    def interjection(self, baseform):
        new_record = Interjection(baseform=baseform, en_translation="-")
        db.session.add(new_record)
        db.session.commit()

    def preposition(self, baseform):
        new_record = Preposition(baseform=baseform, en_translation="-")
        db.session.add(new_record)
        db.session.commit()

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
                print("Done!")
                print(response.request)
                break

            for result in scope:
                word = result.get("entry")
                pos = word.get("partOfSpeech")
                baseform = word.get("baseform")
                inflection_table = word.get("inflectionTable")
                if not inflection_table:
                    continue
                if pos.startswith("nn"):
                    self.noun(inflection_table, baseform)
                elif pos.startswith("av"):
                    self.adjective(inflection_table, baseform)
                elif pos.startswith("vb"):
                    self.verb(inflection_table, baseform)
                elif pos.startswith("ab"):
                    self.adverb(baseform)
                elif pos.startswith("pm"):
                    self.proper_noun(baseform)
                elif pos.startswith("nl"):
                    self.numeral(baseform)
                elif pos.startswith("in"):
                    self.interjection(baseform)
                elif pos.startswith("pp"):
                    self.preposition(baseform)
                else:
                    pass

            batch_from += batch_size

class GetTranslation:
    def __init__(self):
        self.url = "https://libretranslate.com/translate"
        self.databases = [Noun, Verb, Adverb, Adjective, ProperNoun, Numeral, Interjection, Preposition]

    def get_swedish_structure_from_db(self, word):
        pass

    def deepl_translation(self, word, source_lang, target_lang):
        try:
            translation_ob = translator.translate_text(word, source_lang=source_lang, target_lang=target_lang)
            translation_text = translation_ob.text
            flash("Congratulations! You've got a new word to learn.", category='success')
            print(translation_text)
            return translation_text
        except Exception as e:
            print(e)
            flash("Upsss, something went wrong. Please, try again.")

    def get_translation_db_sv_to_en(self, word):
        exist = None
        for database in self.databases:
            exist = database.query.filter(database.baseform == word).first()
            if exist:
                break
        if exist:
            if exist.en_translation == "-":
                translation = self.deepl_translation(word, "SV", "EN-US")
                exist.en_translation = translation
                db.session.commit()
            else:
                translation = exist.en_translation
        else:
            translation = self.deepl_translation(word, "SV", "EN-US")
        print(translation)

    def get_translation_db_en_to_sv(self, word):
        exist = db_source = None
        for database in self.databases:
            exist = database.query.filter(database.en_translation == word).first()
            db_source = database
            if exist:
                break
        if exist:
            column_names = [column.name for column in db_source.__table__.columns if column.name != "id"]
            data = {column : getattr(exist, column) for column in column_names}
        else:
            translation = self.deepl_translation(word, "EN", "SV")
            data = {"baseform" : translation, "en_translation" : word}
        return data

    def translation(self, language, word_to_translate):
        if language == "1":
            self.get_translation_db_sv_to_en(word_to_translate)
        elif language == "2":
            self.get_translation_db_en_to_sv(word_to_translate)
        else:
            pass

    # def existing_translation(self):
    #     existing_translation = True
    #     for database in self.databases:
    #         exist = database.query.filter(database.en_translation == "-")
    #         if exist:
    #             existing_translation = False
    #     return existing_translation


    # def get_word_to_translate(self, database):
    #     return database.query.filter(database.en_translation == "-")
    #
    # def translate(self):
    #     counter = 0
    #     for database in self.databases:
    #         scope = self.get_word_to_translate(database)
    #         for item in scope:
    #             if counter >= 100:
    #                 print("100 requests - done")
    #                 sleep(1)
    #                 counter = 0
    #             counter += 1
    #             word = item.baseform
    #             try:
    #                 en_translation_ob = translator.translate_text(word, source_lang="SV", target_lang="EN-US")
    #                 en_translation_text = en_translation_ob.text
    #                 item.en_translation = en_translation_text
    #                 db.session.commit()
    #             except deepl.exceptions.TooManyRequestsException:
    #                 print("TooManyRequestsException error")
    #                 break
    #             except Exception as e:
    #                 print(e)
