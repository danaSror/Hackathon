# The server is multi-threaded since it has to manage multiple clients
import socket
#import getch
import time
import struct
from threading import Thread
import threading

global glob_connections_counter, client_list_thread  
glob_connections_counter = 0  
client_list_thread = [] 

class Server:
    # server configuration #
    SERVER_PORT = 13117       # Port to listen on (non-privileged ports are > 1023)
    OFFER_TIMEOUT = 1        # the server send udp broadcast every 1 sec
    tcp_port=40440
    IP = socket.gethostbyname(socket.gethostname())
    buffer = 4096
    

    def __init__(self):
        # UDP
        self.server_socket_udp = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP) #, socket.IPPROTO_UDP)
        self.server_socket_udp.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEPORT, 1)
        self.server_socket_udp.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1) # Enable broadcasting mode
        
        #TCP
        self.conn_tcp = None
        
        self.group_1 = []
        self.group_2 = []
        self.score_for_group_1 = 0
        self.score_for_group_2 = 0
        self.group_1_keyboard = {}
        self.group_2_keyboard = {}

    def start(self):
        self.clear_all()
        tcp = threading.Thread(target=self.execute_tcp_connection, name='TCP server')#, name='TCP server')
        udp = threading.Thread(target=self.execute_udp_connection,args=(tcp,), name='UDP server')
        udp.start()
    
    def execute_udp_connection(self,tcp_thread):
        print("3")
        print('Server started,listening on IP address {}...'.format(server.IP))
        tcp_thread.start()
        while True:
            Game_started = False
            # sending offers during the first 10 sec
            for i in range(10):
                # sending_broadcast_offers
                msg = struct.pack('IBH', 0xfeedbeef, 0x2, Server.tcp_port)
                self.server_socket_udp.sendto(msg, ('<broadcast>', Server.SERVER_PORT))
                print("Sent offer")
                time.sleep(1)
                
            # after client connected start the game during 10 sec    
            for i in range(10):
                if glob_connections_counter >= 1:
                    self.Game_Mode(Game_started)
                    time.sleep(1)
                    Game_started = True
                else:
                    print("Waitting for clients")
                    break
            
            winners = 0
            if self.score_for_group_1 >= self.score_for_group_2:
                winners = 1
                teams_name = ""
                for team in self.group_1:
                    teams_name += team[0]
            else:
                winners = 2
                teams_name = ""
                for team in self.group_2:
                    teams_name += team[0]
            
            message_to_send = "Game over!\n" + "Group 1 typed in {} characters. Group 2 typed in {} characters.\n".format(self.score_for_group_1,self.score_for_group_2)
            message_to_send += "Group {} wins!\n\n".format(winners) +  "Congratulation to the winners:\n"      
            message_to_send +=  "{}".format(teams_name)

            all_teams = self.group_1 + self.group_2
            for team in all_teams:
                if team[2]: # 2 represent the index of the team connection
                    try:
                        team[2].sendall(message_to_send.encode('utf-8'))
                        team[2].close()
                    except:
                        print("End game for client failed")
                        pass

            # after close all the client connection      
            print("Game over!"+ '\n'+"Sending out offer requests...")
            for t in client_list_thread:
                    try:
                        t.join()
                    except:
                        pass
            self.clear_all()

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

    def clear_all(self):
        self.group_1 = []
        self.group_2 = []
        self.score_for_group_1 = 0
        self.score_for_group_2 = 0
        self.group_1_keyboard = {}
        self.group_2_keyboard = {}
        global glob_connections_counter , client_list_thread  
        glob_connections_counter = 0  
        client_list_thread = []
    
    def execute_tcp_connection(self): 
        global glob_connections_counter
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server:
            self.conn_tcp = server
            server.bind((Server.IP, Server.tcp_port))
            server.listen()
            while True:
                client_conn, client_addr = server.accept()
                glob_connections_counter = glob_connections_counter + 1
               
                client_thread = threading.Thread(target=self.get_client_tcp_msg,args=(client_conn, client_addr)
                                                ,name=f'Client_{glob_connections_counter}') 
                client_list_thread.append(client_thread)
                client_thread.start()
                   
    def get_client_tcp_msg(self, client_conn, client_addr):
        first_msg = True
        try:
            while True:
                client_data = client_conn.recv(Server.buffer)
                if not client_data:
                    break
                elif first_msg:
                    #print("Team name:" + client_data.decode('utf-8'))  # TODO DELETE
                    team_name = client_data.decode('utf-8')
                    self.divide_teams(team_name, client_addr,client_conn)
                    first_msg = False
                else:
                    #print(f"Received from client {client_data.decode('utf-8')}")
                    self.calculate_score(client_addr) 
        except:
            pass
    
    def calculate_score(self,client_addr):
        for team in self.group_1:
            if team[1][1] == client_addr[1]:
                self.score_for_group_1 += 1
        for team in self.group_2:
            if team[1][1] == client_addr[1]:
                self.score_for_group_2 += 1
  
    def divide_teams(self,team_name, client_address,client_connection):
        if len(self.group_1) > len(self.group_2):
            self.group_2.append((team_name, client_address,client_connection, 0))
        else:
            self.group_1.append((team_name, client_address,client_connection, 0))
        
       
       

if __name__ == "__main__":
    server = Server()
    server.start()
      
   
    #   tcp.start()

    #   udp.join()
    #   tcp.join()
      

    



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
