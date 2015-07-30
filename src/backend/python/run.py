#!/usr/bin/python2.7

"""Tcpflow Visualiser.

Usage:
    tcp_visualiser.py [-v] (-i) <interface> [-c] (-o) <directory>

Opitons:
    -v, --verbose       Show relevant print's during program execution.
    -i, --interface     Listen on the network interface.
    -c, --clean         Clean output directory.
    -o, --output        Output directory.
"""

from docopt import docopt
from Main import Main

if __name__ == '__main__':
    args = docopt(__doc__, version='Tcpflow Visualiser 0.1')
    Main(args["<interface>"], args["<directory>"], args["--clean"], args["--verbose"])

