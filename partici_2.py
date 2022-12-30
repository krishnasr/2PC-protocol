#importing partici file
import partici
node = {'node_id': 'node_2', 'port': 8082, 'bport': 3002}

if __name__ == "__main__":
    partici.parti(node_id=node['node_id'],
                            port=node['port'],
                            bport=node['bport']).listening()
