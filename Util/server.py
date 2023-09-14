import socket
import selectors
import threading
import types

# sel = selectors.DefaultSelector()
SERVER = "127.0.0.1"  # Standard loopback interface address (localhost)
PORT = 5050  # Port to listen on (non-privileged ports are > 1023)
ADDR = (SERVER, PORT)
header = 64
FORMAT = "utf-8"
DISCONNECT_MESSAGE = "!DISCONNECT" 
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(ADDR)
subscribers = {}

def handle_client(conn, addr):
    print(f"[NEW CONNECTION] {addr}, ")
    connected = True
    while connected:
        msg_length = conn.recv(header).decode(FORMAT)
        if msg_length:
            msg_length = int(msg_length)
            msg = conn.recv(msg_length).decode(FORMAT)
            print(f"[{addr}] {msg}")
            if msg == DISCONNECT_MESSAGE:
                connected = False
            conn.send("Message recieved".encode(FORMAT))
    conn.close()

def run_server():
    server.listen()
    print(f"[LISTENING] Server is listening on {SERVER}")
    while True:
        conn, addr = server.accept()
        client_thread = threading.Thread(target=handle_client, args=(conn, addr))
        client_thread.start()
        print(f"[ACTIVE CONNECTIONS] {threading.active_count() - 1}")

try:
    print("[STARTING] Server is starting up")
    run_server()
except KeyboardInterrupt:
    print("Caught keyboard interrupt, exiting")
finally:
    server.close()

# def accept_wrapper(sock):
#     conn, addr = sock.accept()  # Should be ready to read
#     print(f"Accepted connection from {addr}")
#     conn.setblocking(False)
#     data = types.SimpleNamespace(addr=addr, inb=b"", outb=b"")
#     events = selectors.EVENT_READ | selectors.EVENT_WRITE
#     sel.register(conn, events, data=data)

# def service_connection(key, mask):
#     sock = key.fileobj
#     data = key.data
#     if mask & selectors.EVENT_READ:
#         recv_data = sock.recv(1024)  # Should be ready to read
#         if recv_data:
#             data.outb += recv_data
#         else:
#             print(f"Closing connection to {data.addr}")
#             sel.unregister(sock)
#             sock.close()
#     if mask & selectors.EVENT_WRITE:
#         if data.outb:
#             print(f"Echoing {data.outb!r} to {data.addr}")
#             sent = sock.send(data.outb)  # Should be ready to write
#             data.outb = data.outb[sent:]

# try:
#     while True:
#         events = sel.select(timeout=None)
#         for key, mask in events:
#             if key.data is None:
#                 accept_wrapper(key.fileobj)
#             else:
#                 service_connection(key, mask)
# except KeyboardInterrupt:
#     print("Caught keyboard interrupt, exiting")
# finally:
#     sel.close()
