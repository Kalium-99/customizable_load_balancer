from flask import Flask, request, jsonify
from consistent_hashing import ConsistentHashing

app = Flask(__name__)
ch = ConsistentHashing()

@app.route('/rep', methods=['GET'])
def get_replicas():
    return jsonify(message={"N": len(ch.hash_ring), "replicas": list(ch.hash_ring.values())}, status="successful")

@app.route('/add', methods=['POST'])
def add_replicas():
    data = request.json
    num_new_instances = data.get('n')
    hostnames = data.get('hostnames', [])
    for hostname in hostnames[:num_new_instances]:
        ch.add_server(hostname)
    return jsonify(message={"N": len(ch.hash_ring), "replicas": list(ch.hash_ring.values())}, status="successful")

@app.route('/rm', methods=['DELETE'])
def remove_replicas():
    data = request.json
    num_instances_to_remove = data.get('n')
    hostnames = data.get('hostnames', [])
    for hostname in hostnames[:num_instances_to_remove]:
        ch.remove_server(hostname)
    return jsonify(message={"N": len(ch.hash_ring), "replicas": list(ch.hash_ring.values())}, status="successful")

@app.route('/<path:path>', methods=['GET'])
def route_request(path):
    server_id = ch.get_server(path)
    return jsonify(message=f"Request routed to {server_id}", status="successful")

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
