#practice

import csv
#import request
import example_data
import json
from re import sub
from decimal import Decimal



response = json.loads(example_data.data)
#stuff = response.json()

parts = response['SearchResults']['Parts'][0]

#print(response['SearchResults']['Parts'][0]['Availability'])

qty = 14

#print(parts['PriceBreaks'][2]['Price'])

i = 0
x = parts['PriceBreaks']
while i < 4:
	if x[i]['Quantity'] < qty and x[i+1]['Quantity'] > qty:
		print(i)
		print(x[i]['Quantity'])
		print(x[i]['Price'])
	i += 1



with open('bom.csv', 'r') as csv_file:
	csv_reader = csv.reader(csv_file)

	with open('new_bom.csv', 'w') as new_file:
		csv_writer = csv.writer(new_file)

		firstPart = 'RC0603FR-07'
		lastPart = 'L'
		#value_index = 0
		#description_index = 0

		price = Decimal(0.006)

		for line in csv_reader:
			i = 0
			line_len = len(line)
			while i < line_len:

				ready_to_print = 0

				if line[i] == 'Value':
					value_index = i

				if line[i] == 'Description':
					description_index = i

				if line[i] == 'Part Number':
					part_number_index = i

				if line[i] == 'Quantity':
					quantity_index = i

				if line[i] == '0603R*':
					this_part_number = firstPart + line[value_index] + lastPart
					line[i] = this_part_number
					line[description_index] = line[value_index] + ",1%,1/10W,0603"
					ready_to_print = 1

				if ready_to_print == 1:
					qty = Decimal(sub(r'[^\d.]', '', line[quantity_index]))
					extended_cost = price * qty
					print(str(qty) + ': ' + this_part_number + ' = ' + '$' + "{:.3f}".format(extended_cost))

				i += 1

			csv_writer.writerow(line)


#with open('new_bom.csv', 'r') as new_file:
#	csv_reader = csv.reader(new_file)
#	for line in csv_reader:
#		print(line)

#firstPart = 'RC0603FR-07'
#resistance = '56K'
#lastPart = 'L'
#outputString = firstPart + resistance + lastPart


#print(outputString)