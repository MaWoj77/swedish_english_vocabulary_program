import json
import httpx

class GetWord:
    def __init__(self):
        self.url = "https://spraakbanken4.it.gu.se/karp/v7/query/saldom"
    def noun(self):

        params = {
            "resource": "saldom",
            "sort": ["partOfSpeech"],
            # "query" : "hund",
            "size" : 100,
            "from" : 9000
        }
        response = httpx.get(self.url, params=params)
        j_response = json.load(response)
        scope = j_response["hits"]
        # print(scope)
        for result in scope:
            word = result.get("entry")
            if word.get("partOfSpeech") == "nn":
                print(word.get("baseform"))
                print(word.get("partOfSpeech"))
                print(word.get("inflectionTable"))

try_this = GetWord()
try_this.noun()
"""https://spraakbanken.gu.se/karp/?mode=saldom&lexicon=saldom&show=saldom:01HQMY8726SN5W354RSWEV9DFQ&tab=json&filter="""

# res = "https://spraakbanken4.it.gu.se/karp/v7/resources/"
#"https://spraakbanken4.it.gu.se/karp/v7/query/saldom"
# reso = httpx.get(res)
# resors = json.load(reso)
# print(resors)