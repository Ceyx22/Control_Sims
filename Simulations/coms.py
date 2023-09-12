import threading
import socket

HEADER = 64
PORT = 5050 
FORMAT = 'utf-8' 
DISCONNECT_MESSAGE = "!DISCONNECT" 
SERVER = "127.0.0.1"
ADDR = (SERVER, PORT)

# Might have to switch to a queue method
# UNFINISHED SUBCRIBER CLASS NEED TO FINISH

class Publisher:
    def __init__(self, name, topic):
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client.connect(ADDR)
        self.name = name
        self.topic = topic
 
    def publish(self, msg):
        message = msg.encode(FORMAT)
        msg_length = len(message)
        send_length = str(msg_length).encode(FORMAT)
        send_length += b' ' * (HEADER - len(send_length))
        self.client.send(send_length)
        self.client.send(message)
        print(self.client.recv(2048).decode(FORMAT))
 
class Subscriber:
    def __init__(self, name, topic):
        self.name = name
        self.topic =  topic
        self.message = None
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client.connect(ADDR)
 
    def listen(self):
        print(self.client.recv(2048).decode(FORMAT))
        

pub = Publisher("pokemon", "fire")
pub.publish("testing")
pub.publish(DISCONNECT_MESSAGE)