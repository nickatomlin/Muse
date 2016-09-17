import subprocess

# takes in a binary string (sequence) and displays the corresponding letter
def display_letter(sequence):
    # TODO convert sequence to morse code letter
    print(sequence)

def main():
    try:
        # TODO make sure reference to muse-player works
        process = subprocess.Popen(["muse-player", "-l", "5000"], stdout=subprocess.PIPE)
        for line in process.stdout:
            if "/muse/eeg " in line:
                # TODO interpret line
                print(line)
    except subprocess.CalledProcessError as e:
        print("Stdout output:\n", e.output)

if __name__ == "__main__":
    main()
