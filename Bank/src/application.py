from src.filemanager import *
import os
import random
from src.Account.AccountDAO import AccountDAO
from src.Account.Account import Account

class application():
    def __init__(self,client):
        self.client = client
        self.table_DAO = AccountDAO(self)
    
    def Account_create(self,parametrs = None):
        if(parametrs):
            return self.client.send_message("ER Příkaz má mít formát: AC")
        
        existing_accounts = self.table_DAO.Read_account_number()
        if(not existing_accounts):
            existing_accounts = []
        try:
            new_account = random.choice([i for i in range(10000,100000) if i not in existing_accounts])
        except IndexError:
            self.client.send_message("ER Již nelze vytvořit účty")
        else:
            a = Account(new_account,0)
            self.table_DAO.Save(a)
            self.client.send_message(f"AC {new_account}/{self.client.server_ip}")

    def Account_deposit(self,parametrs):
        if(self.Check_parametrs(parametrs,"AD <account>/<ip> <number>",True)):
            split_parametrs = parametrs.split("/",maxsplit=1)
            a = Account(split_parametrs[0],0)
            a.Balance = self.table_DAO.Read_balance(a.Account_number)
            if(a.Balance == None):
                return self.client.send_message("ER Účet neexistuje")
            split_split_parametrs = split_parametrs[1].split(maxsplit=1)
            if((a.Balance+int(split_split_parametrs[1]))>(2**63)-1):
               return self.client.send_message("ER Částka na účtu nemůže být větší než (2**63)-1")
            a.Balance += int(split_split_parametrs[1])
            self.table_DAO.Update(a)
            self.client.send_message(f"AD")
    
    def Account_withdrawal(self,parametrs):
        if(self.Check_parametrs(parametrs,"AW <account>/<ip> <number>",True)):
            split_parametrs = parametrs.split("/",maxsplit=1)
            a = Account(split_parametrs[0],0)
            a.Balance = self.table_DAO.Read_balance(a.Account_number)
            if(a.Balance == None):
                return self.client.send_message("ER Účet neexistuje")
            split_split_parametrs = split_parametrs[1].split(maxsplit=1)
            if((a.Balance-int(split_split_parametrs[1]))<0):
               return self.client.send_message("ER Částka na účtu nemůže být negativní")
            a.Balance -= int(split_split_parametrs[1])
            self.table_DAO.Update(a)
            self.client.send_message(f"AW")

    def Account_balance(self,parametrs):
        if(self.Check_parametrs(parametrs,"AB <account>/<ip>")):
            split_parametrs = parametrs.split("/",maxsplit=1)
            balance = self.table_DAO.Read_balance(split_parametrs[0])
            if(balance == None):
                return self.client.send_message("ER Účet neexistuje")
            self.client.send_message(f"AB {balance}")

    def Account_remove(self,parametrs):
        if(self.Check_parametrs(parametrs,"AR <account>/<ip>")):
            split_parametrs = parametrs.split("/",maxsplit=1)
            balance = self.table_DAO.Read_balance(split_parametrs[0])
            if(balance == None):
                return self.client.send_message("ER Účet neexistuje")
            if(balance>0):
                return self.client.send_message("ER Účet nelze smazat protože obsahuje zůstatek")
            self.table_DAO.Delete(split_parametrs[0])
            self.client.send_message(f"AR")
    
    def Bank_amount(self,parametrs):
        if(parametrs):
            return self.client.send_message("ER Příkaz má mít formát: BA")
        
        if(not os.path.isfile("./Bank/Accounts.csv")):
            create_csv()
        self.client.send_message(f"BA {total_balance()}")

    def Bank_number(self,parametrs):
        if(parametrs):
            return self.client.send_message("ER Příkaz má mít formát: BN")
        
        if(not os.path.isfile("./Bank/Accounts.csv")):
            create_csv()
        self.client.send_message(f"BN {number_of_clients()}")
        
    def Check_parametrs(self,parametrs,format,ammount = False):
        if(not parametrs):
            self.client.send_message(f"ER Příkaz má mít formát: {format}")
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
        
