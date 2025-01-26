from filemanager import *
import os
import random

class application():
    def __init__(self,client):
        self.client = client
    
    def Account_create(self,parametrs = None):
        if(parametrs):
            return self.client.send_message("ER Příkaz má mít formát: AC")
        
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
            
    
    def Account_balance(self,parametrs):
        if(not parametrs):
            return self.client.send_message("ER Příkaz má mít formát: AB <account>/<ip>")
        if(not os.path.isfile("./Bank/Accounts.csv")):
            return self.client.send_message("ER Účet neexistuje")
        split_parametrs = parametrs.split("/",maxsplit=1)
        if(len(split_parametrs) != 2):
            return self.client.send_message("ER Příkaz má mít formát: AB <account>/<ip>")
        balance = read_row_csv(split_parametrs[0])
        if(not balance):
            return self.client.send_message("ER Účet neexistuje")
        if(self.is_invalid_ipv4(split_parametrs[1])):
            return self.client.send_message("ER Špatná formát ip addresy")
        if(split_parametrs[1] != self.client.server_ip):
            return self.client.send_message("Není implementovaný")
        self.client.send_message(f"AB {balance}")
        
    def is_invalid_ipv4(self,ip):
        parts = ip.split(".")
        if (len(parts) != 4):
            return True
        try:
            for part in parts:
                num = int(part)
                if num < 0 or num > 255:
                    return True
                if len(part) > 1 and part[0] == "0":
                    return True
        except ValueError:
            return True
        else:
            return False
        
