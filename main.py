#! /usr/bin/env python3

import hashlib
from datetime import date
from optparse import OptionParser
from time import strftime, localtime
from colorama import Fore, Back, Style

status_color = {
    '+': Fore.GREEN,
    '-': Fore.RED,
    '*': Fore.YELLOW,
    ':': Fore.CYAN,
    ' ': Fore.WHITE
}

def display(status, data, start='', end='\n'):
    print(f"{start}{status_color[status]}[{status}] {Fore.BLUE}[{date.today()} {strftime('%H:%M:%S', localtime())}] {status_color[status]}{Style.BRIGHT}{data}{Fore.RESET}{Style.RESET_ALL}", end=end)

def get_arguments(*args):
    parser = OptionParser()
    for arg in args:
        parser.add_option(arg[0], arg[1], dest=arg[2], help=arg[3])
    return parser.parse_args()[0]

hash_algorithms = {
    "md5" : hashlib.md5,
    "sha1" : hashlib.sha1,
    "sha224" : hashlib.sha224,
    "sha256" : hashlib.sha256,
    "sha384" : hashlib.sha384,
    "sha3_224" : hashlib.sha3_224,
    "sha3_256" : hashlib.sha3_256,
    "sha3_384" : hashlib.sha3_384,
    "sha3_512" : hashlib.sha3_512,
    "sha512" : hashlib.sha512,
    "shake_128" : hashlib.shake_128,
    "shake_256" : hashlib.shake_256,
}
chars = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9', 'a', 'b', 'c', 'd', 'e', 'f']

if __name__ == "__main__":
    data = get_arguments(('-H', "--hash", "hash", f"Hashing Algorithm ([{', '.join(hash_algorithms.keys())}])"))
    if not data.hash or data.hash not in hash_algorithms.keys():
        display('-', f"Please Select a Hashing Algorithm ({Back.YELLOW}[{', '.join(hash_algorithms.keys())}]{Back.RESET})")
        exit(0)
    starting_length = 2
    try:
        while True:
            permutation = 0
            repeat = -1
            while repeat < 1:
                    starting = list(reversed([chars[(permutation//(1 if j == 0 else j * len(chars)))%len(chars)] for j in range(starting_length)]))
                    sentence = f"The {data.hash} hash of this sentence starts with {','.join(starting[:-1])} and {starting[-1]}"
                    starting = ''.join(starting)
                    if hash_algorithms[data.hash](sentence.encode()).hexdigest().startswith(starting):
                          print(f"\r{Back.GREEN}{sentence}{Back.RESET} => {Back.BLUE}{hash_algorithms[data.hash](sentence.encode()).hexdigest()}{Back.RESET}")
                    permutation += 1
                    if starting == '0' * starting_length:
                        repeat += 1
            starting_length += 1
            display('*', f"Current Starting Length = {Back.MAGENTA}{starting_length}{Back.RESET}", start='\r', end='')
    except KeyboardInterrupt:
        display(':', f"Keyboard Interrupt Detected...Exiting!", start='\n')