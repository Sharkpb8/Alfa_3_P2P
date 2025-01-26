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