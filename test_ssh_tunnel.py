
import io
import paramiko
from sshtunnel import SSHTunnelForwarder

with open('id_rsa_fake', 'r') as file:
    proxy_ssh_key = file.read().rstrip()
    

private_key = paramiko.RSAKey.from_private_key(
    io.StringIO(proxy_ssh_key)
)
    
server = SSHTunnelForwarder(
    ("localhost", 22222),
    ssh_username="root",
    ssh_pkey=private_key,
    remote_bind_address=('192.168.27.101', 23),
    local_bind_address=("127.0.0.1", 10023)
)

server.start()

print(server.local_bind_port)  # show assigned local port

server.stop()
