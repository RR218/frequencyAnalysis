#!/usr/bin/env python3
import colorama
import operator
import sys

colorama.init(autoreset=True)

# Place cipher inside quotation marks """  """
cipher = """ """
cipher = cipher.lower()
print(colorama.Fore.BLUE + "\nCIPHER :\n")
print(cipher)

letterCount = len(cipher)
print(colorama.Fore.RED + "\nletter Count: " , str(letterCount) + "\n")


class Attack:
    def __init__(self):
        self.alphabet = "abcdefghijklmnopqrstuvwxyz"
        self.plain_chars_left = "abcdefghijklmnopqrstuvwxyz"
        self.cipher_chars_left = "abcdefghijklmnopqrstuvwxyz"
        self.freq = {}
        self.key = {}
        self.freq_eng = {'a': 0.0817, 'b': 0.0150, 'c': 0.0278, 'd': 0.0425, 'e': 0.1270, 'f': 0.0223,
                         'g': 0.0202, 'h': 0.0609, 'i': 0.0697, 'j': 0.0015, 'k': 0.0077, 'l': 0.0403,
                         'm': 0.0241, 'n': 0.0675, 'o': 0.0751, 'p': 0.0193, 'q': 0.0010, 'r': 0.0599,
                         's': 0.0633, 't': 0.0906, 'u': 0.0276, 'v': 0.0098, 'w': 0.0236, 'x': 0.0015,
                         'y': 0.0197, 'z': 0.0007}
        self.mappings = {}

    def calculate_freq(self, cipher):
        for c in self.alphabet:
            self.freq[c] = 0

        letter_count = 0
        for c in cipher:
            if c in self.freq:
                self.freq[c] += 1
                letter_count += 1

        for c in self.freq:
            self.freq[c] = round(self.freq[c] / letter_count, 4)

    def print_freq(self):
        new_line_count = 0
        for c in self.freq:
            print(colorama.Fore.BLUE + c, ':', self.freq[c],  ' ', end='')
            if new_line_count % 3 == 2:
                print()
            new_line_count += 1

    def calculate_matches(self):
        for cipher_char in self.alphabet:
            map = {}
            for plain_char in self.alphabet:
                map[plain_char] = round(abs(self.freq[cipher_char] - self.freq_eng[plain_char]), 4)
            self.mappings[cipher_char] = sorted(map.items(), key=operator.itemgetter(1))

    def set_key_mapping(self, cipher_char, plain_char):
        if cipher_char not in self.cipher_chars_left or plain_char not in self.plain_chars_left:
            print("ERROR: key mapping error", cipher_char, plain_char)
            sys.exit(-1)
        self.key[cipher_char] = plain_char
        self.plain_chars_left = self.plain_chars_left.replace(plain_char, "")
        self.cipher_chars_left = self.cipher_chars_left.replace(cipher_char, "")

    def guess_key(self):
        for cipher_char in self.cipher_chars_left:
            for plain_char, diff in self.mappings[cipher_char]:
                if plain_char in self.plain_chars_left:
                    self.key[cipher_char] = plain_char
                    self.plain_chars_left = self.plain_chars_left.replace(plain_char, '')
                    break

    def get_key(self):
        return self.key


def decrypt(key, cipher):
    message = ""
    for c in cipher:
        if c in key:
            message += key[c]
        else:
            message += c
    return (message)


attack = Attack()
attack.calculate_freq(cipher)
attack.print_freq()
attack.calculate_matches()

# Run the script multiple times in your text editor terminal / console
# and map the probable matches manually with the format as shown below.

# attack.set_key_mapping(p = plain text, c = cipher)

# EXAMPLES OF SUSPECTED MATCH:
# attack.set_key_mapping('m', 'a')
# attack.set_key_mapping('p', 'h')
# attack.set_key_mapping('r', 'e')
# attack.set_key_mapping('t', 'y')
# attack.set_key_mapping('v', 'c')
# attack.set_key_mapping('q', 'k')
# attack.set_key_mapping('x', 'f')
# attack.set_key_mapping('y', 'm')
# attack.set_key_mapping('e', 'v')
# attack.set_key_mapping('k', 'n')
# attack.set_key_mapping('s', 'p')
# attack.set_key_mapping('u', 'r')
# attack.set_key_mapping('d', 'd')
# attack.set_key_mapping('a', 'x')
# attack.set_key_mapping('c', 'w')
# attack.set_key_mapping('w', 'i')
# attack.set_key_mapping('b', 't')
# attack.set_key_mapping('', '')

attack.guess_key()
key = attack.get_key()
print("\n\n")
print(key)
print()
message = decrypt(key, cipher)
message_lines = message.splitlines()
cipher_lines = cipher.splitlines()
for i in range(len(message_lines)):
    print(colorama.Fore.CYAN + 'p:', colorama.Fore.CYAN + message_lines[i])
    print(colorama.Fore.RED + 'c:', colorama.Fore.RED + cipher_lines[i])
