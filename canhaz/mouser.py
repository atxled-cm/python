#function stuff for mouser api

import example_data
import json
import requests

def get_price():
	return '0.006'
def get_example_parts(_part_number):
	response = json.loads(example_data.data)
	return response['SearchResults']['Parts'][0]

def get_web_parts(_part_number):
	#print(_part_number)
	headers = {
    'accept': 'application/json',
    'Content-Type': 'application/json',
	}

	params = (('apiKey', '9b8429d2-569a-4def-ac9a-feec7144eff8'),)
	data = '{ "SearchByPartRequest": { "mouserPartNumber": "' + _part_number + '", "partSearchOptions": "string" }}'
	#print(data)
	response = requests.post('https://api.mouser.com/api/v1/search/partnumber',headers=headers, params=params, data=data).json();
	if 'SearchResults' in response:
		if response['SearchResults'] == None:
			print("search results = none")
			return {'Error':'Result None'}
			#print(response)
		else:
			if response['SearchResults']['NumberOfResult'] != 0:
				#print(response)
				return response['SearchResults']['Parts'][0]
			else:
				print("problem!")
				#print(response)
				return {'Error':'No Stuff Here'}
	else:
		return {'Error':'No Stuff Here'}

	#print(response)
