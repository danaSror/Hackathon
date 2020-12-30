# The client is a single-threaded app, which has three states
import socket
import struct
import threading
from pynput.keyboard import Listener
# from curtsies import Input


class Client:

    # client configuration #                     
    SERVER_PORT = 13117                     # The port used by the server
    client_connection_list = []
    buffer = 4096 

    def __init__(self,teamName):
        self.TEAM_NAME = teamName + '\n'
        # UDP
        self.client_socket_udf = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP) # UDP
        #self.client_socket_udf.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEPORT, 1)
        self.client_socket_udf.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1) #  Enable broadcasting mode
        self.client_socket_udf.bind(("", Client.SERVER_PORT))
        # TCP
        self.conn_tcp = None
    
    # leave this state when you get an offer message
    def wait_for_server_offer(self):
        print("Client started, listening for offer requests...")
        while True:
            data, addr = self.client_socket_udf.recvfrom(Client.buffer)
            cookie, msg_type, tcp_port_number = struct.unpack('IBH', data)
            if cookie == 0xfeedbeef and msg_type == 0x2 and tcp_port_number > 0:
               print(f"Received offer from {addr[0]}, attempting to connect...")
               tcp_server_port = int(tcp_port_number)
               server_ip = addr[0]
               tcp_thread = threading.Thread(target=self.execute_tcp_connection, args=(server_ip, tcp_server_port, self.TEAM_NAME )) #,name='TCP client')
               tcp_thread.start()
             
        

    def execute_tcp_connection(self,host_ip, tcp_server_port, team_name):
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_socket:
                self.conn_tcp = client_socket
                Client.client_connection_list.append(client_socket)
                print("1")
                client_socket.connect((host_ip, tcp_server_port))
                print("2")
                #client_socket.sendall(team_name.encode('utf-8'))
                client_socket.sendto(team_name.encode('utf-8'),(host_ip,tcp_server_port))
                print("3")
                while True:
                    data_from_server = client_socket.recv(Client.buffer)
                    print("4")
                    print(data_from_server.decode('utf-8'))
                    # self.game_mode()
        except:
            print("Server disconnected, listening for offer requests...")
            Client.client_connection_list.clear()
            self.wait_for_server_offer()

              

    # collect characters from the keyboard and send them over TCP. collect data from the network and print it onscreen
    # def game_mode(self):
    #     listener = Listener(on_press=on_press)
    #     listener.start()

        


if __name__ == "__main__":
    client = Client('-!-!-Rotem-&-Dana-!-!-')
    client.wait_for_server_offer()
