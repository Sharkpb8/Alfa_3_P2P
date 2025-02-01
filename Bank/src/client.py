from src.application import application
from src.error import *

class client():
    """
    A client class that handles communication with the server and processes commands.

    Attributes
    ----------
    connection : socket.socket
        The socket connection to the server.
    application : application
        An instance of the application class that manages account-related operations.
    server_ip : str
        The IP address of the server.
    client_ip : str
        The IP address of the client.

    Methods
    -------
    run()
        Starts listening for user input and processes commands.
    menu_input()
        Handles user input and executes corresponding commands.
    send_message(message, newline=True)
        Sends a message to the client.
    get_input()
        Receives input from the client.
    Bank_Code(parameters=None)
        Returns the bank code (server IP address) or an error message if incorrect parameters are provided.
    """

    def __init__(self,connection,server_ip,client_ip):
        """
        Initialises the client with a connection to the server and prepares the application module.

        Parameters
        ----------
        connection : socket.socket
            The socket connection to the server.
        server_ip : str
            The IP address of the server.
        client_ip : str
            The IP address of the client.

        Examples
        --------
        >>> client = Client(connection, "192.168.1.1", "192.168.1.100")
        """
        self.connection = connection
        self.application = application(self)
        self.server_ip = server_ip
        self.client_ip = client_ip

    def run(self):
        """
        Starts listening for user input and processes commands.

        This method continuously calls `menu_input()` to handle client requests.
        """
        while True:
            self.menu_input()

    def menu_input(self):
        """
        Handles user input and executes the corresponding command.

        The method reads input from the client, identifies the associated command, and executes it. 
        If an invalid command is given, an error message is sent back.
        """
        commands = [
            ("BC",self.Bank_Code),
            ("AC",self.application.Account_create),
            ("AD",self.application.Account_deposit),
            ("AW",self.application.Account_withdrawal),
            ("AB",self.application.Account_balance),
            ("AR",self.application.Account_remove),
            ("BA",self.application.Bank_amount),
            ("BN",self.application.Bank_number),
            ("RP",self.application.Robbery_plan)
        ]

        choosen_com = None
        try:
            while (choosen_com == None):
                choosen_com = self.get_input()
                split_input = choosen_com.split(maxsplit=1)
                try:
                    num = 0
                    for i,comand in commands:
                        if(split_input[0] == i):
                            break
                        num += 1
                    if (num == len(commands)):
                        raise Exception()
                except:
                    self.send_message("Špatný příkaz")
                    choosen_com = None
        except OSError:
            pass
        else:
            try:
                result = commands[num][1](split_input[1] if len(split_input) > 1 else None)
                if(result):
                    self.send_message(result)
            except ConnectionAbortedError:
                pass

    def send_message(self,message,newline = True):
        """
        Sends a message to the client.

        Parameters
        ----------
        message : str
            The message to be sent.
        newline : bool, optional
            Whether to append a newline character at the end (default is True).

        Examples
        --------
        >>> client.send_message("Welcome to the bank system")
        """
        if(newline):
            message_as_bytes = bytes(f"{message}\n\r", "utf-8")
        else:
            message_as_bytes = bytes(message, "utf-8")
        self.connection.send(message_as_bytes)

    def get_input(self):
        """
        Receives input from the client.

        This method listens for incoming data from the client until it receives a full command.

        Returns
        -------
        str
            The decoded client input.

        Raises
        ------
        ClientAbortError
            If the client unexpectedly disconnects.

        Examples
        --------
        >>> client.get_input()
        'BC'
        """
        buffer = b""

        while True:
            chunk = self.connection.recv(256)
            if(chunk == b''):
                raise ClientAbortError
            buffer += chunk
            
            if buffer.endswith(b"\r\n"):
                message = buffer.decode("utf-8")
                return message.strip()
            
    def Bank_Code(self,parametrs = None):
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
        if not parametrs:
            self.send_message(f"BC {self.server_ip}")
        else:
            self.send_message("ER Příkaz má mít formát: BC")
