import multiprocessing.process
import socket
from src.client import client
import json
from src.error import *
import traceback

class server:
    """
    A server class that initialises a socket server, handles client connections, and manages configuration settings.

    Attributes
    ----------
    server_socket : socket.socket
        The server's main socket used for listening to incoming connections.
    server_ip : str
        The IP address of the server.

    Methods
    -------
    server_run()
        Starts the server and continuously listens for incoming client connections.
    create_new_client(connection, client_inet_address)
        Handles a new client connection by creating a new process.
    readconfig(key)
        Reads a configuration value from a JSON file.
    is_invalid_ipv4(ip)
        Validates whether a given IP address is a valid IPv4 address.
    is_invalid_port(port)
        Validates whether a given port number is within the acceptable range.
    """

    def __init__(self):
        """
        Initialises the server by reading configuration values, setting up a socket, and binding it to an IP and port.

        The server reads IP, port, and timeout values from a configuration file. If invalid values are found, it falls back 
        to default values.

        Examples
        --------
        >>> server = Server()
        Server start on 127.0.0.1:65525
        """
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
        print("".join(traceback.format_stack()))
        server_inet_address = (ip, port)
        server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_socket.bind(server_inet_address)
        server_socket.listen()
        server_socket.settimeout(timeout)

        self.server_socket = server_socket
        self.server_ip = ip

        print("Server start on "+str(server_inet_address[0])+":"+str(server_inet_address[1]))

    def server_run(self):
        """
        Starts the server loop, continuously accepting new client connections.

        The method waits for incoming connections, creates a new process for each client, and handles exceptions 
        like timeouts and OS errors.

        Examples
        --------
        >>> server.server_run()
        Client connected on 192.168.1.10
        """
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
        """
        Handles a new client connection.

        Parameters
        ----------
        connection : socket.socket
            The socket connection to the client.
        client_inet_address : tuple
            The IP address and port of the client.

        Examples
        --------
        >>> server.create_new_client(connection, ('192.168.1.10', 5000))
        After client loop ends: Client with address 192.168.1.10 disconnected
        """
        try:
            c = client(connection,"192.168.69.200",client_inet_address[0])
            c.run()
        except ClientAbortError:
            print(f"Client with address {client_inet_address[0]} disconnected")
        finally:
            connection.close()

    def readconfig(self,key):
        """
        Reads a configuration value from a JSON file.

        Parameters
        ----------
        key : str
            The key whose value needs to be retrieved.

        Returns
        -------
        str or None
            The value associated with the key, or None if an error occurs.

        Examples
        --------
        >>> server.readconfig("ip")
        '192.168.1.1'
        """
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
        """
        Validates whether a given IP address is a valid IPv4 address.

        Parameters
        ----------
        ip : str
            The IP address to validate.

        Returns
        -------
        bool
            True if the IP address is invalid, False otherwise.

        Examples
        --------
        >>> server.is_invalid_ipv4("192.168.1.1")
        False
        >>> server.is_invalid_ipv4("999.999.999.999")
        True
        """
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
        """
        Validates whether a given port number is within the acceptable range (65525-65535).

        Parameters
        ----------
        port : str or int
            The port number to validate.

        Returns
        -------
        bool
            True if the port number is invalid, False otherwise.

        Examples
        --------
        >>> server.is_invalid_port(65530)
        False
        >>> server.is_invalid_port(70000)
        True
        """
        try:
            num = int(port)
            if num < 65525 or num > 65535:
                return True
        except ValueError:
            return True
        else:
            return False