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
  
