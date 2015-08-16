#!/usr/bin/python2.7

'''TcpViewer.

Usage:
    tcpviewer.py [-v] (-i) <interface> [-c] ((-h) <directory> | (-f) <frontend> (-a) <address> [-e <ips> ...])

Opitons:
    -v, --verbose       Show relevant output during the program execution.
    -i, --interface     Listen on the network interface.
    -c, --clean         Clean the output directory.
    -h, --headless      Run without a frontend using an output directory.
    -f, --frontend      Use one of the frontends from the following: (nodejs,).
    -a, --address       Host the frontend on this ip:port.
    -e, --exclude       Exclude this IP's from source and destination in capture.
'''

import sys
from docopt import docopt

from Utilities import *
from TcpViewer import TcpViewer

FRONTENDS = ['nodejs']

if __name__ == '__main__':
    args = docopt(__doc__, version='TcpViewer 0.1')

    if args['<frontend>'] and args['<frontend>'] not in FRONTENDS:
        sys.exit('The ' + args['<frontend>'] + ' frontend is not available. See --help.')

    try:
        if args['<address>']: validate_ipv4_colon_port(args['<address>'])
        if args['<ips>']: validate_ipv4s(args['<ips>'])
    except ValueError as e:
        sys.exit(e)

    TcpViewer(args['--verbose'], args['<interface>'], args['<ips>'], args['--clean'],
        args['<directory>'], args['<frontend>'], args['<address>'])

