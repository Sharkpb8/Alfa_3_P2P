import socket
import multiprocessing
from src.client import client

class server:

    def __init__(self):
        server_inet_address = ("127.0.0.1", 65430)
        server_socket = socket.socket()
        server_socket.bind(server_inet_address)
        server_socket.listen()

        self.server_socket = server_socket
        self.server_ip = server_inet_address[0]

        print("Server start on "+str(server_inet_address[0])+":"+str(server_inet_address[1]))

    def server_run(self):
        while True:
            try:
                connection, client_inet_address = self.server_socket.accept()
                process = multiprocessing.Process(target=self.create_new_client,args=(connection,self,))
                process.start()
            except OSError:
                break
            except ConnectionAbortedError:
                break
    
    def create_new_client(self,connection,server):
        c = client(connection,self.server_ip)
        c.run()