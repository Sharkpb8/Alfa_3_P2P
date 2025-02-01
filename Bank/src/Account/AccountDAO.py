from src.DatabaseSingleton import *
from src.Account.Account import Account

class AccountDAO:
    """
    A Data Access Object (DAO) for handling database operations related to bank accounts.

    Attributes
    ----------
    table_application : Application
        The application instance associated with the DAO.

    Methods
    -------
    Save(a)
        Saves a new account to the database.
    Update(a)
        Updates the balance of an existing account.
    Delete(Account_number)
        Deletes an account from the database.
    Read_balance(Account_number)
        Retrieves the balance of a specific account.
    Read_account_number()
        Retrieves all existing account numbers.
    Read_Bank_amount()
        Retrieves the total amount held by the bank.
    Read_Bank_number()
        Retrieves the total number of accounts in the bank.
    """

    def __init__(self,table_application):
        """
        Initialises the DAO with a reference to the application.

        Parameters
        ----------
        table_application : Application
            The application instance managing bank operations.

        Examples
        --------
        >>> dao = AccountDAO(app)
        """
        self.table_application = table_application

    def Save(self,a):
        """
        Saves a new account to the database.

        Parameters
        ----------
        a : Account
            The account object to be saved.

        Examples
        --------
        >>> account = Account(12345, 1000)
        >>> dao.Save(account)
        """
        sql = "INSERT INTO Accounts(account_number, balance)VALUES (%s, %s);"
        val = [a.Account_number, a.Balance]
        conn = DatabaseSingleton()
        cursor = conn.cursor()
        try:
            cursor.execute("START TRANSACTION;")
            cursor.execute(sql, val)
        except Exception as e:
            print(e)
            cursor.execute("ROLLBACK;")
        else:
            cursor.execute("COMMIT;")
        finally:
            DatabaseSingleton.close_conn()

    def Update(self,a):
        """
        Updates the balance of an existing account.

        Parameters
        ----------
        a : Account
            The account object with updated balance.

        Examples
        --------
        >>> account = Account(12345, 2000)
        >>> dao.Update(account)
        """
        sql = "UPDATE Accounts SET balance = %s WHERE account_number = %s;"
        val = [a.Balance, a.Account_number]
        conn = DatabaseSingleton()
        cursor = conn.cursor()
        try:
            cursor.execute("START TRANSACTION;")
            cursor.execute(sql, val)
        except Exception as e:
            print(e)
            cursor.execute("ROLLBACK;")
        else:
            cursor.execute("COMMIT;")
        finally:
            DatabaseSingleton.close_conn()

    def Delete(self,Account_number):
        """
        Deletes an account from the database.

        Parameters
        ----------
        Account_number : int
            The account number to be deleted.

        Examples
        --------
        >>> dao.Delete(12345)
        """
        sql = "DELETE FROM Accounts WHERE account_number = %s;"
        val = [Account_number]
        conn = DatabaseSingleton()
        cursor = conn.cursor()
        try:
            cursor.execute("START TRANSACTION;")
            cursor.execute(sql, val)
        except Exception as e:
            print(e)
            cursor.execute("ROLLBACK;")
        else:
            cursor.execute("COMMIT;")
        finally:
            DatabaseSingleton.close_conn()

    def Read_balance(self,Account_number):
        """
        Retrieves the balance of a specific account.

        Parameters
        ----------
        Account_number : int
            The account number.

        Returns
        -------
        int or None
            The balance of the account, or None if not found.

        Examples
        --------
        >>> dao.Read_balance(12345)
        1000
        """
        sql = "SELECT balance FROM Accounts where account_number = %s;"
        val = [Account_number]
        conn = DatabaseSingleton()
        cursor = conn.cursor()
        balance = None
        try:
            cursor.execute(sql,val)
            myresult = cursor.fetchall()
        except Exception as e:
            print(e)
        else:
            balance = myresult[0][0]      
        finally:
            DatabaseSingleton.close_conn()
            return balance
        
    def Read_account_number(self):
        """
        Retrieves all existing account numbers.

        Returns
        -------
        list of int or None
            A list of account numbers, or None if no accounts exist.

        Examples
        --------
        >>> dao.Read_account_number()
        [12345, 67890, 11223]
        """
        sql = "SELECT account_number FROM Accounts;"
        conn = DatabaseSingleton()
        cursor = conn.cursor()
        data = []
        try:
            cursor.execute(sql)
            myresult = cursor.fetchall()
        except Exception as e:
            print(e)
        else:
            for i in myresult:
                data.append(i[0])    
        finally:
            DatabaseSingleton.close_conn()
            if(len(data)>0):
                return data
            

    def Read_Bank_amount(self):
        """
        Retrieves the total amount held by the bank.

        Returns
        -------
        int
            The total bank balance.

        Examples
        --------
        >>> dao.Read_Bank_amount()
        500000
        """
        sql = "SELECT * FROM Bank_amount;"
        conn = DatabaseSingleton()
        cursor = conn.cursor()
        amount = 0
        try:
            cursor.execute(sql)
            myresult = cursor.fetchall()
        except Exception as e:
            print(e)
        else:
            amount = myresult[0][0]   
        finally:
            DatabaseSingleton.close_conn()
            return amount
        
    def Read_Bank_number(self):
        """
        Retrieves the total number of accounts in the bank.

        Returns
        -------
        int
            The number of accounts.

        Examples
        --------
        >>> dao.Read_Bank_number()
        150
        """
        sql = "SELECT * FROM Bank_number;"
        conn = DatabaseSingleton()
        cursor = conn.cursor()
        amount = 0
        try:
            cursor.execute(sql)
            myresult = cursor.fetchall()
        except Exception as e:
            print(e)
        else:
            amount = myresult[0][0]   
        finally:
            DatabaseSingleton.close_conn()
            return amount