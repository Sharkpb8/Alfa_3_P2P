import socket
import multiprocessing
import time
import json
from itertools import combinations

class RobberyPlan():

    def __init__(self,ip):
        parts = ip.split(".")
        network_identification = f"{parts[0]}.{parts[1]}.{parts[2]}."
        self.ip = network_identification
        self.total_processes = self.readconfig("scan_processes")
        self.scan_time_out = self.readconfig("scan_time_out")

    def scan_network(self,process_id,addresses):
        connections = []
        x_start = (256 * process_id) // self.total_processes
        x_end = (256 * (process_id + 1)) // self.total_processes-1
        try:
            for i in range(65525,65536):
                for x in range(x_start,x_end):
                    try:
                        # print(str(ip)+str(x), str(i))
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

        return f"K dosažení {target} je třeba vyloupit banky {banks} a bude poškozeno jen {best_clients} klientů."

    def readconfig(self,key):
        with open("./Bank/config.json","r") as f:
            config = json.load(f)
            return config[key]
