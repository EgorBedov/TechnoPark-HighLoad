import sys, getopt

from server import MainServer
from files import Files


def main():
    if len(sys.argv) > 1:
        Files.read_config(sys.argv[1])

    s = MainServer()
    s.run()


if __name__ == '__main__':
    main()
