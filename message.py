OFFER = 2

class Message:

    def __init__(self, magic_cookie, type, server_port magic_cookie, type, server_port):
        self.magic_cookie = magic_cookie # (4 bytes): 0xfeedbeef
        self.type = type # (1 byte): 0x2
        self.server_port = server_port # (2 bytes)
        
        