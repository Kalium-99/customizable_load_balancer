import hashlib

class ConsistentHashing:
    def __init__(self, num_slots=512, num_replicas=9):
        self.num_slots = num_slots
        self.num_replicas = num_replicas
        self.hash_ring = {}

    def _hash(self, key):
        return int(hashlib.md5(key.encode('utf-8')).hexdigest(), 16) % self.num_slots

    def add_server(self, server_id):
        for i in range(self.num_replicas):
            virtual_node = f"{server_id}-{i}"
            hash_key = self._hash(virtual_node)
            self.hash_ring[hash_key] = server_id

    def remove_server(self, server_id):
        for i in range(self.num_replicas):
            virtual_node = f"{server_id}-{i}"
            hash_key = self._hash(virtual_node)
            del self.hash_ring[hash_key]

    def get_server(self, request_key):
        hash_key = self._hash(request_key)
        sorted_keys = sorted(self.hash_ring.keys())
        for key in sorted_keys:
            if hash_key <= key:
                return self.hash_ring[key]
        return self.hash_ring[sorted_keys[0]]

# Example usage
ch = ConsistentHashing()
ch.add_server('server1')
ch.add_server('server2')
ch.add_server('server3')
print(ch.get_server('client_request'))
