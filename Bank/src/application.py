import random
from src.Account.AccountDAO import AccountDAO
from src.Account.Account import Account
from src.logging import log
from src.error import *
import socket

class application():
    def __init__(self,client):
        self.client = client
        self.table_DAO = AccountDAO(self)
    
    @log
    def Account_create(self,parametrs = None):
        try:
            if(parametrs):
                raise ParametrsError
            existing_accounts = self.table_DAO.Read_account_number()
            if(not existing_accounts):
                existing_accounts = []
            new_account = random.choice([i for i in range(10000,100000) if i not in existing_accounts])
        except ParametrsError:
            self.client.send_message("ER Příkaz má mít formát: AC")
        except IndexError:
            self.client.send_message("ER Již nelze vytvořit účty")
        else:
            a = Account(new_account,0)
            self.table_DAO.Save(a)
            return self.client.send_message(f"AC {new_account}/{self.client.server_ip}")

    @log
    def Account_deposit(self,parametrs):
        account,ip,number = self.parse_parametrs(parametrs)
        try:
            self.Check_parametrs(account,ip,number)
            a = Account(account,0)
            a.Balance = self.table_DAO.Read_balance(a.Account_number)
            if(a.Balance == None):
                raise AccountDoestnExistError
            if((a.Balance+int(number))>(2**63)-1):
                raise NumberLimitError
            a.Balance += int(number)
        except ParametrsError:
            self.client.send_message(f"ER Příkaz má mít formát: AD <account>/<ip> <number>")
        except IpV4Error:
            self.client.send_message("ER Špatný formát ip addresy")
        except NotImplementedError:
            self.client.send_message("Není implementovaný")
        except NumberError:
            self.client.send_message("ER number musí být nezáporný číslo")
        except AccountDoestnExistError:
            self.client.send_message("ER Účet neexistuje")
        except NumberLimitError:
            self.client.send_message("ER Částka na účtu nemůže být větší než (2**63)-1")
        else:
            self.table_DAO.Update(a)
            return self.client.send_message(f"AD")
    
    @log
    def Account_withdrawal(self,parametrs):
        account,ip,number = self.parse_parametrs(parametrs)
        try:
            self.Check_parametrs(account,ip,number)
            a = Account(account,0)
            a.Balance = self.table_DAO.Read_balance(a.Account_number)
            if(a.Balance == None):
                raise AccountDoestnExistError
            if((a.Balance-int(number))<0):
                raise NegativeBalanceError
            a.Balance -= int(number)
        except ParametrsError:
            self.client.send_message(f"ER Příkaz má mít formát: AW <account>/<ip> <number>")
        except IpV4Error:
            self.client.send_message("ER Špatný formát ip addresy")
        except NotImplementedError:
            self.client.send_message("Není implementovaný")
        except NumberError:
            self.client.send_message("ER number musí být nezáporný číslo")
        except AccountDoestnExistError:
            self.client.send_message("ER Účet neexistuje")
        except NegativeBalanceError:
            self.client.send_message("ER Částka na účtu nemůže být negativní")
        else:
            self.table_DAO.Update(a)
            return self.client.send_message(f"AW")

    @log
    def Account_balance(self,parametrs):
        account,ip,number = self.parse_parametrs(parametrs)
        try:
            if(number):
                number = None
            else:
                number = "2" 
            self.Check_parametrs(account,ip,number)
            balance = self.table_DAO.Read_balance(account)
            if(balance == None):
                raise AccountDoestnExistError
        except ParametrsError:
            self.client.send_message(f"ER Příkaz má mít formát: AB <account>/<ip>")
        except IpV4Error:
            self.client.send_message("ER Špatný formát ip addresy")
        except NotImplementedError:
            response = self.forward_command(account,ip,number,"AB")
            return self.client.send_message(f"{response}")
        except AccountDoestnExistError:
            self.client.send_message("ER Účet neexistuje")
        else:
            return self.client.send_message(f"AB {balance}")

    @log
    def Account_remove(self,parametrs):
        account,ip,number = self.parse_parametrs(parametrs)
        try:
            if(number):
                number = None
            else:
                number = "2"
            self.Check_parametrs(account,ip,number)
            balance = self.table_DAO.Read_balance(account)
            if(balance == None):
                raise AccountDoestnExistError
            if(balance>0):
                raise AccountRemovalError
        except ParametrsError:
            self.client.send_message(f"ER Příkaz má mít formát: AR <account>/<ip>")
        except IpV4Error:
            self.client.send_message("ER Špatný formát ip addresy")
        except NotImplementedError:
            self.client.send_message("Není implementovaný")
        except AccountDoestnExistError:
            self.client.send_message("ER Účet neexistuje")
        except AccountRemovalError:
            self.client.send_message("ER Účet nelze smazat protože obsahuje zůstatek")
        else:
            self.table_DAO.Delete(account)
            return self.client.send_message(f"AR")
    
    @log
    def Bank_amount(self,parametrs):
        try:
            if(parametrs):
                raise ParametrsError
        except ParametrsError:
            self.client.send_message("ER Příkaz má mít formát: BA")
        else:
            self.client.send_message(f"BA {self.table_DAO.Read_Bank_amount()}")

    @log
    def Bank_number(self,parametrs):
        try:
            if(parametrs):
                raise ParametrsError
        except ParametrsError:
            self.client.send_message("ER Příkaz má mít formát: BN")
        else:
            self.client.send_message(f"BN {self.table_DAO.Read_Bank_number()}")
        
    def Check_parametrs(self,account,ip,number):
        if(not (account and ip and number)):
            raise ParametrsError
        if(self.is_invalid_ipv4(ip)):
            raise IpV4Error
        if(ip != self.client.server_ip):
            raise NotImplementedError
        if(not number.isdigit()):
            raise NumberError
        if(int(number)<0):
            raise NumberError

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
        
    def parse_parametrs(self,parametrs):
        try:
            split_parametrs = parametrs.split("/",maxsplit=1)
            split_split_parametrs = split_parametrs[1].split(maxsplit=1)
        except IndexError:
            return None,None,None
        else:
            try:
                account = split_parametrs[0]
            except IndexError:
                account = None
            try:
                ip = split_split_parametrs[0]
            except IndexError:
                ip= None
            try:
                number = split_split_parametrs[1]
            except IndexError:
                number = None
            return account,ip,number
    
    def forward_command(self,account,ip,number,code):
        try:
            for i in range(65525,65536):
                try:
                    server_inet_address = (ip, i)
                    remote_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                    remote_socket.connect((ip, i))
                    break
                except socket.error:
                    print(i)
                    pass
            else:
                return None
        except Exception as e:
            print(e)
            return None
        else:
            command = f"{code} {account}/{ip} {'' if number is None else number}\r\n"
            print(command)
            remote_socket.sendall(command.encode("utf-8"))

            response = remote_socket.recv(4096).decode()
            remote_socket.close()
            return response