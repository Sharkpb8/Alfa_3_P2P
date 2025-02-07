# P2P Bank System

## Author
**Name:** Adam Hlaváčik  
**Contact:** hlavacik@spsejecna.cz

**Date of Completion:** 01.02.2024  
**Institution:** Střední průmyslová škola elektrotechnická, Praha 2, Ječná 30  
**Type of project:** School project



## Project Overview
This P2P Bank System is a python program that simulates a peer-to-peer network of banks where users can perform banking operations such as creating accounts, depositing, withdrawing money, and checking balances. It also supports operations like creating robbery plans by evaluating the state of the entire network.



## User Requirements
- The application allows users to:
  - Create a new bank account.
  - Deposit money into an account.
  - Withdraw money from an account.
  - Check the balance of an account.
  - Remove accounts with a zero balance.
  - Get the total bank amount across all accounts.
  - Get the number of clients in the bank.
  - Send a robbery plan request to estimate how to reach a target amount by robbing the least number of clients.



## Configuration Options
Configurations are set in `config.json`:
- **Network Configuration**:
  - `host`: The IP address the server listens on.
  - `port`: The port the server listens on, configurable between 65525 and 65535.
  - `timeout`: The timeout for client listening, in s (e.g., 5).
  - `client_time_out`: The timeout for client in s (e.g. 5).
  - `scan_processes`: Number of processes used to scan network (e.g. 10).
  - `scan_time_out`: Time out used in scaning network.

  
Refer to `config.json` for valid configurations.


## Documentation and Reporting

### Overview
The P2P Bank System simulates the operation of a bank that communicates with other nodes in a peer-to-peer network. The application supports multiple banking commands, logs all activities, and implements a simple robbery plan functionality based on current balances and client information from all connected nodes.

### How It Works
1. **Commands**:
   - **BC**: Returns the bank code (IP address).
   - **AC**: Creates a new account and returns the account number.
   - **AD**: Deposits money into an account.
   - **AW**: Withdraws money from an account.
   - **AB**: Displays the balance of an account.
   - **AR**: Removes an account if its balance is zero.
   - **BA**: Displays the total balance of the bank.
   - **BN**: Displays the number of clients in the bank.
   - **RP**: Generates a robbery plan to reach a specified target balance while minimizing the number of affected clients.

| Name                        | Code | Call                                      | Successfull response         | Error response      |
|------------------------------|-----|---------------------------------------------|-----------------------------|------------------------|
| Bank code                    | BC  | `BC`                                          | `BC <ip>`                     | `ER <message>` <message>           |
| Account create                | AC  | `AC`                                          | `AC <account>/<ip>`           | `ER <message>` <message>           |
| Account deposit               | AD  | `AD <account>/<ip> <number>`                  | `AD`                          | `ER <message>` <message>           |
| Account withdrawal            | AW  | `AW <account>/<ip> <number>`                  | `AW`                          | `ER <message>` <message>           |
| Account balance               | AB  | `AB <account>/<ip>`                           | `AB <number>`                 | `ER <message>` <message>           |
| Account remove                | AR  | `AR <account>/<ip>`                           | `AR`                          | `ER <message>` <message>           |
| Bank (total) amount           | BA  | `BA`                                          | `BA <number>`                 | `ER <message>` <message>           |
| Bank number of clients        | BN  | `BN`                                          | `BN <number>`                 | `ER <message>` <message>           |
| Robbery plan                  | RP | `RP <number>`                                | `RP <message>`                |`ER <message>`           |


1. **Logs**:
   - Every operation is logged to the system log file with relevant details about commands received, errors encountered, and any operations performed.

2. **Networking**:
   - The system listens on a user-defined port for incoming connections.
   - Commands are received as UTF-8 encoded text and processed accordingly.
   - Responses are sent back to the requesting client in the same format.

## Sources and Consulted
- ChatGPT
- Chat used for documentation: [Link](https://chatgpt.com/share/679eaab0-6f38-800a-9668-1d85f4a41434)
- Wikipedia
- W3Schools
- GeeksforGeeks
- Python Docs
- Martin Hornych
- Tomáš Križko
- Ondra Kábrt

### Reused code
- [Alfa_2](https://github.com/Sharkpb8/Alfa_2_Database)

## Installation and Execution

### Dependencies
- Python 3.xx
- mysql-connector-python
- pyinstaller

### Code Build
1. Clone the project from GitHub using the command:
   ```bash
   git clone https://github.com/Sharkpb8/Alfa_3_P2P.git
2. install venv and modules
   ```bash
   python.exe -m venv venv
   ./venv/Scripts/pip.exe install -r requirements.txt
4. In powershell navigate to Alfa_3_P2P
5. Paste this command to activate:
   ```bash
   & disk:/path/to/project/Alfa_3_P2P/venv/Scripts/python.exe disk:/path/to/project/Alfa_3_P2P/Bank/main.py
6. Connect using putty with connection type raw on the same ip and port as the server.
