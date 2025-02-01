import multiprocessing.process
import socket
from src.client import client
import json
import time
from src.error import *

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
        except Exception:
            timeout = 5
        port = int(port)
        server_inet_address = (ip, port)
        server_socket = socket.socket()
        server_socket.bind(server_inet_address)
        server_socket.listen()
        server_socket.settimeout(timeout)

        self.server_socket = server_socket
        self.server_ip = ip

        print("Server start on "+str(server_inet_address[0])+":"+str(server_inet_address[1]))

    def server_run(self):
        while True:
            try:
                connection, client_inet_address = self.server_socket.accept()
                process = multiprocessing.Process(target=self.create_new_client,args=(connection,client_inet_address,))
                process.start()
                print(f"Client connected on {client_inet_address[0]}")
            except socket.timeout:
                continue
            except OSError:
                break
            except ConnectionAbortedError:
                break
    
    def create_new_client(self,connection,client_inet_address):
        try:
            c = client(connection,self.server_ip,client_inet_address[0])
            c.run()
        except ClientAbortError:
            connection.close()
            print(f"Client with address {client_inet_address[0]} disconnected")

    def readconfig(self,key):
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
        
    def is_invalid_ipv4(self,ip):
        try:
            parts = ip.split(".")
            if (len(parts) != 4):
                return True
            for part in parts:
                num = int(part)
                if num < 0 or num > 255:
                    return True
                if len(part) > 1 and part[0] == "0":
                    return True
        except Exception:
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