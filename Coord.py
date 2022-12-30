import json
from threading import Thread
from socket import AF_INET, SOCK_STREAM
from socket import SOL_SOCKET, SO_REUSEADDR
from socket import socket

status = {"active": True, "inactive": False}
vote = {"yes": True, "no": False}

class Coord(Thread):

    def __init__(self, node_id, port=8080, bport=3000, participants=None):
        Thread.__init__(self)

        self.node_id: str = node_id
        self.addr: tuple = ("127.0.0.1", port)
        self.participants: list = participants
        self.status: str = status["active"]

    def commiting(self, transac, process): # calling commiting function
        transacs = dict()
        if not process:
            print("Transaction aborted")
            p4=json.dumps({'ack': '-ABORTED'}).encode()
            self.client.send(p4)
        else:
            for person in self.participants:
                soc_comm = socket(AF_INET, SOCK_STREAM)
                soc_comm.connect(person.addr)
                soc_comm.send(json.dumps(transac).encode())
           
                res = json.loads(soc_comm.recv(65535).decode()) 
                transacs[person.node_id] = res
                soc_comm.close()
            print("Transaction successful")
        txs = json.dumps(transac, indent=2)
        self.client.send(txs.encode())

    def stat_chang(self, transac): # calling stat_chang function
        if self.node_id != transac['node_id']:
            for person in self.participants:
                if person.node_id == transac['node_id']:
                    soc_k = socket(AF_INET, SOCK_STREAM)
                    soc_k.connect(person.addr)
                    r1=json.dumps(transac).encode()
                    soc_k.send(r1)
                    soc_k.close()
                    break
        else:
            self.status = not self.status
        print("\n\t", f"{transac['node_id']} {transac['status']}ed", "\n")
        self.client.send(f":{transac['status']}ed {transac['node_id']}".encode())
    
    def prep(self)-> bool: #calling prep function
        q1 = json.dumps({'action': 'vote', 'proceed': None})
        trans_comm = True
        for person in self.participants:
            soc_voter = socket(AF_INET, SOCK_STREAM)
            soc_voter.connect(person.addr) # connecting to the participant
            soc_voter.send(q1.encode())
            a1=soc_voter.recv(65535).decode()
            res = json.loads(a1) # response
            if not res["proceed"]:
                print(f"Abort transaction: PARTICIPANT-{person.node_id} not ready")
                trans_comm = False
            soc_voter.close()
        return trans_comm

    def listening(self): # calling listening function
        self.start() 
        client_sock=socket(AF_INET, SOCK_STREAM)
        client_sock.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
        client_sock.bind(self.addr) # conneting to the client
        client_sock.listen(100)
        print(f"COORDINATOR-{self.node_id} listening at {self.addr[0]}:{self.addr[1]}")
        p1=99
        while p1==99:
            self.client, cleint_addr = client_sock.accept()
            r1 = self.client.recv(65535)
            transac = json.loads(r1.decode())
            print(f"[NEW] {cleint_addr[0]}:{cleint_addr[1]} -> {self.addr[0]}:{self.addr[1]}")
            print(f"[TRANSACTION] {transac}")
            if transac['action'] == 'change_status':
                self.stat_chang(transac)
            elif self.prep() and transac['action'] == 'commit':
                print("-COMMIT" if self.status == status["active"] else "-ABORT")
                pro=bool(self.status == status["active"])
                self.commiting(transac, pro)
            else:
                print("-ABORT", "\n")
                rp=vote["no"]
                self.commiting(transac, rp)
            print() 
            self.client.close() # closing the client 

    

     

    
