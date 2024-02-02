from constants import *
def hex2binary_code(code16: str):  # code16 is smth like 0xA78679B
    if LOCAL_DEBUG:
        assert code16[:2] == "0X"
        for c in code16[2:]:
            assert ord('0') <= ord(c) <= ord('9') or ord('A') <= ord(c) <= ord('F')

    code2 = [0 for _ in range((len(code16) - 2) * 4)]
    for i in range(2, len(code16)):
        for j in range(4):
            code2[(i - 2) * 4 + j] = chars16_to_2[code16[i]][j]
    return code2


def int2code2(x: int, bits: int) -> list[int]:
    code = [0 for _ in range(bits)]
    x %= (1 << bits)
    if x >= (1 << (bits - 1)):
        x -= (1 << bits)
    if LOCAL_DEBUG:
        assert -(1 << (bits - 1)) <= x < (1 << bits)
    if x < 0:
        code[0] = 1
        x += (1 << (bits - 1))
    for i in range(bits - 1, 0, -1):
        code[i] = x % 2
        x >>= 1
    return code


def int2bin(x: int, bits: int): # returns x converted in bits
    return [1 if (x & (1 << (bits - 1 - i))) else 0 for i in range(bits)]


def bin_code2int(code: list[int]):
    t = 0
    for i in range(len(code)):
        t += (1 << i) * code[len(code) - 1 - i]
    return t


def string_can_be_converted_to_int(string):
    for c in string:
        if c not in "0123456789":
            return False
    return True

def least_bits_needed(x: int): # минимальное число битов для x, то есть наименьшее L такое что (1 << L) > x
    L = 0
    while (1 << L) <= x:
        L += 1
    return L

def check_for_valid_hex(s: str):
    if len(s) < 3 or (s[:2] != "0x" and s[:2] != "0X"):
        return False
    for c in s[2:]:
        if c not in hex_string and c not in hex_string.lower():
            return False
    return True
