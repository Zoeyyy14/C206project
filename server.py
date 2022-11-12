
import socket
from  threading import Thread

SERVER = None
PORT = None
IP_ADDRESS = None

CLIENTS = {}
playerNames=[]



def acceptConnections():
    global CLIENTS
    global SERVER

    while True:
        player_socket, addr = SERVER.accept()
        player_name=player_socket.recv(1024).decode().strip()
        if(len(CLIENTS.keys())==0):
            CLIENTS[player_name]={'player_type':'player1'}
        else:
            CLIENTS[player_name]={'player_type':'player2'}

        CLIENTS[player_name]["player_socket"]=player_socket
        CLIENTS[player_name]["address"]=addr
        CLIENTS[player_name]["player_name"]=player_name
        CLIENTS[player_name]["turn"]=False
        
        print(f"Connection is establish with{player_name}:{addr}")

def setup():
    print("\n")
    print("\t\t\t\t\t\t*** Welcome to Tambola Game ***")

    global SERVER
    global PORT
    global IP_ADDRESS

    IP_ADDRESS = '127.0.0.1'
    PORT = 5000
    SERVER = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    SERVER.bind((IP_ADDRESS, PORT))

    SERVER.listen(10)

    print("\t\t\t\tSERVER IS WAITING FOR INCOMMING CONNECTIONS...")
    print("\n")

    acceptConnections()


setup()
