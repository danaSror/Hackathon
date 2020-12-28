# The client is a single-threaded app, which has three states
import socket


# client configuration #
TEAM_NAME = '-!-!-Rotem-&-Dana-!-!-'
HOST = '127.0.0.1'                      # The server's hostname or IP address
SERVER_PORT = 13117                     # The port used by the server
BROADCAST = "255.255.255.255"
OFFER_TIMEOUT = 1

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM ,socket.IPPROsocket.IPPROTO_UDP) # UDP
client_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEPORT, 1)
client.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1) #  Enable broadcasting mode
client.bind(("", PORT))

# leave this state when you get an offer message
def wait_for_server_offer():
    client_sock.settimeout(OFFER_TIMEOUT)
    try:
        while True:
            (message, server_address) = client_socket.recvfrom(2048)
    except socket.timeout:
        return


# leave this state when you successfully connect using TCP
def connect_to_server():
    pass


# collect characters from the keyboard and send them over TCP. collect data from the network and print it onscreen
def game_mode():
    # Note that in game mode the client responds to two events: 1. both keyboard presses 2. data coming in over TCP.
    # After connecting, the client sends the predefined team name to the server, followed by a line break (‘\n’).
    # After that, the client simply prints anything it gets from the server onscreen
    # sends anything it gets from the keyboard to the server
    pass


if __name__ == "__main__":
    
    #client_socket.connect((HOST, PORT))
    var = struct.pack('cc', 'd'.encode('ascii'), 'a'.encode('ascii'))
    client_socket.sendto(var, (HOST, PORT))




#with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
#    s.connect((HOST, PORT))
#    print("client connected to server")
#    s.sendall(b'Hello, world')
#    data = s.recv(1024)

#print('Received', repr(data))