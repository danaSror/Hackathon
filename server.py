# The server is multi-threaded since it has to manage multiple clients
import socket
import getch
import message
import msg_utils

# server configuration #
TEAM_NAME = '-!-!-Rotem-&-Dana-!-!-'
HOST = '127.0.0.4'  # Standard loopback interface address (localhost)
SERVER_PORT = 13117       # Port to listen on (non-privileged ports are > 1023)
BROADCAST = "255.255.255.255"
OFFER_TIMEOUT = 1        # the server send udp broadcast every 1 sec

msg_utils = msg_utils.Msg_utils()

class Server:
    server_socket = None

    def __init__(self):
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP))
        self.server_socket.bind(("", SERVER_PORT))



    # 1. sending out offer messages 
    # 2. responding to request messages
    # 3. responding to new TCP connections
    # - leave this state after 10 seconds.
    def waiting_for_clients():
        print('Server started,listening on IP address 172.1.0.4...')
        # 1. sending out offer messages
        send_offer_messages()
        # 2. responding to request messages
        while True:
            message, client_address = self.server_socket.recvfrom(SERVER_PORT)
            decoded_message =msg_utils.decode(message)
            t = threading.Thread(target=self.talkToClient, args=(decoded_msg, client_address, time.time()))
            t.start()

    def send_offer_messages():
            discover_msg = message.Message("feedbeef", 2, SERVER_PORT)
            encoded = msg_utils.encode(discover_msg)
            self.server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1) # Enable broadcasting mode
            self.server_socket.sendto(encoded, (BROADCAST, SERVER_PORT))
            print("Sent offer")
   

    # 1. collect characters from the network 
    # 2. calculate the score
    # - leave this state after 10 seconds.
    def game_mode():
        pass    


if __name__ == "__main__":
      server = Server()
      server.waiting_for_clients()

    



# with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
#     s.bind((HOST, PORT))
#     s.listen()
#     print("Server started,listening on IP address 172.1.0.4")
#     conn, addr = s.accept()
#     with conn:
#         print('Connected by', addr)
#         while True:
#             data = conn.recv(1024)
            
#             print('Received from client - ', repr(data))
#             if not data:
#                 break
#             conn.sendall(data)