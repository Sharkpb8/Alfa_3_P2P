# from src.Inputs_check import *
# from src.Error import *

class Account:
    """
    A class representing a bank account.

    Attributes
    ----------
    Account_number : int
        The unique account number.
    Balance : int
        The current balance of the account.
    """
    def __init__(self, Account_number, Balance):

        self.Account_number = int(Account_number)

        self.Balance = int(Balance)