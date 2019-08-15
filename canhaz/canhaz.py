import requests
import json

class DictQuery(dict):
    def get(self, path, default = None):
        keys = path.split("/")
        val = None

        for key in keys:
            if val:
                if isinstance(val, list):
                    val = [ v.get(key, default) if v else None for v in val]
                else:
                    val = val.get(key, default)
            else:
                val = dict.get(self, key, default)

            if not val:
                break;

        return val

headers = {
    'accept': 'application/json',
    'Content-Type': 'application/json',
}

params = (
    ('apiKey', '9b8429d2-569a-4def-ac9a-feec7144eff8'),
)

data = '{ "SearchByPartRequest": { "mouserPartNumber": "RC0603FR-07200KL", "partSearchOptions": "string" }}'

response = requests.post('https://api.mouser.com/api/v1/search/partnumber', headers=headers, params=params, data=data)

#stuff = response.json()
stuff = json.loads(response)

print(stuff['SearchResults']['Parts']);




#NB. Original query string below. It seems impossible to parse and
#reproduce query strings 100% accurately so the one below is given
#in case the reproduced version is not "correct".
# response = requests.post('https://api.mouser.com/api/v1/search/partnumber?apiKey=9b8429d2-569a-4def-ac9a-feec7144eff8', headers=headers, data=data)