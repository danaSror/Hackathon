import message
from struct import *

TN_LEN = 32
TYPE_LEN = 1
HASH_LEN = 40
ORIG_LEN_LEN = 1
START_LEN = 256
END_LEN = 256

TN_OFFSET = 0
TYPE_OFFSET = 32
HASH_OFFSET = 33
ORIG_LEN_OFFSET = 73
START_OFFSET = 74
END_OFFSET = 330



class Code_And_Decode():
    pass


    def decode(self, encoded_msg):
        team_name, type, hash, length = unpack('32sc40sc',encoded_msg[:74])
        team_name = team_name.decode('utf-8').strip()
        type = int.from_bytes(type, "big")
        hash = hash.decode('utf-8')
        length = int.from_bytes(length, "big")
        start, end = unpack('{0}s{0}s'.format(length),encoded_msg[74:])
        start = start.decode()
        end = end.decode()
        decoded_msg = message.Message(team_name, type, hash, length, start, end)
        return decoded_msg

    def encode(self, message):
        team_name = message.team_name.ljust(32).encode()
        type = bytes([message.type])
        hash = message.hash.encode()
        length = bytes([message.length])
        start = message.start.encode()
        end = message.end.encode()
        _format = '32sc40sc{0}s{0}s'.format(message.length)
        encoded_msg = pack(_format, team_name, type, hash, length, start, end)
        return encoded_msg