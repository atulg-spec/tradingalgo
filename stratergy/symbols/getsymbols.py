import csv

def csv_to_python_object():
    data = []
    with open('complete.csv', 'r', newline='') as csvfile:
        csvreader = csv.DictReader(csvfile)
        
        for row in csvreader:
            data.append(row)
    return data

def exc_symbols():
    data = csv_to_python_object()
    slist = {}
    for i in range(0,data.__len__()):
        temp = {"exchange":data[i]['exchange'],"token":data[i]['exchange_token']}
        symbol = data[i]['tradingsymbol']
        slist[symbol] = temp

    slist['Nifty Bank'] = {"exchange":"NSE","token":"99926009"}
    slist['Nifty 50'] = {"exchange":"NSE","token":"99926000"}
    return slist