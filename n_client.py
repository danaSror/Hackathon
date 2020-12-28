# The client is a single-threaded app, which has three states
import socket


# client configuration #
TEAM_NAME = '-!-!-Rotem-&-Dana-!-!-'
HOST = '127.0.0.1'                      # The server's hostname or IP address
SERVER_PORT = 13117                     # The port used by the server
BROADCAST = "255.255.255.255"
OFFER_TIMEOUT = 1


# leave this state when you get an offer message
def wait_for_server_offer():
    pass

# leave this state when you successfully connect using TCP
def connect_to_server(ip):
    pass


# collect characters from the keyboard and send them over TCP. collect data from the network and print it onscreen
def game_mode(server_socket):
    # Note that in game mode the client responds to two events: 1. both keyboard presses 2. data coming in over TCP.
    # After connecting, the client sends the predefined team name to the server, followed by a line break (‘\n’).
    # After that, the client simply prints anything it gets from the server onscreen
    # sends anything it gets from the keyboard to the server
    pass


if __name__ == "__main__":
    

#with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
#    s.connect((HOST, PORT))
#    print("client connected to server")
#    s.sendall(b'Hello, world')
#    data = s.recv(1024)

#print('Received', repr(data))