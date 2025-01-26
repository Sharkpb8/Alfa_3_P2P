from src.application import application

class client():

    def __init__(self,connection,server_ip):
        self.connection = connection
        self.application = application(self)
        self.server_ip = server_ip

    def run(self):
        while True:
            self.menu_input()

    def menu_input(self):
        commands = [
            ("BC",self.Bank_Code),
            ("AC",self.application.Account_create),
            ("AD",self.application.Account_deposit),
            ("AW",self.application.Account_withdrawal),
            ("AB",self.application.Account_balance),
            ("AR",self.application.Account_remove),
            ("BA",self.application.Bank_amount),
            ("BN",self.application.Bank_number),
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
        except ConnectionAbortedError:
            pass
        else:
            return commands[num][1](split_input[1] if len(split_input) > 1 else None)   

    def send_message(self,message,newline = True):
        if(newline):
            message_as_bytes = bytes(message+"\n\r", "utf-8")
        else:
            message_as_bytes = bytes(message, "utf-8")
        self.connection.send(message_as_bytes)

    def get_input(self):
        buffer = b""

        while True:
            chunk = self.connection.recv(256)
            buffer += chunk
            
            if buffer.endswith(b"\r\n"):
                message = buffer.decode("utf-8")
                return message.strip()
            
    def Bank_Code(self,parametrs = None):
        if not parametrs:
            self.send_message(f"BC {self.server_ip}")
        else:
            self.send_message("ER Příkaz má mít formát: BC")
