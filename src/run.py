#!/usr/bin/python2.7

"""TcpViewer.

Usage:
    tcpviewer.py [-v] (-i) <interface> [-c] ((-a) <address> (-f) <frontend> | (-h) <directory>)

Opitons:
    -v, --verbose       Show relevant print's during program execution.
    -i, --interface     Listen on the network interface.
    -c, --clean         Clean output directory.
    -f, --frontend      Use one of the frontends from (nodejs,).
    -a, --address       Host the frontend on this ip:port.
    -h, --headless      Without a frontend with an output directory.
"""

import re
from docopt import docopt
from TcpViewer import TcpViewer

if __name__ == '__main__':
    args = docopt(__doc__, version='TcpViewer 0.1')

    if args["<frontend>"] not in ["nodejs"]:
        print "The " + args["<frontend>"] + " frontend is not availabe. See --help."
     
    ip_port_v4_regex = re.compile('[0-9]+(?:\.[0-9]+){3}:[0-9]+')
    if not re.findall(ip_port_v4_regex, args["<address>"]):
        raise ValueError("The %s is not in the ip:port v4 format." % args["<address>"])

    TcpViewer(args["<interface>"], args["<frontend>"], args["<address>"],
        args["<directory>"], args["--clean"], args["--verbose"])

