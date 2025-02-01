import random
from src.Account.AccountDAO import AccountDAO
from src.Account.Account import Account
from src.logging import log
from src.error import *
import socket
from src.RobberyPlan import RobberyPlan
from mysql.connector.errors import *

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
            a = Account(new_account,0)
            self.table_DAO.Save(a)
        except ParametrsError:
            return "ER Příkaz má mít formát: AC"
        except IndexError:
            return "ER Již nelze vytvořit účty"
        except DatabaseError:
            return f"ER Připojení k databázi selhalo"
        else:
            return f"AC {new_account}/{self.client.server_ip}"

    @log
    def Account_deposit(self,parametrs):
        try:
            account,ip,number = self.parse_parametrs(parametrs)
            self.Check_parametrs(account,ip,number)
            a = Account(account,0)
            a.Balance = self.table_DAO.Read_balance(a.Account_number)
            if(a.Balance == None):
                raise AccountDoestnExistError
            if((a.Balance+int(number))>(2**63)-1):
                raise NumberLimitError
            a.Balance += int(number)
            self.table_DAO.Update(a)
        except ParametrsError:
            return f"ER Příkaz má mít formát: AD <account>/<ip> <number>"
        except IpV4Error:
            return "ER Špatný formát ip addresy"
        except NotServerIpError:
            response = self.forward_command(account,ip,number,"AD")
            if(not response):
                return f"ER S bankou na {ip} se nepodařilo spojit"
            return f"{response}"
        except NumberError:
            return "ER number musí být nezáporný číslo"
        except AccountDoestnExistError:
            return "ER Účet neexistuje"
        except NumberLimitError:
            return "ER Částka na účtu nemůže být větší než (2**63)-1"
        except DatabaseError:
            return f"ER Připojení k databázi selhalo"
        else:
            return f"AD"
    
    @log
    def Account_withdrawal(self,parametrs):
        try:
            account,ip,number = self.parse_parametrs(parametrs)
            self.Check_parametrs(account,ip,number)
            a = Account(account,0)
            a.Balance = self.table_DAO.Read_balance(a.Account_number)
            if(a.Balance == None):
                raise AccountDoestnExistError
            if((a.Balance-int(number))<0):
                raise NegativeBalanceError
            a.Balance -= int(number)
            self.table_DAO.Update(a)
        except ParametrsError:
            return f"ER Příkaz má mít formát: AW <account>/<ip> <number>"
        except IpV4Error:
            return "ER Špatný formát ip addresy"
        except NotServerIpError:
            response = self.forward_command(account,ip,number,"AW")
            if(not response):
                return f"ER S bankou na {ip} se nepodařilo spojit"
            return f"{response}"
        except NumberError:
            return "ER number musí být nezáporný číslo"
        except AccountDoestnExistError:
            return "ER Účet neexistuje"
        except NegativeBalanceError:
            return "ER Částka na účtu nemůže být negativní"
        except DatabaseError:
            return f"ER Připojení k databázi selhalo"
        else:
            return f"AW"

    @log
    def Account_balance(self,parametrs):
        try:
            account,ip,number = self.parse_parametrs(parametrs)
            if(number):
                number = None
            self.Check_parametrs(account,ip,number,False)
            balance = self.table_DAO.Read_balance(account)
            if(balance == None):
                raise AccountDoestnExistError
        except ParametrsError:
            return f"ER Příkaz má mít formát: AB <account>/<ip>"
        except IpV4Error:
            return "ER Špatný formát ip addresy"
        except NotServerIpError:
            response = self.forward_command(account,ip,number,"AB")
            if(not response):
                return f"ER S bankou na {ip} se nepodařilo spojit"
            return f"{response}"
        except AccountDoestnExistError:
            return "ER Účet neexistuje"
        except DatabaseError:
            return f"ER Připojení k databázi selhalo"
        else:
            return f"AB {balance}"

    @log
    def Account_remove(self,parametrs):
        try:
            account,ip,number = self.parse_parametrs(parametrs)
            if(number):
                number = None
            self.Check_parametrs(account,ip,number,False)
            balance = self.table_DAO.Read_balance(account)
            if(balance == None):
                raise AccountDoestnExistError
            if(balance>0):
                raise AccountRemovalError
            self.table_DAO.Delete(account)
        except ParametrsError:
            return f"ER Příkaz má mít formát: AR <account>/<ip>"
        except IpV4Error:
            return "ER Špatný formát ip addresy"
        except AccountDoestnExistError:
            return "ER Účet neexistuje"
        except AccountRemovalError:
            return "ER Účet nelze smazat protože obsahuje zůstatek"
        except DatabaseError:
            return f"ER Připojení k databázi selhalo"
        else:
            return f"AR"
    
    @log
    def Bank_amount(self,parametrs):
        try:
            if(parametrs):
                raise ParametrsError
            BA = self.table_DAO.Read_Bank_amount()
        except ParametrsError:
            return "ER Příkaz má mít formát: BA"
        except DatabaseError:
            return f"ER Připojení k databázi selhalo"
        else:
            return f"BA {BA}"

    @log
    def Bank_number(self,parametrs):
        try:
            if(parametrs):
                raise ParametrsError
            BN = self.table_DAO.Read_Bank_number()
        except ParametrsError:
            return "ER Příkaz má mít formát: BN"
        except DatabaseError:
            return f"ER Připojení k databázi selhalo"
        else:
            return f"BN {BN}"

    @log
    def Robbery_plan(self,parametrs):
        try:
            if(not parametrs):
                raise ParametrsError
            if(not parametrs.isdigit()):
                raise ParametrsError
            rp = RobberyPlan(self.client.server_ip)
            addresses = rp.available_servers()
            banks = rp.banks_info(addresses)
            result = rp.best_combination(banks,int(parametrs))
        except ParametrsError:
            return "ER Příkaz má mít formát: RP <number>"
        except DatabaseError:
            return f"ER Připojení k databázi selhalo"
        else:
            return result
        
    def Check_parametrs(self,account,ip,number,check_number = True):
        if(check_number):
            if(not (account and ip and number)):
                raise ParametrsError
        else:
            if(not (account and ip)):
                raise ParametrsError
        if(self.is_invalid_ipv4(ip)):
            raise IpV4Error
        if(ip != self.client.server_ip):
            raise NotServerIpError
        if(check_number):
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
        except AttributeError:
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
        working_port = None
        try:
            for i in range(65525,65536):
                try:
                    server_inet_address = (ip, i)
                    remote_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                    remote_socket.settimeout(0.1)
                    remote_socket.connect(server_inet_address)
                    working_port = i
                    remote_socket.close()
                    break
                except socket.error:
                    print(i)
                    pass
            else:
                raise socket.error
        except socket.error:
            return None
        else:
            server_inet_address = (ip, working_port)
            remote_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            remote_socket.connect(server_inet_address)
            command = f"{code} {account}/{ip} {'' if number is None else number}\r\n"
            remote_socket.sendall(command.encode("utf-8"))

            response = remote_socket.recv(4096).decode().strip()
            remote_socket.close()
            return response
                