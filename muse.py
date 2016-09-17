import subprocess

def main():
    try:
        print subprocess.check_output(["echo", "hello"])
    except subprocess.CalledProcessError, e:
        print "Stdout output:\n", e.output

if __name__ == "__main__":
    main()
