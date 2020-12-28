import socket
import string_utils
import math
import encoder_decoder
import message
import itertools as it
import time

# client configuration #

BROADCAST = "255.255.255.255"
SERVER_PORT = 3117
TEAM_NAME = ';Drop table students; --'
OFFER_TIMEOUT = 1
ACK_TIMEOUT = 30
NUM_OF_LETTERS = 26
WORKERS = []

client_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
enc_dec = encoder_decoder.Encoder_decoder()



def main():
    hashed_string = input('Welcome to ' + TEAM_NAME + '.' + ' Please enter the hash:\n')
    if not_valid(hashed_string):
        return
    str_length = input('Please enter the input string length:\n')
    str_length = int(str_length)
    send_discover()
    wait_for_offers()
    jobs = create_jobs(str_length, len(WORKERS))
    send_requests(WORKERS, jobs, hashed_string)
    ans = wait_for_ack()
    print('The input string is ' + ans)


def send_requests(workers, jobs, hashed_string):
    i = 0
    for worker in workers:
        send_request(worker, jobs[i], hashed_string)
        i = i + 1


def send_request(worker, job, hashed_string):
    length = len(job[0])
    req_msg = message.Message(TEAM_NAME, message.REQUEST, hashed_string, length, job[0], job[1])
    encoded_msg = enc_dec.encode(req_msg)
    client_sock.sendto(encoded_msg, (worker[0], SERVER_PORT))


def send_discover():
    discover_msg = message.Message(TEAM_NAME, message.DISCOVER, "", 1, "", "")
    encoded = enc_dec.encode(discover_msg)
    client_sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
    client_sock.sendto(encoded, (BROADCAST, SERVER_PORT))


def wait_for_offers():
    client_sock.settimeout(OFFER_TIMEOUT)
    try:
        while 1:
            (message, server_address) = client_sock.recvfrom(2048)
            WORKERS.append(server_address)
    except socket.timeout:
        return


def split_to_chunks(lst, each):
    return list(it.zip_longest(*[iter(lst)] * each))


def divide(length, num_servers):
    start = 'a' * length
    end = 'z' * length
    search_space = string_utils.Ranger(start, end)
    num_strings = NUM_OF_LETTERS ** length
    strings = search_space.generate_all_from_to_of_len()
    each = math.ceil(num_strings / num_servers)
    chunks = split_to_chunks(strings,each)
    return chunks


def create_jobs(length, num_servers):
    jobs = []
    chunks = string_utils.split_fairly(length,num_servers)
    for chunk in chunks:
        jobs.append((chunk[0], chunk[-1]))
    return jobs


def not_valid(hashed_string):
    length = len(hashed_string)
    if length != 40:
        print('Input string must be of length 40.')
        return True
    try:
        sha_int = int(hashed_string, 16)
    except ValueError:
        print('Input string must be sh1 hash.')
        return True
    return False


def wait_for_ack():
    start_time = time.time()
    client_sock.settimeout(None)
    while 1:
        if time.time() - start_time > ACK_TIMEOUT:
            return '[ACK timeout!]'
        (msg, server_address) = client_sock.recvfrom(2048)
        decoded_msg = enc_dec.decode(msg)
        if decoded_msg.type == message.ACK:
            return decoded_msg.start
        elif decoded_msg.type == message.NACK:
            WORKERS.remove(server_address)

        if len(WORKERS) == 0:  # all servers returned NACK
            return 'not found!'


if __name__ == "__main__":
    main()