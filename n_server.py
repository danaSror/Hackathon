# The server is multi-threaded since it has to manage multiple clients
import socket

# server configuration #
TEAM_NAME = '-!-!-Rotem-&-Dana-!-!-'
HOST = '127.0.0.4'  # Standard loopback interface address (localhost)
SERVER_PORT = 13117       # Port to listen on (non-privileged ports are > 1023)

class Server:
    server_socket = None

    def __init__(self):
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.server_socket.bind(("", SERVER_PORT))

    def talkToClient(self, user_message: message.Message, ip, start_time):
            server_response = self.process_message(user_message, user_message.length, start_time)
            self.server_socket.sendto(server_response, ip)

    # 1. sending out offer messages 
    # 2. responding to request messages
    # 3. responding to new TCP connections
    # - leave this state after 10 seconds.
    def waiting_for_clients():
        print('Server started,listening on IP address 172.1.0.4...')
        while True:
            msg, client = self.server_socket.recvfrom(SERVER_PORT)
            decoded_msg =encoder_decoder.decode(msg)
            if decoded_msg.type == 2:
                print('sent: offer')
            t = threading.Thread(target=self.talkToClient, args=(decoded_msg, client, time.time()))
            t.start()

    # 1. collect characters from the network 
    # 2. calculate the score
    # - leave this state after 10 seconds.
    def game_mode():
        pass    


if __name__ == "__main__":
    server = Server()
    



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