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
    print(sequence)
    length = len(sequence)
    value = int(sequence, 2)

    try:
        if length == 1:
            sys.stdout.write(len_1[value])
        elif length == 2:
            sys.stdout.write(len_2[value])
        elif length == 3:
            sys.stdout.write(len_3[value])
        elif length == 4:
            sys.stdout.write(len_4[value])
        else:
            #print(sequence, "could not be recognized as a character.")
            sys.stdout.write("*")
    except KeyError as e:
        sys.stdout.write("*")
    sys.stdout.flush()


tick = 0.2  # length of 1 unit of morse code time
letter = "" # string of 0 for dot, 1 for dash
recent = 2  # most recent action

def process_letter():
    global letter
    if len(letter) > 0:
        display_letter(letter)
        letter = ""

def process(action, time): # 0 for close, 1 for open, 2 for timeout, 3 for very first call
    global tick
    global letter
    global recent
    print("process", action, time)

    if action == 3:
        recent = 0;
        return;

    if action == 0:
        if recent == 0:
            letter += '0'
        if time > 2 * tick:
            process_letter();
        if time > 5 * tick:
            display_letter("1111")
    elif action == 1:
        if time > 2 * tick:
            letter += '1'
        if time <= 2 * tick:
            letter += '0'
    elif action == 2:
        if recent == 0:
            letter += '0'
            process_letter();
    recent = action;

last_event = -2
last_time = 0.0
#timeout_sent = False
def interpret_eeg(timestamp, datapoint):
    global last_event
    global last_time
    #global timeout_sent

    event = -1
    if datapoint < 700:
        event = 0
    elif datapoint > 1000:
        event = 1
    else:
        # no blink (normal)
        event = 4
        '''
        if last_event >= 0 and timestamp - last_time > tick * 5:
            # timeout, send last event
            #print("TIMEOUT")
            process(2, timestamp)
            last_event = -1
        return
        '''
        '''
        if last_event >= 0 and timestamp - last_time > tick * 5 and not timeout_sent:
            # timeout, send last event
            print("TIMEOUT")
            process(2, 0)
        '''

    #print(timestamp, "->", event)
    #print("last", last_event)
    #print("event", event)
    if last_event < -1:
        process(3, 0)
        last_event = event
        last_time = timestamp
    elif event != last_event:
        #print("not equal")
        if last_event >= 0 and last_event != 4:
            #print("timestamp", timestamp)
            #print("last_time", last_time)
            #print("diff", timestamp - last_time)
            process(last_event, timestamp - last_time)
            last_time = timestamp
            #timeout_sent = False

        last_event = event

last_timestamp = 0
items = []
def smooth(timestamp, datapoint):
    global last_timestamp
    global items

    if timestamp == last_timestamp:
        items.append(datapoint)
    else:
        if len(items) > 0:
            average = sum(items) / len(items)
            interpret_eeg(timestamp, average)

        last_timestamp = timestamp
        items = [datapoint]

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
                smooth(timestamp, eeg[0])
    except subprocess.CalledProcessError as e:
        print("Stdout output:\n", e.output)

if __name__ == "__main__":
    if (len(sys.argv) < 2):
        print("Usage: muse.py path-to-muse-player")
    else:
        main(sys.argv[1])
