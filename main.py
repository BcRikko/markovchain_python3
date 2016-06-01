# coding: utf-8

import sys, os

from prepare import PrepareChain
from generate import GenerateText


if __name__ == "__main__":
    mode = sys.argv[1]

    if mode == "1":
        file = open("./input.txt", encoding="utf-8")
        text = file.read()

        chain = PrepareChain(text)
        quartet_freqs = chain.make_chain_freqs()

        if os.path.exists(chain.DB_PATH):
            init = False
        else:
            init = True

        chain.save(quartet_freqs, init=init)

    elif mode == "2":
        generator = GenerateText()
        print(generator.generate())
