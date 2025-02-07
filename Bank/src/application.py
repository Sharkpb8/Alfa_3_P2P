import random
from src.Account.AccountDAO import AccountDAO
from src.Account.Account import Account
from src.logging import log
from src.error import *
import socket
from src.RobberyPlan import RobberyPlan
from mysql.connector.errors import *
import json

class application():
    """
    The Application class manages banking operations such as account creation, deposits, withdrawals, and balance inquiries.

    Attributes
    ----------
    client : Client
        The client associated with the application.
    table_DAO : AccountDAO
        Data Access Object for handling account operations.

    Methods
    -------
    Account_create(parameters=None)
        Creates a new bank account with a unique number.
    Account_deposit(parameters)
        Deposits an amount into an account.
    Account_withdrawal(parameters)
        Withdraws an amount from an account.
    Account_balance(parameters)
        Retrieves the balance of a specified account.
    Account_remove(parameters)
        Removes an account if it has no remaining balance.
    Bank_amount(parameters)
        Retrieves the total balance held by the bank.
    Bank_number(parameters)
        Retrieves the number of accounts in the bank.
    Robbery_plan(parameters)
        Calculates the best banks to rob to get closest to specific ammount while robbing least clients.
    Check_parametrs(account, ip, number, check_number=True)
        Validates account operation parameters.
    is_invalid_ipv4(ip)
        Checks whether a given IP address is a valid IPv4 address.
    parse_parametrs(parameters)
        Parses input parameters into account number, IP address, and amount.
    forward_command(account, ip, number, code)
        Forwards a command to another bank server.
    """
    def __init__(self,client):
        """
        Initialises the application, linking it to a client and setting up database access.

        Parameters
        ----------
        client : Client
            The client instance associated with this application.

        Examples
        --------
        >>> app = Application(client)
        """
        self.client = client
        self.table_DAO = AccountDAO(self)

    @log
    def Bank_Code(self,parametrs):
        """
        Returns the bank code (server IP address) or an error message if incorrect parameters are provided.

        Parameters
        ----------
        parameters : str, optional
            Additional parameters (should be None).

        Examples
        --------
        >>> client.Bank_Code()
        BC 192.168.1.1
        >>> client.Bank_Code("extra")
        ER Příkaz má mít formát: BC
        """
        try:
            if(parametrs):
                    raise ParametrsError
        except ParametrsError:
            return "ER Příkaz má mít formát: BC"
        else:
            return f"BC {self.client.server_ip}"
    
    @log
    def Account_create(self,parametrs = None):
        """
        Creates a new bank account with a unique number.

        Parameters
        ----------
        parameters : None
            No parameters should be provided; otherwise, an error is raised.

        Returns
        -------
        str
            A success message with the new account number or an error message.

        Examples
        --------
        >>> app.Account_create()
        'AC 12345/192.168.1.1'
        >>> app.Account_create("extra")
        'ER Příkaz má mít formát: AC'
        """
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
        """
        Deposits an amount into an account.

        Parameters
        ----------
        parameters : str
            The command format: "AD <account>/<ip> <amount>".

        Returns
        -------
        str
            A success message or an error message.

        Examples
        --------
        >>> app.Account_deposit("12345/192.168.1.1 500")
        'AD'
        >>> app.Account_deposit("invalid/192.168.1.1 -500")
        'ER number musí být nezáporný číslo'
        """
        try:
            account,ip,number = self.parse_parametrs(parametrs)
            self.Check_parametrs(account,ip,number)
            a = Account(account,0)
            a.Balance = self.table_DAO.Read_balance(a.Account_number)
            if(a.Balance == None):
                raise AccountDoestnExistError
            # TODO add isdigit() to number
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
        """
        Withdraws an amount from an account.

        Parameters
        ----------
        parameters : str
            The command format: "AW <account>/<ip> <amount>".

        Returns
        -------
        str
            A success message or an error message.

        Examples
        --------
        >>> app.Account_withdrawal("12345/192.168.1.1 100")
        'AW'
        >>> app.Account_withdrawal("12345/192.168.1.1 10000")
        'ER Částka na účtu nemůže být negativní'
        """
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
        """
        Retrieves the balance of a specified account.

        Parameters
        ----------
        parameters : str
            The command format: "AB <account>/<ip>".

        Returns
        -------
        str
            The account balance or an error message.

        Examples
        --------
        >>> app.Account_balance("12345/192.168.1.1")
        'AB 1500'
        >>> app.Account_balance("99999/192.168.1.1")
        'ER Účet neexistuje'
        """
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
        """
        Removes an account if it has no remaining balance.

        Parameters
        ----------
        parameters : str
            The command format: "AR <account>/<ip>".

        Returns
        -------
        str
            A success message or an error message.

        Examples
        --------
        >>> app.Account_remove("12345/192.168.1.1")
        'AR'
        >>> app.Account_remove("67890/192.168.1.1")
        'ER Účet nelze smazat protože obsahuje zůstatek'
        """
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
        """
        Retrieves the total balance held by the bank.

        Parameters
        ----------
        parameters : str
            Should be None; otherwise, an error is returned.

        Returns
        -------
        str
            The total balance or an error message.

        Examples
        --------
        >>> app.Bank_amount()
        'BA 500000'
        """
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
        """
        Retrieves the number of accounts in the bank.

        Parameters
        ----------
        parameters : str
            Should be None; otherwise, an error is returned.

        Returns
        -------
        str
            The number of accounts or an error message.

        Examples
        --------
        >>> app.Bank_number()
        'BN 150'
        """
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
        """
        Calculates the best banks to rob to get closest to specific ammount while robbing least clients.

        Parameters
        ----------
        parameters : str
            The amount to be stolen.

        Returns
        -------
        str
            The best robbery plan or an error message.

        Examples
        --------
        >>> app.Robbery_plan("10000")
        'RP Nejbližší částka k dosažení 10000 je 1100 a bude třeba vyloupit banky 192.168.1.19 192.168.1.45 a bude poškozeno 26 klientů.'
        >>> app.Robbery_plan("invalid")
        'ER Příkaz má mít formát: RP <number>'
        """
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
        """
        Validates account operation parameters.

        Parameters
        ----------
        account : str
            The account number.
        ip : str
            The IP address.
        number : str or None
            The transaction amount, if applicable.
        check_number : bool, optional
            Whether to validate the transaction amount (default is True).

        Raises
        ------
        ParametrsError
            If required parameters are missing.
        IpV4Error
            If the IP address format is incorrect.
        NotServerIpError
            If the IP address does not match the server IP.
        NumberError
            If the transaction amount is invalid.
        """
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
        """
        Checks whether a given IP address is a valid IPv4 address.

        Parameters
        ----------
        ip : str
            The IP address to validate.

        Returns
        -------
        bool
            True if the IP is invalid, False otherwise.

        Examples
        --------
        >>> app.is_invalid_ipv4("192.168.1.1")
        False
        >>> app.is_invalid_ipv4("999.999.999.999")
        True
        """
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
        """
        Parses input parameters into account number, IP address, and transaction amount.

        Parameters
        ----------
        parameters : str
            The command input.

        Returns
        -------
        tuple
            A tuple of (account, IP, amount).

        Examples
        --------
        >>> app.parse_parametrs("12345/192.168.1.1 500")
        ('12345', '192.168.1.1', '500')
        """
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
        """
        Forwards a command to another bank server.

        Parameters
        ----------
        account : str
            The account number.
        ip : str
            The target server IP.
        number : str or None
            The transaction amount, if applicable.
        code : str
            The command code.

        Returns
        -------
        str or None
            The server response or None if the connection fails.
        """
        working_port = None
        try:
            for i in range(65525,65536):
                try:
                    server_inet_address = (ip, i)
                    remote_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                    try:
                        timeout = float(self.readconfig("forward_scan_time_out"))
                    except Exception:
                        timeout = 5
                    remote_socket.settimeout(timeout)
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
        
    def readconfig(self,key):
        """
        Reads a configuration value from a JSON file.

        Parameters
        ----------
        key : str
            The key whose value needs to be retrieved.

        Returns
        -------
        str or None
            The value associated with the key, or None if an error occurs.

        Examples
        --------
        >>> server.readconfig("ip")
        '192.168.1.1'
        """
        try:
            with open("./Bank/config.json","r") as f:
                config = json.load(f)
                return config.get(key)
        except FileNotFoundError:
            print("Error: Config nebyl nalezen.")
            return None
        except KeyError:
            print(f"Error: Klíč: {key} nebyl v configu nalezen.")
            return None
        except Exception as e:
            print(e)
            return None
                