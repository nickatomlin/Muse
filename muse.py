#!/usr/bin/python

import subprocess
import sys

len_1 = {0: 'e', 1: 't'}
len_2 = {1: 'a', 0: 'i', 3: 'm', 2: 'n'}
len_3 = {4: 'd', 6: 'g', 5: 'k', 7: 'o', 2: 'r', 0: 's', 1: 'u', 3: 'w'}
len_4 = {8: 'b', 10: 'c', 2: 'f', 0: 'h', 7: 'j', 4: 'l', 6: 'p', 13: 'q', 1: 'v', 9: 'x', 11: 'y', 12: 'z', 15: ' '}
# takes in a binary string (sequence) and displays the corresponding letter
# 0=dot, 1=dash
# 1111=space
def display_letter(sequence):
    length = len(sequence)
    value = int(sequence, 2)

    if length == 1:
        print(len_1[value])
    elif length == 2:
        print(len_2[value])
    elif length == 3:
        print(len_3[value])
    elif length == 4:
        print(len_4[value])
    else:
        print(sequence, "could not be recognized as a character.")

def interpret_eeg(timestamp, datapoint):
    # TODO interpret data
    print(timestamp, " -> ", datapoint)

# muse_player = path to muse player
def main(muse_player):
    try:
        process = subprocess.Popen([muse_player, "-l", "5000"], stdout=subprocess.PIPE)
        for line in process.stdout:
            line = line.decode("utf-8")
            if "/muse/eeg " in line:
                split = line.split()
                timestamp = float(split[0]) # unix timestamp in UTC
                eeg = split[3:7] # eeg data (organized into tracks)
                for i in range(0, len(eeg)):
                    eeg[i] = float(eeg[i])
                # only interpret track 0
                interpret_eeg(timestamp, eeg[0])
    except subprocess.CalledProcessError as e:
        print("Stdout output:\n", e.output)

if __name__ == "__main__":
    if (len(sys.argv) < 2):
        print("Usage: muse.py path-to-muse-player")
    else:
        main(sys.argv[1])
