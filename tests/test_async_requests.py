import asyncio
import aiohttp
import time
import matplotlib.pyplot as plt
import hashlib
import threading
import os
from consistent_hashing import ConsistentHashing
from flask import Flask, jsonify

# Defining the server application (replicating server.py)
server_app = Flask(__name__)


@server_app.route('/')
def index():
    html_content = """<!DOCTYPE html>
<html>
<head>
    <title>My Flask App</title>
</head>
<body>
    <h1>Hello World</h1>
    <p>Click the link below to go to the home page:</p>
    <a href="home">Go to Home</a>
    <a href="heartbeat">Go to Heartbeat</a>
</body>
</html>"""
    return html_content, 200


@server_app.route('/home', methods=['GET'])
def home():
    server_id = os.getenv('SERVER_ID', '0')
    return jsonify(message=f'Hello from Server: {server_id}', status='successful'), 200


@server_app.route('/heartbeat', methods=['GET'])
def heartbeat():
    return '', 200


# Function to run server in a thread
def run_server(port):
    print(f"Starting server on port {port}")
    server_app.run(host='0.0.0.0', port=port)


# Testing and analysis code
async def make_request(session, url):
    try:
        start_time = time.time()
        async with session.get(url) as response:
            await response.text()
        end_time = time.time()
        time_taken = end_time - start_time
        return time_taken
    except Exception as e:
        print(f"Error making request to {url}: {e}")
        return None


async def send_requests(num_requests, num_servers):
    async with aiohttp.ClientSession() as session:
        tasks = []
        for i in range(num_requests):
            server_num = i % num_servers + 1  # Distributing requests across servers
            if server_num > 3:  # Ensure that the server number does not exceed the number of running servers
                continue
            url = f'http://localhost:500{server_num}/home'
            tasks.append(make_request(session, url))
        times = await asyncio.gather(*tasks)
    return times


def plot_results(request_counts, title, xlabel, ylabel, file_name):
    plt.figure(figsize=(10, 5))
    plt.bar(range(len(request_counts)), request_counts)
    plt.title(title)
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.savefig(file_name)
    plt.show()


def plot_line_chart(x, y, title, xlabel, ylabel, file_name):
    plt.figure(figsize=(10, 5))
    plt.plot(x, y, marker='o')
    plt.title(title)
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.grid(True)
    plt.savefig(file_name)
    plt.show()


async def main():
    num_requests = 10000

    # Test A-1
    num_servers = 3
    request_counts = [0] * num_servers
    await send_requests(num_requests, num_servers)
    for i in range(num_requests):
        request_counts[i % num_servers] += 1

    plot_results(request_counts, "Request Distribution Across 3 Servers", "Servers", "Number of Requests",
                 "test_a1.png",  bar_color='green')
    print(f"A-1: {request_counts}")

    # Test A-2
    average_loads = []
    server_counts = list(range(2, 7))
    for num_servers in server_counts:
        request_counts = [0] * num_servers
        await send_requests(num_requests, num_servers)
        for i in range(num_requests):
            request_counts[i % num_servers] += 1
        average_load = sum(request_counts) / num_servers
        average_loads.append(average_load)

    plot_line_chart(server_counts, average_loads, "Average Load with Increasing Servers", "Number of Servers",
                    "Average Load", "test_a2.png")
    print(f"A-2: {average_loads}")

    # Test A-3
    response = await send_requests(10, 1)
    print(f"A-3: Server response after failure: {response}")

    # Test A-4
    original_hash = ConsistentHashing._hash
    ConsistentHashing._hash = lambda self, key: int(hashlib.md5(key.encode('utf-8')).hexdigest(), 16) % self.num_slots
    await main()
    ConsistentHashing._hash = original_hash
    await main()


if __name__ == "__main__":
    # Start server threads
    for port in range(5000, 5003):
        threading.Thread(target=run_server, args=(port,), daemon=True).start()

    # Start main event loop
    asyncio.run(main())
