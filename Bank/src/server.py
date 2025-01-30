import multiprocessing.process
import socket
from src.client import client
import json

class server:

    def __init__(self):
        ip = self.readconfig("ip")
        if(self.is_invalid_ipv4(ip)):
            ip = "127.0.0.1"
        port = self.readconfig("port")
        if(self.is_invalid_port(port)):
            port = "65525"
        timeout = self.readconfig("server_time_out")
        try:
            timeout = float(timeout)
        except ValueError:
            timeout = 5
        port = int(port)
        server_inet_address = (ip, port)
        server_socket = socket.socket()
        server_socket.bind(server_inet_address)
        server_socket.listen()
        server_socket.settimeout(timeout)

        timeout = self.readconfig("server_time_out")
        try:
            timeout = float(timeout)
        except ValueError:
            timeout = 5
        server_socket.settimeout(timeout)

        self.server_socket = server_socket
        self.server_ip = ip

        print("Server start on "+str(server_inet_address[0])+":"+str(server_inet_address[1]))

    def server_run(self):
        while True:
            try:
                connection, client_inet_address = self.server_socket.accept()
                process_client = multiprocessing.Process(target=self.create_new_client,args=(connection,client_inet_address,))
                process_client.start()
                process_alive = multiprocessing.Process(target=self.is_alive,args=(connection,client_inet_address,))
                process_alive.start()
                print(f"Client connected on {client_inet_address[0]}")
            except socket.timeout:
                continue
            except OSError:
                break
            except ConnectionAbortedError:
                break
    
    def create_new_client(self,connection,client_inet_address):
        c = client(connection,self.server_ip,client_inet_address[0])
        c.run()

    def readconfig(self,key):
        with open("./Bank/config.json","r") as f:
            config = json.load(f)
            return config[key]
        
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
        
    def is_invalid_port(self,port):
        try:
            num = int(port)
            if num < 65525 or num > 65535:
                return True
        except ValueError:
            return True
        else:
            return False
    
    def is_alive(self,connection,client_inet_address):
        timeout = self.readconfig("client_time_out")
        try:
            timeout = float(timeout)
        except ValueError:
            timeout = 5
        connection.settimeout(timeout)
        while True:
            try:
                connection.sendall(b"\x00")
            except (BrokenPipeError, ConnectionResetError):
                break
        connection.close()
        print(f"Client with address {client_inet_address[0]} disconnected")
        print(connection)