from sys import argv
from random import choice

GROUPSIZE=5
GROUPS=10


for i in range(GROUPS):
    for j in range(GROUPSIZE):
        print(choice(argv[1]), end='', flush=True)
    print()
