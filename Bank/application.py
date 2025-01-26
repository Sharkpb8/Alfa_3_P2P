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

    def Account_deposit(self,parametrs):
        if(self.Check_parametrs(parametrs,"AD <account>/<ip> <number>",True)):
            split_parametrs = parametrs.split("/",maxsplit=1)
            balance = read_row_csv(split_parametrs[0])
            if(balance == None):
                return self.client.send_message("ER Účet neexistuje")
            balance = int(balance)
            split_split_parametrs = split_parametrs[1].split(maxsplit=1)
            if((balance+int(split_split_parametrs[1]))>(2**63)-1):
               return self.client.send_message("ER Částka na účtu nemůže být větší než (2**63)-1")
            balance += int(split_split_parametrs[1])
            update_balance(split_parametrs[0],balance)
            self.client.send_message(f"AD")
    
    def Account_withdrawal(self,parametrs):
        if(self.Check_parametrs(parametrs,"AW <account>/<ip> <number>",True)):
            split_parametrs = parametrs.split("/",maxsplit=1)
            balance = read_row_csv(split_parametrs[0])
            if(balance == None):
                return self.client.send_message("ER Účet neexistuje")
            balance = int(balance)
            split_split_parametrs = split_parametrs[1].split(maxsplit=1)
            if((balance-int(split_split_parametrs[1]))<0):
               return self.client.send_message("ER Částka na účtu nemůže být negativní")
            balance -= int(split_split_parametrs[1])
            update_balance(split_parametrs[0],balance)
            self.client.send_message(f"AW")

    def Account_balance(self,parametrs):
        if(self.Check_parametrs(parametrs,"AB <account>/<ip>")):
            split_parametrs = parametrs.split("/",maxsplit=1)
            balance = read_row_csv(split_parametrs[0])
            if(balance == None):
                return self.client.send_message("ER Účet neexistuje")
            self.client.send_message(f"AB {balance}")

    def Account_remove(self,parametrs):
        if(self.Check_parametrs(parametrs,"AR <account>/<ip>")):
            split_parametrs = parametrs.split("/",maxsplit=1)
            balance = read_row_csv(split_parametrs[0])
            if(balance == None):
                return self.client.send_message("ER Účet neexistuje")
            if(int(balance)>0):
                return self.client.send_message("ER Účet nelze smazat protože není prázdný")
            delete_accoun(split_parametrs[0])
            self.client.send_message(f"AR")
        
    def Check_parametrs(self,parametrs,format,ammount = False):
        if(not parametrs):
            self.client.send_message(f"ER Příkaz má mít formát: {format}")
            return False
        if(not os.path.isfile("./Bank/Accounts.csv")):
            self.client.send_message("ER Účet neexistuje")
            return False
        split_parametrs = parametrs.split("/",maxsplit=1)
        if(len(split_parametrs) != 2):
            self.client.send_message(f"ER Příkaz má mít formát: {format}")
            return False
        if(ammount):
            split_split_parametrs = split_parametrs[1].split(maxsplit=1)
            if(self.is_invalid_ipv4(split_split_parametrs[0])):
                self.client.send_message("ER Špatný formát ip addresy")
                return False
            if(split_split_parametrs[0] != self.client.server_ip):
                self.client.send_message("Není implementovaný")
                return False
            try:
                number = int(split_split_parametrs[1])
                if(number<0):
                    return False
            except ValueError:
                return False
        else:
            if(self.is_invalid_ipv4(split_parametrs[1])):
                self.client.send_message("ER Špatný formát ip addresy")
                return False
            if(split_parametrs[1] != self.client.server_ip):
                self.client.send_message("Není implementovaný")
                return False
        return True

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
        
