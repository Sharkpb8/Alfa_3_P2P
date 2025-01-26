import csv

def create_csv():
    with open("./Bank/Accounts.csv","w",newline='') as file:
        csvwriter = csv.writer(file)
        rows = ["account_number", "balance"]
        csvwriter.writerow(rows)

def save_csv(account_number, balance):
    with open("./Bank/Accounts.csv","a", newline='') as file:
        csvwriter = csv.writer(file)
        data = [account_number, balance]
        csvwriter.writerow(data)

def read_csv():
    with open("./Bank/Accounts.csv","r") as file:
        csvwriter = csv.reader(file)
        contents = []
        for rows in csvwriter:
            data = [rows[0],rows[1]]
            contents.append(data)
        return contents
    
def read_row_csv(account_number):
    with open("./Bank/Accounts.csv","r") as file:
        csvwriter = csv.reader(file)
        data = None
        for rows in csvwriter:
            if(rows[0] == account_number):
                data = rows[1]
        return data

def update_balance(account_number, balance):
    contents = []
    with open("./Bank/Accounts.csv","r", newline='') as f_read:
        csvread = csv.reader(f_read)
        for rows in csvread:
            if(rows[0] == account_number):
                data = [rows[0],balance]
            else:
                data = [rows[0],rows[1]]
            contents.append(data)
    with open("./Bank/Accounts.csv","w",newline='') as f_write:
        csvwriter = csv.writer(f_write)
        for i in contents:
            csvwriter.writerow(i)

def delete_accoun(account_number):
    contents = []
    with open("./Bank/Accounts.csv","r", newline='') as f_read:
        csvread = csv.reader(f_read)
        for rows in csvread:
            if(rows[0] != account_number):
                data = [rows[0],rows[1]]
                contents.append(data)
    with open("./Bank/Accounts.csv","w",newline='') as f_write:
        csvwriter = csv.writer(f_write)
        for i in contents:
            csvwriter.writerow(i)

def total_balance():
    balance = 0
    with open("./Bank/Accounts.csv","r") as file:
        csvreader = csv.reader(file)
        next(csvreader)
        for rows in csvreader:
            balance += int(rows[1])
        return balance

def number_of_clients():
    ammount = 0
    with open("./Bank/Accounts.csv","r") as file:
        csvreader = csv.reader(file)
        next(csvreader)
        for rows in csvreader:
            ammount += 1
        return ammount