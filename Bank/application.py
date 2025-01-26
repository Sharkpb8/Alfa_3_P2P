from filemanager import *
import os
import random

class application():
    def __init__(self,client):
        self.client = client
    
    def Account_create(self,parametrs = None):
        if not parametrs:
            if(not os.path.isfile("./Bank/Accounts.csv")):
                create_csv()
            contents = read_csv()
            existing_accounts = []
            for i in contents:
                existing_accounts.append(i[0])
            try:
                new_account = random.choice([i for i in range(10000,100000) if i not in existing_accounts])
            except IndexError:
                self.client.send_message("ER Již nelze vytvořit učty")
            else:
                save_csv(new_account,0)
                self.client.send_message(f"AC {new_account}/{self.client.server_ip}")
        else:
            self.client.send_message("ER Příkaz má mít formát: AC")