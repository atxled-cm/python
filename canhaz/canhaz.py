import csv
import example_data
import json
from re import sub
from decimal import Decimal
import mouser
import time


def find_price(_quantity, _part_number):

    output_info = {'Quantity': 0, 'Tier:': 0, 'Price': 0, 'Extended Price': "{:.3f}".format(0)}

    parts = mouser.get_web_parts(_part_number)
    #parts = mouser.get_example_parts(_part_number)
    if 'Availability' in parts:
        #print('got availability')
        #print("yes!")
        i = 0
        x = parts['PriceBreaks']
        while i < 4:

#yo this would break at 1000 or more
            if x[i]['Quantity'] <= _quantity and x[i+1]['Quantity'] > _quantity:
                quantity_tier = x[i]['Quantity']
                price_at_quantity = float(x[i]['Price'].strip('$'))
                extended_price = price_at_quantity * _quantity
                output_info = {'Quantity': _quantity, 'Tier:': quantity_tier, 'Price': "{:.3f}".format(price_at_quantity), 'Extended Price': "{:.3f}".format(extended_price)}
                #return [_quantity, quantity_tier, price_at_quantity, extended_price]
                #return output_info
                #print(price_at_quantity_results)
            i += 1
    return output_info


#product_info = find_price(150, "PMV55ENEAR")
#print('Price: ' + str(product_info['Price']))
#print('Extended Price: ' + str(product_info['Extended Price']))


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
                    #print(str(qty) + ' * ' + this_part_number + ' = ' + '$' + "{:.3f}".format(extended_cost))

                i += 1

            csv_writer.writerow(line)

with open('new_bom.csv', 'r') as csv_file:
    csv_reader = csv.DictReader(csv_file)

    total_cost = 0.0

    for row in csv_reader: 
        this_part = row['Part Number']
        this_quantity = float(row['Quantity'])
        #print(this_quantity)
        #print(this_part)
        time.sleep(2.0)
        product_info = find_price(this_quantity, this_part)
        total_cost += float(product_info['Extended Price'])
        
        if 'Extended Price' in product_info:
            #output = '$' + str(product_info['Extended Price']) + ' - ' + this_part
            output = 'qty: ' + str(int(product_info['Quantity'])) + "   " + '$' + str(product_info['Extended Price']) + "   " + this_part
            print(output)
        else:
            print(this_part)

    print('Total BOM cost from mouser = ' + '$' + str(total_cost))






