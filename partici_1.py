

import partici #importing partici file
node = {'node_id': 'node_1', 'port': 8081, 'bport': 3001}

if __name__ == "__main__":
    partici.parti(node_id=node['node_id'],
                    port=node['port'],
                    bport=node['bport']).listening()
