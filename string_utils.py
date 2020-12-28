import math

# author: Yuval Ben Eliezer
class Ranger(object):
    def __init__(self,start_str, end_str):
        self._start_str = start_str
        self._end_str = end_str
        self._length = len(start_str)

    def _get_last_index_not_z(self, str_list):
        for i, char in enumerate(str_list[::-1]):
            if char is not 'z':
                return self._length - 1 - i

    def _make_all_chars_after_index_into_a(self, str_list, index):
        for i in range(index + 1, self._length):
            str_list[i] = 'a'

    def generate_all_from_to_of_len(self):
        tmp = list(self._start_str)
        last = list(self._end_str)
        yield "".join(tmp)
        while tmp != last:
            i = self._get_last_index_not_z(tmp)
            tmp[i] = chr(ord(tmp[i]) + 1)
            if i is not len(tmp) - 1:
                self._make_all_chars_after_index_into_a(tmp, i)
            yield "".join(tmp)
        yield "".join(last)

# author: Eliad Shem Tov

def cycle_string(char_arr , jump_size):
    char_arr = list(reversed(char_arr))
    base_26_to_10 = sum([ ( ord(char_arr[i]) - ord('a') )*(26**i) for i in range(len(char_arr))])
    base_26_to_10 += jump_size

    res_arr = []
    while len(res_arr) != len(char_arr):
        if base_26_to_10 == 0:
            res_arr += 'a'
            continue

        res_arr += chr( (base_26_to_10%26) + ord('a') )
        base_26_to_10 = int(math.floor(base_26_to_10/26))

    return list(reversed(res_arr))


def get_word_from_char_arr(char_arr):
    output = ""
    for c in char_arr:
        output += c

    return output


# splits the string-space fairly between the number of servers
def split_fairly(input_length : int, number_of_servers : int):
    from_string, to_string = [], []
    for __ in range(input_length):
        from_string += ["a"]
        to_string += ["z"]

    space_size = 26 ** input_length
    strings_per_server = int(math.floor(space_size / number_of_servers))

    ranges = []

    curr_from = from_string

    for k in range(number_of_servers):
        if k == number_of_servers-1:
            curr_to = to_string
        else:
            curr_to = cycle_string(curr_from , strings_per_server-1)

        ranges += [(get_word_from_char_arr(curr_from), get_word_from_char_arr(curr_to))]
        curr_from = cycle_string(curr_to , 1)

    return ranges


if __name__ == '__main__':
    ranges = split_fairly(13,5)