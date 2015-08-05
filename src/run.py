#!/usr/bin/python2.7

'''TcpViewer.

Usage:
    tcpviewer.py [-v] (-i) <interface> [-e <ip> -c] ((-h) <directory> | (-f) <frontend> (-a) <address>)

Opitons:
    -v, --verbose       Show relevant output during the program execution.
    -i, --interface     Listen on the network interface.
    -e, --exclude       Exclude this IP from source and destination in capture.
    -c, --clean         Clean the output directory.
    -h, --headless      Run without a frontend using an output directory.
    -f, --frontend      Use one of the frontends from the following: (nodejs,).
    -a, --address       Host the frontend on this ip:port.
'''

import sys, re
from docopt import docopt

from Utilities import *
from TcpViewer import TcpViewer

if __name__ == '__main__':
    args = docopt(__doc__, version='TcpViewer 0.1')

    if args['<frontend>'] and args['<frontend>'] not in ['nodejs']:
        sys.exit('The ' + args['<frontend>'] + ' frontend is not availabe. See --help.')

    for ip in [args['<ip>']]:
        if not re.findall(ipv4_regex(), ip):
            raise ValueError('The %s is not in the ipv4 format.' % ip)

    if args['<address>'] and not re.findall(ipv4_port_regex(), args['<address>']):
        raise ValueError('The %s is not in the ipv4:port format.' % args['<address>'])

    TcpViewer(args['--verbose'], args['<interface>'], args['<ip>'], args['--clean'],
        args['<directory>'], args['<frontend>'], args['<address>'])

