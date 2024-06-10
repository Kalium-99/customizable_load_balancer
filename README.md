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


