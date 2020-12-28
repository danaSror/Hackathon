DISCOVER = 1
OFFER = 2
REQUEST = 3
ACK = 4
NACK = 5

class Message:

    def __init__(self, team_name, type, hash, length, start, end):
        self.team_name = team_name
        self.type = type
        self.hash = hash
        self.length = length
        self.start = start
        self.end = end