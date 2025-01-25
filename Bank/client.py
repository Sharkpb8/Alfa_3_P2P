

class client():

    def __init__(self,connection,server_ip):
        self.connection = connection
        self.server_ip = server_ip

    def run(self):
        while True:
            self.menu_input()

    def menu_input(self):
        commands = [
            ("BC","1"),
            ("AC","2"),
            ("AD","3"),
            ("AW","4"),
            ("AB","5"),
            ("AR","6"),
            ("BA","7"),
            ("BN","8"),
        ]

        choosen_com = None
        try:
            while (choosen_com == None):
                choosen_com = self.get_input()
                code = choosen_com[:2]
                try:
                    num = 0
                    for i,comand in commands:
                        if(code == i):
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
            print(commands[num][0])
            #return commands[choosen_com - 1][1]()   

    def send_message(self,message,newline = True):
        if(newline):
            message_as_bytes = bytes(message+"\n\r", "utf-8")
        else:
            message_as_bytes = bytes(message, "utf-8")
        self.connection.send(message_as_bytes)

    def get_input(self):
        #why ?????????????
        buffer = b""

        while True:
            chunk = self.connection.recv(256)
            buffer += chunk
            
            if buffer.endswith(b"\r\n"):
                message = buffer.decode("utf-8")
                return message.strip()
