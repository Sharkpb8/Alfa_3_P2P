from src.DatabaseSingleton import *
from src.Account.Account import Account

class AccountDAO:

    def __init__(self,table_application):
        self.table_application = table_application

    def Save(self,a):
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