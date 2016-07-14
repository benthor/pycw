# pycw

Reads characters from stdin, generates morse (cw) audio for each legal character using pyaudio before echoing it back out.

**NOTE: I haven't triple-checked the character to code mapping. It _feels_ correct, but no guarantees.**


## Idea

I've long wanted to investigate if I can train my subconscious to understand morse signals by constantly exposing myself to the strongly correlated stimuli of the heard signal and the observed printed character. Someone should write a twitter or irc client with this feature.

## Usage

```
echo "This is a test" | python3 cw.py
```

or

```
cat code_group1.txt | python3 cw.py
```

You can also use the dumb included helper script "groups.py" to generate random code groups from the characters found in the first argument for group training. Defaults to 10 groups of 5 characters each.

```
python3 groups.py "ukm" | python3 cw.py
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

* clean up the code
* command line flags for WPM configuration missing (for now, edit the top of the file)
* letter/word spacing currently hardcoded
* sometimes audio stream terminates early. code includes dirty hacks to try and prevent this

## Internals

* native sine signal generation (no fucking wav files like every other tool out there, ugh)
* logistic sigmoid function for edge smoothing
* treats newlines as whitespace (acoustically)
* prints "_" for non-translatable characters, treats as whitespace

## Fork me!