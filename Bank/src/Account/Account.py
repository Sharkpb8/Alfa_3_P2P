# from src.Inputs_check import *
# from src.Error import *

class Account:
    def __init__(self, Account_number, Balance):

        self.Account_number = int(Account_number)

        self.Balance = int(Balance)
        
    def __str__(self):
        return (f"Číslo účtu: {self.Account_number}, zůstatek: {self.Balance}")