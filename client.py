

import json
from sys import stderr, exit
from socket import AF_INET, SOCK_STREAM
from socket import socket

def client_main(forever=True):
    a1=98
    while a1==98:
        qer = {'action': 'commit'}
        string1 = input("client> ")

        if string1 == "exit":
            forever = False
            a1=0
            break

        query = string1.split()
        if query[0] in ['crash', 'recover']: # if the input is crash or recover then it will change the stat to crash or recover
            qer['action'] = 'change_status'
            qer['status'] = query[0]
            qer['node_id'] = query[1]
        elif query[0] in ['add', 'sub']:
            qer['query'] = f"{query[0]}('{query[1]}', {query[2]})"
        elif query[0] in ['new', 'del']:
            qer['query'] = f"{query[0]}('{query[1]}')"
        else: # if no desired input is entered these details will be printed for understanding.
            print("vailable actions are: ")
            print("exit")
            print("new <key>")
            print("add <key> <offset>")
            print("sub <key> <offset>")
            print("del <key>")
            print("crash <node_id>")
            print("recover <node_id>")
            print()
            continue

        cclient_sco=socket(AF_INET, SOCK_STREAM)
        cclient_sco.connect(("127.0.0.1", 8080))
        cclient_sco.send(json.dumps(qer).encode())
        rs1 = cclient_sco.recv(65535).decode()
        try:
            rs1 = json.loads()
            print(json.dumps(rs1, indent=4))
        except:
            print(rs1)

if __name__ == "__main__":
    client_main()
