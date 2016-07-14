import pyaudio
import numpy as np
import math
from sys import stdin

WPM = 20


# duration atom, length of one dot and length of intra-character gaps in seconds
# atom = 0.05
# see https://en.wikipedia.org/wiki/Morse_code#/Speed_in_words_per_minute
atom = 1.2 / WPM


volume = 0.5     # range [0.0, 1.0]
fs = 44100       # sampling rate, Hz, must be integer
f = 800.0        # sine frequency, Hz, may be float



chars = {
    'a' : [1, 2],
    'b' : [2, 1, 1, 1],
    'c' : [2, 1, 2, 1],
    'd' : [2, 1, 1],
    'e' : [1],
    'f' : [1, 1, 2, 1],
    'g' : [2, 2, 1],
    'h' : [1, 1, 1, 1],
    'i' : [1, 1],
    'j' : [1, 2, 2, 2],
    'k' : [2, 1, 2],
    'l' : [1, 2, 1, 1],
    'm' : [2, 2],
    'n' : [2, 1],
    'o' : [2, 2, 2],
    'p' : [1, 2, 2, 1],
    'q' : [2, 2, 1, 2],
    'r' : [1, 2, 1],
    's' : [1, 1, 1],
    't' : [2],
    'u' : [1, 1, 2],
    'v' : [1, 1, 1, 2],
    'w' : [1, 2, 2],
    'x' : [2, 1, 1, 2],
    'y' : [2, 1, 2, 2],
    'z' : [2, 2, 1, 1],
    '0' : [2, 2, 2, 2, 2],
    '1' : [1, 2, 2, 2, 2],
    '2' : [1, 1, 2, 2, 2],
    '3' : [1, 1, 1, 2, 2],
    '4' : [1, 1, 1, 1, 2],
    '5' : [1, 1, 1, 1, 1],
    '6' : [2, 1, 1, 1, 1],
    '7' : [2, 2, 1, 1, 1],
    '8' : [2, 2, 2, 1, 1],
    '9' : [2, 2, 2, 2, 1],
    ' ' : [0, 0, 0, 0],
    '.' : [1, 2, 1, 2, 1, 2],
    ',' : [2, 2, 1, 1, 2, 2],
    '?' : [1, 1, 2, 2, 1, 1],
    '!' : [2, 1, 2, 1, 2, 2],
}




# sigmodial smoothing function. factor determines steepness, cutoff is sig(t) value beyond which smoothing will cease, offset moves curve along t axis
def sigsmooth(samples, factor=0.05, cutoff=0.95, offset=5):
    tmp = 0
    l = len(samples)
    for i in range(l):
        sig = 1 / (1+math.pow(math.e, -(i*factor)+offset))
        samples[i] *= sig
        if sig >= cutoff:
            tmp = i
            break
    for i in range(tmp, l):
        sig = 1 / (1+math.pow(math.e, ((-l+i)*factor)+offset))
        samples[i] *= sig
    return samples


def char2sample(char):
    tau = math.pi * 2
    stepsize = tau * f / fs # how many samples for one full sine wave at frequency f
    samples = []
    for press in chars[char]:
        if press == 1:
            samples = np.append(samples, sigsmooth([math.sin(x*stepsize) for x in range(int(fs*atom))]))
        elif press == 2:
            samples = np.append(samples, sigsmooth([math.sin(x*stepsize) for x in range(int(fs*atom*3))]))
        else:
            samples = np.append(samples, [0 for x in range(int(fs*atom))])
        samples = np.append(samples, [0 for x in range(int(fs*atom))])
    samples = np.append(samples, [0 for x in range(int(fs*atom*3))])
    return samples.astype(np.float32)


p = pyaudio.PyAudio()

# for paFloat32 sample values must be in range [-1.0, 1.0]
stream = p.open(format=pyaudio.paFloat32,
                channels=1,
                rate=fs,
                output=True)


line = stdin.readline()
while line:
    for char in line:
        char = char.lower()
        if char in chars.keys():
            samples = char2sample(char)
            stream.write(volume*samples, len(samples))
            print(char, end='', flush=True)
        else:
            stream.write(volume*char2sample(' '))
            print("_", end='', flush=True)
    line = stdin.readline()
    # short break
    stream.write(volume*char2sample(' '))
    # print newline
    print()

# HACK: prevent early closing of stream
stream.write(volume*char2sample(' '))
stream.write(volume*char2sample(' '))
    

stream.stop_stream()
stream.close()

p.terminate()
