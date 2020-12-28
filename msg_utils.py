import message
from struct import *


class Msg_utils():
    pass

  
    def decode(self, encoded_msg):
        magic_cookie,type, server_port = unpack('4sc2s',encoded_msg)
        magic_cookie = magic_cookie.decode('utf-8')
        type = int.from_bytes(type, "big")
        server_port = int.from_bytes(server_port, "big")
        decoded_msg = message.Message(magic_cookie, type, server_port)
        return decoded_msg

    def encode(self, message):
        magic_cookie = message.magic_cookie.encode()
        type = bytes([message.type])
        server_port = bytes([message.server_port])
        encoded_msg = pack('4sc2s', magic_cookie,type, server_port)
        return encoded_msg
        