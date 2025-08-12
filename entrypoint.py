import os
import ast
from sshtunnel import SSHTunnelForwarder

ssh_host = os.getenv("ssh_host")
ssh_port = int(os.getenv("ssh_port", 22))
ssh_username = os.getenv("ssh_username")
ssh_password = os.getenv("ssh_password")
ssh_pkey = "/private.key" if os.path.exists("/private.key") else None
ssh_private_key_password = os.getenv("ssh_private_key_password")

remote_bind_addresses = ast.literal_eval(os.getenv("remote_bind_addresses"))
local_bind_addresses = ast.literal_eval(os.getenv("local_bind_addresses"))

tunnels = []

for (remote_host, remote_port), (local_host, local_port) in zip(remote_bind_addresses, local_bind_addresses):
    kwargs = {
        "ssh_address_or_host": (ssh_host, ssh_port),
        "ssh_username": ssh_username,
        "remote_bind_address": (remote_host, remote_port),
        "local_bind_address": (local_host, local_port),
    }

    if ssh_password:
        kwargs["ssh_password"] = ssh_password
    if ssh_pkey:
        kwargs["ssh_pkey"] = ssh_pkey
    if ssh_private_key_password:
        kwargs["ssh_private_key_password"] = ssh_private_key_password

    if not ("ssh_password" in kwargs or "ssh_pkey" in kwargs):
        raise ValueError("❌ No SSH password or key found in environment or mounted volume.")

    server = SSHTunnelForwarder(**kwargs)
    server.start()
    tunnels.append(server)
    print(f"✅ Tunnel started: {local_host}:{local_port} → {remote_host}:{remote_port}")

try:
    while True:
        pass
except KeyboardInterrupt:
    for t in tunnels:
        t.stop()
