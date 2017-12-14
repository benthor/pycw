# pycw

Reads characters from stdin, synthesizes morse (cw) audio for each legal character using pyaudio before echoing it back out.


## Idea

I've long wanted to investigate if I can train my subconscious to understand morse signals by constantly exposing myself to the strongly correlated stimuli of the heard signal and the observed printed character. Someone should write a twitter or irc client with this feature.

## Usage

```
cw.py <volume in range [0.0, 1.0]> <sample frequency in Hz> <tone frequency in Hz> <words per minute>
```

This gives you a half-volume, 44000 Hz sampled tone of 800 Hz at 20 WPM:

```
echo "This is a test" | python3 cw.py 0.5 44000 800 20
```

or

```
cat code_group1.txt | python3 cw.py 0.5 44000 800 20
```

You can also use the dumb included helper script "groups.py" to generate random code groups from the characters found in the first argument for group training. Defaults to 10 groups of 5 characters each.

```
python3 groups.py "ukm" | python3 cw.py 0.5 44000 800 20
```

Sample output:

```
kkkuu
ukmkm
kukuk
umuku
ummkm
kmkuu
kmkmu
kukku
mkuuu
kmmmm
```
## Requirements

* python (only tested with python3.5)
* pyaudio (tested with 0.2.9)
* numpy (tested with 1.11.0)

## Issues/ToDos

* clean up & document the code (somewhat fixed)
* command line flags for WPM configuration missing (somewhat fixed)
* letter/word spacing currently hardcoded
* sometimes audio stream terminates early. code includes dirty hacks to try and prevent this

## Internals

* native sine signal synthesis (no fucking wav files like every other tool out there, ugh)
* logistic sigmoid function for edge smoothing
* treats newlines as whitespace (acoustically)
* prints "_" for non-translatable characters, treats as whitespace

## Fork me!