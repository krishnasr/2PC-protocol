

import Coord # importing Coord.py files
node = {'node_id': 'master', 'port': 8080, 'bport': 3000}

class node_2: #this is participant 2
    node_id = 'node_2'
    addr = ("127.0.0.1", 8082)
class node_3: #this is participant 3
    node_id = 'node_3'
    addr = ("127.0.0.1", 8083)
class node_1: #this is participant 1
    node_id = 'node_1'
    addr = ("127.0.0.1", 8081)

if __name__ == "__main__":
    Coord.Coord(node_id=node['node_id'],
                            port=node['port'],
                            bport=node['bport'],
                            participants=[node_1, node_2, node_3]).listening() #calling Coor function class from Coor.py
