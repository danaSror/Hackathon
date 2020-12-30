# The server is multi-threaded since it has to manage multiple clients
import socket
#import getch
import message
import time
import msg_utils
import struct
from threading import Thread
import threading

global glob_connections_counter  #   TODO change names of boris
glob_connections_counter = 0  #   TODO change names of boris
client_list_thread = [] #   TODO change names of boris

class Server:
    # server configuration #
    TEAM_NAME = '-!-!-Rotem-&-Dana-!-!-'
    SERVER_PORT = 13117       # Port to listen on (non-privileged ports are > 1023)
    OFFER_TIMEOUT = 1        # the server send udp broadcast every 1 sec
    tcp_port=40440
    IP = socket.gethostbyname(socket.gethostname())
    buffer = 4096 #   TODO change names of boris


    def __init__(self):
        # UDP
        self.server_socket_udp = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP) #, socket.IPPROTO_UDP)
        #self.server_socket_udp.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEPORT, 1)
        self.server_socket_udp.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1) # Enable broadcasting mode
        
        #TCP
        self.conn_tcp = None

        self.group_1 = []
        self.group_2 = []


    def execute_tcp_connection(self): 
        global glob_connections_counter
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server:
            self.conn_tcp = server
            print("1")
            server.bind((Server.IP, Server.tcp_port))
            print("2")
            server.listen()
            print("3")
            while True:
                print("4")
                client_conn, client_addr = server.accept()
                print("5")
                glob_connections_counter = glob_connections_counter + 1
                if glob_connections_counter <= 4:
                    client_thread = threading.Thread(target=self.get_client_tcp_msg,args=(client_conn, client_addr)
                                                    ,name=f'Client_{glob_connections_counter}') 
                    client_list_thread.append(client_thread)
                    client_thread.start()
                    print("6")

    def get_client_tcp_msg(self, client_conn, client_addr):
        print("H1")
        first_msg = True
        try:
            while True:
                client_data = client_conn.recv(Server.buffer)
                print("H2")
                if not client_data:
                    break
                if first_msg:
                    print("Team name:" + client_data.decode('utf-8'))  # TODO DELETE
                    team_name = client_data.decode('utf-8')
                    self.randomly_divide_teams(team_name, client_addr,client_conn)
                    first_msg = False
                else:
                    print(f"Received from client {client_data.decode('utf-8')}")
                    #Handle_Game(client_address) 
        except:
            pass
    
    def randomly_divide_teams(self,team_name, client_address,client_connection):
        if len(self.group_1) > len(self.group_2):
            self.group_2.append((team_name, client_address,client_connection, 0))
        else:
            self.group_1.append((team_name, client_address,client_connection, 0))
        
    def sending_broadcast_offers(self):
            msg = struct.pack('IBH', 0xfeedbeef, 0x2, Server.tcp_port)
            self.server_socket_udp.sendto(msg, ('<broadcast>', Server.SERVER_PORT))
            print("Sent offer")
            

    # 1. collect characters from the network 
    # 2. calculate the score
    # - leave this state after 10 seconds.
    def game_mode(self):
        pass    

    def execute_udp_connection(self):
        print('Server started,listening on IP address {}...'.format(server.IP))
        while True:
            Game_started = False
            # sending offers during the first 10 sec
            for i in range(10):
                self.sending_broadcast_offers()
                time.sleep(1)
                

            # after client connected start the game during 10 sec    
            for i in range(10):
                self.Game_Mode(Game_started)
                time.sleep(1)
                Game_started = True

            #Terminate_Teams_Conecction() TODO
            print("Game over, sending out offer requests...")
            #Stop_All_Client_Threads() TODO
            #Reset()  TODO

    def Game_Mode(self, is_game_started):
         if not is_game_started:
            welcome_message = "Welcome to Keyboard Spamming Battle Royale.\n"
            welcome_message += 'Group 1:\n==\n'
            for team in self.group_1:
                welcome_message += team[0] # concatenate the team name
            welcome_message += 'Group 2:\n==\n'
            for team in self.group_2:
                welcome_message += team[0] # concatenate the team name
            welcome_message += 'Start pressing keys on your keyboard as fast as you can!!'

            all_teams = self.group_1 + self.group_2
            for team in all_teams:
                team[2].sendall(welcome_message.encode('utf-8')) # 2 represent the connection of client

if __name__ == "__main__":
      server = Server()
      udp = threading.Thread(target=server.execute_udp_connection, daemon=True)
      tcp = threading.Thread(target=server.execute_tcp_connection)#, name='TCP server')

      udp.start()
      tcp.start()

      udp.join()
      tcp.join()
      

    



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
