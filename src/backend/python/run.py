#!/usr/bin/python2.7

"""TcpViewer.

Usage:
    tcpviewer.py [-v] (-i) <interface> [-c] (-o) <directory>

Opitons:
    -v, --verbose       Show relevant print's during program execution.
    -i, --interface     Listen on the network interface.
    -c, --clean         Clean output directory.
    -o, --output        Output directory.
"""

from docopt import docopt
from TcpViewer import TcpViewer

if __name__ == '__main__':
    args = docopt(__doc__, version='TcpViewer 0.1')
    TcpViewer(args["<interface>"],
        args["<directory>"],
        args["--clean"],
        args["--verbose"]
    )

