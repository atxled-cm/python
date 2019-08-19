# practice functions

import example_data


class Mouser(object):
	def getPrice(self):
		return '0.006'
	def getParts(self):
		response = json.loads(example_data.data)
		return response['SearchResults']['Parts'][0]