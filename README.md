# customizable_load_balancer

## Getting Started

### Prerequisites

- Docker
- Docker Compose
-  Python 3.9 or later

### Installation

1. **Clone the repository**:

   ```bash
   git clone https://github.com/Kalium-99/customizable_load_balancer.git

2. **Build the Docker images**:
    ```bash
    docker-compose build
3. **Start the services**:
   ```bash
   docker-compose up

### Load Balancer Overview

The load balancer uses consistent hashing  to distribute client requests across multiple server instances. Consistent hashing is a technique that allows efficient and scalable distribution of keys (in this case, client requests) across dynamic set of nodes.It minimises the number of keys that need to be remapped when nodes are added or removed.

  ### 1. Consistent Hashning implementation
  1. **Initialization**:
     ```bash
     class ConsistentHashing:
    def __init__(self, num_slots=512, num_replicas=9):
        self.num_slots = num_slots
        self.num_replicas = num_replicas
        self.hash_ring = {}
   - num_slots: The total number of slots or positions on the hash ring. The hash values are mapped to these slots.
   - num_replicas: The number of virtual nodes or replicas for each server. This helps in evenly distributing the load.
   - hash_ring: A dictionary to store the mapping of hash keys to server IDs.
     
  2. **Hashing Function**:
     ```bash
     def _hash(self, key):
    return int(hashlib.md5(key.encode('utf-8')).hexdigest(), 16) % self.num_slots
   - _hash: Converts the input key (server ID or request path) to a hash value using MD5 and maps it to a slot in the hash ring.

 3. **Adding a Server**
    ```bash
    def add_server(self, server_id):
    for i in range(self.num_replicas):
        virtual_node = f"{server_id}-{i}"
        hash_key = self._hash(virtual_node)
        self.hash_ring[hash_key] = server_id
   - add_server: Adds virtual nodes for a server by hashing the server ID combined with an index. Each virtual node is assigned a position on the hash ring.

 4. ** Removing a server**
    ```bash
    def remove_server(self, server_id):
    for i in range(self.num_replicas):
        virtual_node = f"{server_id}-{i}"
        hash_key = self._hash(virtual_node)
        del self.hash_ring[hash_key]
   - remove_server: Removes the virtual nodes of a server from the hash ring by deleting their corresponding hash keys.

 5. **Getting a Server for a Request**
    ```bash
    def get_server(self, request_key):
    hash_key = self._hash(request_key)
    sorted_keys = sorted(self.hash_ring.keys())
    for key in sorted_keys:
        if hash_key <= key:
            return self.hash_ring[key]
    return self.hash_ring[sorted_keys[0]]
- get_server: Finds the appropriate server for a given request key by hashing the request key and finding the closest hash key on the ring.

  ### 2. Load Balancer Implementation
  1. **Initialization**
     ```bash
     from flask import Flask, request, jsonify
     from consistent_hashing import ConsistentHashing
     app = Flask(_name_)
     ch = ConsistentHashing()
   - Creates a Flask application and initializes a 'ConsistentHashing' instance.
  2. **Check Crurrent Replicas**
     ```bash
     @app.route('/rep', methods=['GET'])
     def get_replicas():
     return jsonify(message={"N": len(ch.hash_ring), "replicas": list(ch.hash_ring.values())}, status="successful")
   - /rep: Returns the number of replicas and a list of servers currently in the hash ring.
  3. **Add Replicas**
     ```bash
     @app.route('/add', methods=['POST'])
     def add_replicas():
     data = request.json
     num_new_instances = data.get('n')
     hostnames = data.get('hostnames', [])
     for hostname in hostnames[:num_new_instances]:
        ch.add_server(hostname)
     return jsonify(message={"N": len(ch.hash_ring), "replicas": list(ch.hash_ring.values())}, status="successful")
   4. **Remove Replicas**
      ```bash
      @app.route('/rm', methods=['DELETE'])
      def remove_replicas():
      data = request.json
      num_instances_to_remove = data.get('n')
      hostnames = data.get('hostnames', [])
      for hostname in hostnames[:num_instances_to_remove]:
        ch.remove_server(hostname)
      return jsonify(message={"N": len(ch.hash_ring), "replicas": list(ch.hash_ring.values())}, status="successful")
   5. **Route Requests**
      ```bash
          @app.route('/<path:path>', methods=['GET'])
       def route_request(path):
        server_id = ch.get_server(path)
        return jsonify(message=f"Request routed to {server_id}", status="successful")
   - /<path:path>: Routes incoming requests to the appropriate server by using the consistent hashing algorithm.

 ### 3. Hashing Process
 **Hashing Ring constriction**
 - The hash ring is constructed by hashing the server IDs (including replicas) and placing them on a virtual ring with a fixed number of slots.

**Adding/Removing Servers**
-When a server is added, its replicas are hashed and placed on the ring. When a server is removed, its replicas are removed from the ring.

**Routung Requests**
Each incoming request is hashed to determine its position on the ring. The load balancer then finds the nearest server in a clockwise direction from this position. If no server is found in the clockwise direction, it wraps around to the first server in the ring.



