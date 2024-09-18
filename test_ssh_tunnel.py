from sshtunnel import SSHTunnelForwarder

server = SSHTunnelForwarder(
    ("localhost", 22222),
    ssh_username="root",
    ssh_pkey="/home/eon/workspace/fake-switches/id_rsa_fake",
    remote_bind_address=('192.168.1.101', 23),
    local_bind_address=("127.0.0.1", 10023)
)

server.start()

print(server.local_bind_port)  # show assigned local port
# work with `SECRET SERVICE` through `server.local_bind_port`.

server.stop()
