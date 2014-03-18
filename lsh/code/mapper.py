#!/usr/bin/env python

import numpy as np
import sys

hash_functions = []


def minhash(video_id, shingles):
    signature_vector = [1000000000] * 256

    for shingle in shingles:
        for i, hash in enumerate(hash_functions):
            if signature_vector[i] > hash[shingle]:
                signature_vector[i] = hash[shingle]

    # b = 15, r = 17
    # b = 10, r = 25
    for i in range(0, 10):
        key = ""
        key = key + str((100 + i))
        for j in range(0, 31 if i == 9 else 25):
            key = key + str(signature_vector[25 * i + j])
        print '%s\t%s' % (key, video_id)

if __name__ == "__main__":
    # Very important. Make sure that each machine is using the
    # same seed when generating random numbers for the hash functions.
    np.random.seed(seed=42)

    for i in range(0, 256):
        a = np.random.randint(1000)
        b = np.random.randint(1000)
        temp = []
        for j in range(0, 10001):
            temp.append((a * j + b) % 10001)

        hash_functions.append(temp)

    for line in sys.stdin:
        line = line.strip()
        video_id = int(line[6:15])
        shingles = np.fromstring(line[16:], dtype=np.int32, sep=" ")
        minhash(video_id, shingles)