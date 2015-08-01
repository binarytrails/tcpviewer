#!/usr/bin/python2.7

'''TcpViewer.

Usage:
    tcpviewer.py [-v] (-i) <interface> [-c] ((-h) <directory> | (-f) <frontend> (-a) <address>)

Opitons:
    -v, --verbose       Show relevant output during the program execution.
    -i, --interface     Listen on the network interface.
    -c, --clean         Clean the output directory.
    -h, --headless      Run without a frontend using an output directory.
    -f, --frontend      Use one of the frontends from the following: (nodejs,).
    -a, --address       Host the frontend on this ip:port.
'''

import sys, re
from docopt import docopt
from TcpViewer import TcpViewer

if __name__ == '__main__':
    args = docopt(__doc__, version='TcpViewer 0.1')

    if args['<frontend>'] and args['<frontend>'] not in ['nodejs']:
        sys.exit('The ' + args['<frontend>'] + ' frontend is not availabe. See --help.')

    ip_port_v4_regex = re.compile('[0-9]+(?:\.[0-9]+){3}:[0-9]+')
    if args['<address>'] and not re.findall(ip_port_v4_regex, args['<address>']):
        raise ValueError('The %s is not in the ip:port v4 format.' % args['<address>'])

    TcpViewer(args['<interface>'], args['<frontend>'], args['<address>'],
        args['<directory>'], args['--clean'], args['--verbose'])

