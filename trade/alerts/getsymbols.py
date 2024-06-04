import requests
import json
import csv
import re
from trade.models import bot_order_quantity

def get_quantity(user,symbol):
    print(user)
    print(symbol)
    qtyob = bot_order_quantity.objects.filter(user=user).first()
    qty = 0
    if 'CRUDEOIL' in symbol:
        qty = qtyob.crudeoil_quantity
    elif 'BANKNIFTY' in symbol:
        qty = qtyob.bank_nifty_quantity
    elif 'FINNIFTY' in symbol:
        qty = qtyob.fin_nifty_quantity
    elif 'NIFTY' in symbol:
        qty = qtyob.nifty_quantity
    elif 'SENSEX' in symbol:
        qty = qtyob.sensex_quantity
    elif 'BANKEX' in symbol:
        qty = qtyob.bankex_quantity
    else:
        qty = qtyob.quantity
        print(qty)
    return qty

def avg_price(number, n):
    return round(number / n) * n

def get_symbol(symbol):
    if 'CRUDEOIL' in symbol:
        return 'CRUDEOIL'
    if 'BANKEX' in symbol:
        return 'BANKEX'
    if 'SENSEX' in symbol:
        return 'SENSEX'
    match = re.match(r'(.*?)(\d{2}[A-Z]{3}\d+)', symbol)
    if match:
        result = match.group(1)
        return result
    else:
        return symbol

def create_csv():
    url = "https://margincalculator.angelbroking.com/OpenAPI_File/files/OpenAPIScripMaster.json"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        csv_filename = "SYMBOLS.csv"
        header = data[0].keys()
        with open(csv_filename, 'w', newline='') as csv_file:
            csv_writer = csv.DictWriter(csv_file, fieldnames=header)
            csv_writer.writeheader()
            csv_writer.writerows(data)
        print(f"CSV file '{csv_filename}' has been created successfully.")
    else:
        print(f"Failed to retrieve data. Status code: {response.status_code}")

def symbol_list():
    data = []
    with open('syb.csv', 'r', newline='') as csvfile:
        csvreader = csv.DictReader(csvfile)

        for row in csvreader:
            data.append(row)
    return data



def rename_columns(input_csv_file, output_csv_file):
    with open(input_csv_file, 'r', newline='') as csvfile_in, \
         open(output_csv_file, 'w', newline='') as csvfile_out:
        reader = csv.DictReader(csvfile_in)

        # Define the new column names
        fieldnames_out = reader.fieldnames
        fieldnames_out[fieldnames_out.index('Symbol')] = 'Trading Symbol'
        fieldnames_out[fieldnames_out.index('Trading Symbol')] = 'Symbol'

        writer = csv.DictWriter(csvfile_out, fieldnames=fieldnames_out)
        writer.writeheader()

        for row in reader:
            # Rename the columns
            renamed_row = {
                'Symbol': row['Trading Symbol'],
                'Trading Symbol': row['Symbol']
            }

            # Copy other fields as is
            for field in fieldnames_out:
                if field not in renamed_row:
                    renamed_row[field] = row[field]

            writer.writerow(renamed_row)

def csv_to_python_object():
    data = []
    with open('/home/smartalgo/tradingalgo/syb.csv', 'r', newline='') as csvfile:
        csvreader = csv.DictReader(csvfile)

        for row in csvreader:
            data.append(row)

    # with open('INDICES.csv', 'r', newline='') as csvfile:
    #     csvreader = csv.DictReader(csvfile)
    #     for row in csvreader:
    #         data.append(row)

    # # rename_columns('MCX.csv','newMCX.csv')
    # with open('newMCX.csv', 'r', newline='') as csvfile:
    #     csvreader = csv.DictReader(csvfile)
    #     for row in csvreader:
    #         data.append(row)

    # # rename_columns('NFO.csv','newNFO.csv')
    # with open('newNFO.csv', 'r', newline='') as csvfile:
    #     csvreader = csv.DictReader(csvfile)
    #     for row in csvreader:
    #         data.append(row)

    return data

def exc_symbols():
    data = csv_to_python_object()
    slist = {}
    for i in range(0,data.__len__()):
        temp = {"exchange":data[i]['exch_seg'],"token":data[i]['token']}
        symbol = data[i]['symbol']
        slist[symbol] = temp
    return slist
