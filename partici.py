import json
from threading import Thread

from socket import AF_INET, SOCK_STREAM
from socket import SOL_SOCKET, SO_REUSEADDR
from socket import socket

status = {"active": True, "inactive": False}
vote = {"yes": True, "no": False}

class parti(Thread):

    def __init__(self, node_id, port=8080, bport=3000):
        Thread.__init__(self)

        self.node_id: str = node_id
        self.addr: tuple = ("127.0.0.1", port)
        self.baddr: tuple = ("127.0.0.1", bport)
        self.store: dict = dict()
        self.status: str = status["active"]

    
    def _del(self, keys): # the following del,sub,add,new are the function that process the key and offset value and store them in the storage.
        _ = self.store.pop(keys)
        return self.store
    
    def _sub(self, keys, offsets):
        self.store[keys] =self.store[keys] -offsets
        return self.store
    
    def _add(self, keys, offsets) :
        self.store[keys] =self.store[keys]+ offsets
        return self.store

    def _new(self, keys):
        self.store[keys] = 0
        return self.store
    
    def commiting(self, transac): # when the trasaction sends commit command the coordinator will commit
        # print(transaction) #DEBUG
        transac['node_id'] = self.node_id
        transac['result'] = eval(f"self._{transac['query']}")
        print(f"[RESULT] {transac}", "\n")
        i1=json.dumps(transac).encode()
        self.coordinator.send(i1)
     
    def stat_change(self): #function for changing the status
        self.status = not self.status
        print(f"{self.node_id} {':recovered' if self.status else ':crashed'}")
    
    def voting(self, transac): #function for changing current transaction status
        transac['node_id'] = self.node_id
        transac['proceed'] = self.status
        print(f"[VOTE] {transac}")
        p1=json.dumps(transac).encode()
        self.coordinator.send(p1)

    def listening(self): # calling listening function
        self.start() 
        client_soc=socket(AF_INET, SOCK_STREAM)
        client_soc.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
        client_soc.bind(self.addr)
        client_soc.listen(100)
        print(f"PARTICIPANT-{self.node_id} is listening at {self.addr[0]}:{self.addr[1]}")
        rp2=78
        while rp2==78:
            self.coordinator, client_addr = client_soc.accept()
            req = self.coordinator.recv(65535)
            transac = json.loads(req.decode())
            print(f"[NEW] {client_addr[0]}:{client_addr[1]} -> {self.addr[0]}:{self.addr[1]}")
            print(f"[TRANSACTION] {transac}")
            self.transac_handle(transac)
            self.coordinator.close()
     
    def transac_handle(self, transac): # this function changes the transaction and handles the status of the participant
        if transac['action'] == 'change_status':
            self.stat_change()
        elif transac['action'] == 'commit':
            self.commiting(transac)
        elif transac['action'] == 'vote':
            self.voting(transac)
        else:
            dums1=json.dumps({'node_id': self.node_id,
                                              'message': f'Unknown action operation: {transac["action"]}'}).encode()
            self.coordinator.send(dums1)