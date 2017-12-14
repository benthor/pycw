#!/usr/bin/python3

import sys

with open(sys.argv[1], "rb") as f:
    byte = f.read(1)
    while byte != b"":
        if byte == b'\x89':
            text = 'B\u0305T\u0305'
        elif byte == b'\x83':
            text = 'A\u0305S\u0305'
        elif byte == b'\x1a':
            text = '[END OF MESSAGE]'
        else:
            text = byte.decode('utf-8')
        print (text, end='')
        byte = f.read(1)
f.close()
