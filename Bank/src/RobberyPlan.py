import socket
import multiprocessing
import time
import json
from itertools import combinations

class RobberyPlan():
    """
    A class for scanning a network for bank servers and determining the best targets for robbery.

    Attributes
    ----------
    ip : str
        The network identification (subnet) used for scanning.
    total_processes : int
        The number of parallel processes used for network scanning.
    scan_time_out : float
        The timeout value for each network connection attempt.

    Methods
    -------
    scan_network(process_id, addresses)
        Scans a range of IP addresses in the network for available bank servers.
    available_servers()
        Finds available bank servers in the local network.
    banks_info(addresses)
        Retrieves information about detected bank servers.
    best_combination(banks, target)
        Determines the best combination of banks to rob to meet a target amount.
    readconfig(key)
        Reads a configuration value from a JSON file.
    """

    def __init__(self,ip):
        """
        Initialises the RobberyPlan with the provided IP address.

        Parameters
        ----------
        ip : str
            The IP address used to determine the subnet for scanning.

        Examples
        --------
        >>> rp = RobberyPlan("192.168.1.1")
        """
        parts = ip.split(".")
        network_identification = f"{parts[0]}.{parts[1]}.{parts[2]}."
        self.ip = network_identification
        total_processes = self.readconfig("scan_processes")
        if(not total_processes or not isinstance(total_processes, int)):
            total_processes = 10
        self.total_processes = total_processes
        scan_time_out = self.readconfig("rp_scan_time_out")
        if (not scan_time_out or not isinstance(scan_time_out, (int,float))):
            scan_time_out = 0.1
        self.scan_time_out = scan_time_out

    def scan_network(self,process_id,addresses):
        """
        Scans a range of IP addresses in the network for available bank servers.

        Parameters
        ----------
        process_id : int
            The ID of the scanning process, used to determine the range of addresses to scan.
        addresses : dict
            A shared dictionary to store detected servers and their ports.

        Examples
        --------
        >>> rp.scan_network(0, {})
        """
        connections = []
        x_start = (256 * process_id) // self.total_processes
        x_end = (256 * (process_id + 1)) // self.total_processes-1
        try:
            for i in range(65525,65536):
                for x in range(x_start,x_end):
                    try:
                        server_inet_address = (self.ip+str(x), i)
                        remote_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                        remote_socket.settimeout(self.scan_time_out)
                        remote_socket.connect(server_inet_address)
                    except socket.error:
                        pass
                    else:
                        addresses[x] = i
                        connections.append(remote_socket)
            else:
                raise socket.error
        except socket.error:
            pass
        finally:
            for i in connections:
                i.close()

    def available_servers(self):
        """
        Finds available bank servers in the local network.

        This method launches multiple processes to scan the network and returns detected servers.

        Returns
        -------
        dict
            A dictionary containing detected servers and their corresponding ports.

        Examples
        --------
        >>> rp.available_servers()
        {10: 65525, 15: 65526}
        """
        manager = multiprocessing.Manager()
        addresses = manager.dict()
        processes = []
        start = time.time()
        for i in range(self.total_processes):
            process_client = multiprocessing.Process(target=self.scan_network,args=(i,addresses))
            processes.append(process_client)
            process_client.start()

        for process in processes:
            process.join()

        end = time.time()

        print("Scan trval {:.6f} sec.".format((end - start)))
        return addresses
    
    def banks_info(self,addresses):
        """
        Retrieves information about detected bank servers.

        Parameters
        ----------
        addresses : dict
            A dictionary containing detected servers and their corresponding ports.

        Returns
        -------
        list of list
            A list of banks, each containing IP address, bank amount, and number of clients.

        Examples
        --------
        >>> rp.banks_info({10: 65525})
        [['192.168.1.10', 'BA 100000', 'BN 500']]
        """
        result = []
        for addr,port in addresses.items():
            try:
                server_inet_address = (self.ip+str(addr), port)
                remote_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                remote_socket.connect(server_inet_address)
            except socket.error:
                pass
            else:
                data = [self.ip+str(addr)]
                BA = f"BA\r\n"
                remote_socket.sendall(BA.encode("utf-8"))
                BA_response = remote_socket.recv(4096).decode().strip()
                data.append(BA_response)
                BN = f"BN\r\n"
                remote_socket.sendall(BN.encode("utf-8"))
                BN_response = remote_socket.recv(4096).decode().strip()
                data.append(BN_response)
                result.append(data)
                remote_socket.close()
        return result

    def best_combination(self,banks, target):
        """
        Determines the best combination of banks to rob to meet a target amount.

        Parameters
        ----------
        banks : list of list
            A list of banks, each containing IP address, bank amount, and number of clients.
        target : int
            The target amount of money to be stolen.

        Returns
        -------
        str
            A formatted message with the closest sum to the target and affected banks.

        Examples
        --------
        >>> rp.best_combination([['192.168.1.10', 'BA 100000', 'BN 500']], 90000)
        'RP Nejbližší částka k dosažení 90000 je 100000 a bude třeba vyloupit banky 192.168.1.10 a bude poškozeno 500 klientů.'
        """
        print(banks)
        best_sum = float('inf')
        best_combo = []
        best_clients = float('inf')
        
        for i in range(1, len(banks) + 1):
            for combo in combinations(banks, i):
                total_money = sum(int(bank[1].split()[1]) for bank in combo)
                total_clients = sum(int(bank[2].split()[1]) for bank in combo)
                
                if ((abs(target - total_money) < abs(target - best_sum)) or (abs(target - total_money) == abs(target - best_sum) and total_clients < best_clients)):
                    if(best_sum == target):
                        break
                    best_sum = total_money
                    best_clients = total_clients
                    best_combo = combo
            if(best_sum == target):
                break
        
        banks = ""
        for bank in best_combo:
            banks += " "+bank[0]

        return f"RP Nejbližší částka k dosažení {target} je {best_sum} a bude třeba vyloupit banky {banks} a bude poškozeno {best_clients} klientů."

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
        >>> rp.readconfig("scan_processes")
        10
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