from itertools import count
import struct

BIT_64 = 64
BYTE_2_BITS = 8
WORD_SIZE = 4
WORD_SIZE_2_BITS = 32
CHUNK_SIZE = 64
CHUNK_SIZE_2_BITS = CHUNK_SIZE * BYTE_2_BITS

# addition is calculated modulo 2**32
MOD = 0xFFFFFFFF

INIT_HASH = [
    0x6a09e667,
    0xbb67ae85,
    0x3c6ef372,
    0xa54ff53a,
    0x510e527f,
    0x9b05688c,
    0x1f83d9ab,
    0x5be0cd19,
]
    
ROUND_CONSTS = [
    0x428a2f98, 0x71374491, 0xb5c0fbcf, 0xe9b5dba5, 0x3956c25b, 0x59f111f1, 
    0x923f82a4, 0xab1c5ed5, 0xd807aa98, 0x12835b01, 0x243185be, 0x550c7dc3, 
    0x72be5d74, 0x80deb1fe, 0x9bdc06a7, 0xc19bf174, 0xe49b69c1, 0xefbe4786, 
    0x0fc19dc6, 0x240ca1cc, 0x2de92c6f, 0x4a7484aa, 0x5cb0a9dc, 0x76f988da,
    0x983e5152, 0xa831c66d, 0xb00327c8, 0xbf597fc7, 0xc6e00bf3, 0xd5a79147, 
    0x06ca6351, 0x14292967, 0x27b70a85, 0x2e1b2138, 0x4d2c6dfc, 0x53380d13, 
    0x650a7354, 0x766a0abb, 0x81c2c92e, 0x92722c85, 0xa2bfe8a1, 0xa81a664b, 
    0xc24b8b70, 0xc76c51a3, 0xd192e819, 0xd6990624, 0xf40e3585, 0x106aa070, 
    0x19a4c116, 0x1e376c08, 0x2748774c, 0x34b0bcb5, 0x391c0cb3, 0x4ed8aa4a, 
    0x5b9cca4f, 0x682e6ff3, 0x748f82ee, 0x78a5636f, 0x84c87814, 0x8cc70208, 
    0x90befffa, 0xa4506ceb, 0xbef9a3f7, 0xc67178f2,
]


def sha_256(message: bytes | str) -> bytes:
    """Returns the hash of the input using the SHA-256 cryptographic hash function

    For more informations check: `https://en.wikipedia.org/wiki/SHA-2#Pseudocode`
    """

    if type(message) is str:
        message = message.encode("utf-8")

    hash_values = INIT_HASH.copy()

    L = len(message) * BYTE_2_BITS
    K = _find_K(L)
    K = b"\x00" * (K // BYTE_2_BITS)
    L = struct.pack(">Q", L)
    message = message + b"\x80" + K + L

    for i in range(0, len(message), CHUNK_SIZE):
        chunk = message[i: i + CHUNK_SIZE]
        w = [0] * CHUNK_SIZE

        w[:16] = [
            struct.unpack(">I", chunk[i: i + WORD_SIZE])[0]
            for i in range(0, CHUNK_SIZE, WORD_SIZE)
        ]
        
        for i in range(16, CHUNK_SIZE):
            w0 = w[i - 15]
            w1 = w[i - 2]
            s0 = right_rotate(w0, 7) ^ right_rotate(w0, 18) ^ right_shift(w0, 3)
            s1 = right_rotate(w1, 17) ^ right_rotate(w1, 19) ^ right_shift(w1, 10)
            w[i] = (w[i - 16] + s0 + w[i - 7] + s1) & MOD
        
        a, b, c, d, e, f, g, h = hash_values

        for i in range(64):
            s1 = right_rotate(e, 6) ^ right_rotate(e, 11) ^ right_rotate(e, 25)
            ch = (e & f) ^ (~e & g)
            temp1 = (h + s1 + ch + ROUND_CONSTS[i] + w[i]) & MOD
            s0 = right_rotate(a, 2) ^ right_rotate(a, 13) ^ right_rotate(a, 22)
            maj = (a & b) ^ (a & c) ^ (b & c)
            temp2 = (s0 + maj) & MOD
            
            h = g
            g = f
            f = e
            e = (d + temp1) & MOD
            d = c
            c = b
            b = a
            a = (temp1 + temp2) & MOD
    
        hash_values = [
            (old + new) & MOD 
            for old, new in zip(hash_values, (a, b, c, d, e, f, g, h))
            ]

    return b"".join(struct.pack(">I", value) for value in hash_values)

def _find_K(L: int) -> int:
    for i in count(start=1):
        if CHUNK_SIZE_2_BITS * i >= L + 1 + BIT_64:
            break
    return CHUNK_SIZE_2_BITS * i - (L + 1 + BIT_64)

def right_rotate(number: int, offset: int) -> int:
    return (
        (number >> offset) | 
        ((number << (WORD_SIZE_2_BITS - offset)) & 0xFFFFFFFF)
        )


def right_shift(number: int, offset: int) -> int:
    return number >> offset
    