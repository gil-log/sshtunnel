# sshtunnel

sshtunnel is a Docker image for establishing SSH tunnels using environment variables with password or public key authentication. Supports multi-platform deployment including AMD64 and ARM64 (Apple Silicon M1/M2) architectures.

## Table of Contents
- [Usage Scenario](#usage-scenario)
- [Features](#features)
- [Requirements](#requirements)
- [Quick Start](#quick-start)
- [Environment Variables](#environment-variables)
- [Authentication Methods](#authentication-methods)
- [Examples](#examples)
- [Contributing](#contributing)
- [Thanks](#thanks)
- [License](#license)

## Usage Scenario

Allows connecting to a remote server's ports (e.g., databases, web services) when only SSH port 22 is reachable. Perfect for accessing services behind firewalls or in secure networks through SSH tunneling with Docker port mapping.

## Features

- **Multi-platform support**: Works on both AMD64 and ARM64 (Apple Silicon M1/M2)
- **Multiple SSH tunnels**: Support for multiple simultaneous tunnels
- **Flexible authentication**: Password or private key authentication
- **Auto-restart**: Automatically restarts tunnels if they fail
- **Environment-based config**: Simple configuration via environment variables
- **Docker Compose ready**: Easy deployment with docker-compose

## Requirements

- SSH endpoint with public key or password-based authentication
- Docker or Docker Compose

## Quick Start

### Docker Compose (Recommended)

Create a `docker-compose.yml` file:

```yaml
version: '3.8'
services:
  sshtunneller:
    image: sshtunneller-arm64
    container_name: sshtunneller
    hostname: sshtunneller
    ports:
      - "3306:3306"
      - "5432:5432"
    environment:
      - ssh_host=your-ssh-server.com
      - ssh_port=22
      - ssh_username=root
      - ssh_private_key_password=your_key_password
      - remote_bind_addresses=[("127.0.0.1", 3306),("127.0.0.1", 5432)]
      - local_bind_addresses=[("0.0.0.0", 3306),("0.0.0.0", 5432)]
    volumes: 
      - ./path/to/private.key:/private.key:ro
    restart: always
```

Deploy with:
```bash
docker-compose up -d
```

### Docker Run

```bash
docker run -d \
  --name sshtunneller \
  -p 3306:3306 \
  -p 5432:5432 \
  -e ssh_host="your-ssh-server.com" \
  -e ssh_port="22" \
  -e ssh_username="root" \
  -e ssh_password="your_password" \
  -e remote_bind_addresses="[('127.0.0.1', 3306), ('127.0.0.1', 5432)]" \
  -e local_bind_addresses="[('0.0.0.0', 3306), ('0.0.0.0', 5432)]" \
  --restart always \
  sshtunneller-arm64
```

## Environment Variables

| Variable | Description | Required | Default |
|----------|-------------|----------|---------|
| `ssh_host` | SSH server hostname or IP address | ✅ Yes | - |
| `ssh_port` | SSH server port | No | `22` |
| `ssh_username` | SSH username | ✅ Yes | - |
| `ssh_password` | SSH password | No* | - |
| `ssh_private_key_password` | Private key passphrase | No | - |
| `remote_bind_addresses` | List of (host, port) tuples for remote binding | ✅ Yes | - |
| `local_bind_addresses` | List of (host, port) tuples for local binding | ✅ Yes | - |

*Either `ssh_password` or a private key mounted at `/private.key` is required.

## Authentication Methods

### 1. Private Key Authentication (Recommended)

Mount your private key file to `/private.key`:

```yaml
volumes: 
  - ./path/to/your/private.key:/private.key:ro
environment:
  - ssh_private_key_password=your_key_passphrase  # Optional
```

### 2. Password Authentication

```yaml
environment:
  - ssh_password=your_ssh_password
```

## Examples

### MySQL Database Tunnel
```yaml
version: '3.8'
services:
  mysql-tunnel:
    image: sshtunneller-arm64
    ports:
      - "3306:3306"
    environment:
      - ssh_host=database-server.com
      - ssh_username=user
      - ssh_password=password
      - remote_bind_addresses=[("127.0.0.1", 3306)]
      - local_bind_addresses=[("0.0.0.0", 3306)]
    restart: always
```

### Multiple Services (MySQL + PostgreSQL + Redis)
```yaml
version: '3.8'
services:
  multi-tunnel:
    image: sshtunneller-arm64
    ports:
      - "3306:3306"  # MySQL
      - "5432:5432"  # PostgreSQL
      - "6379:6379"  # Redis
    environment:
      - ssh_host=server.example.com
      - ssh_username=tunneluser
      - remote_bind_addresses=[("localhost", 3306),("localhost", 5432),("localhost", 6379)]
      - local_bind_addresses=[("0.0.0.0", 3306),("0.0.0.0", 5432),("0.0.0.0", 6379)]
    volumes:
      - ./ssh-keys/id_rsa:/private.key:ro
    restart: always
```

### Web Service Tunnel
```bash
docker run -d \
  --name web-tunnel \
  -p 8080:8080 \
  -e ssh_host="web-server.com" \
  -e ssh_username="webuser" \
  -e ssh_password="webpass" \
  -e remote_bind_addresses="[('127.0.0.1', 8080)]" \
  -e local_bind_addresses="[('0.0.0.0', 8080)]" \
  sshtunneller-arm64
```


## Contributing

Issues and pull requests are welcome! Please feel free to contribute to improve this project.

## Thanks

This project uses the excellent [SSHTunnel](https://github.com/pahaz/sshtunnel) Python library.

## License

MIT License

---

Enjoy secure SSH tunneling! 🎉
