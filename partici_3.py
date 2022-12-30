#importing partici file
import partici
node = {'node_id': 'node_3', 'port': 8083, 'bport': 3003}

if __name__ == "__main__":
    partici.parti(node_id=node['node_id'],
                            port=node['port'],
                            bport=node['bport']).listening()
