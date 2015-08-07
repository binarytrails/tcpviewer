# TCP Viewer

We wrap *tcpflow* in the backend to arrange data for dynamic visualisation for the frontend.

Our goal is to raise awareness about the quantity of personal information available to everyone connected to a network. We accomplish this using a fun and interactive image board.

The majority of people don't understand the network traffic. Knowing the OSI model and protocols by heart can be painful. We believe that our tool will bring more people into networking by making visualization accessible and fun.

The code base was written during HackPrinceton 2015.

## Setup

Install the system dependecies from *sys_dependencies.txt* and the python ones with:

    pip install -r requirements.txt --user

### Tcpflow

In order to capture the network traffic as a normal user, you need to allow *tcpflow* to capture raw packets and give it the permissions to manipulate the network interfaces. Of course, we need a group dedicated for this purpose to limit this capability to only a certain group of users.

    su
    groupadd pcap
    usermod -a -G pcap user
    chgrp pcap /usr/bin/tcpflow
    chmod 750 /usr/bin/tcpflow
    setcap cap_net_raw,cap_net_admin=eip /usr/bin/tcpflow
    exit

*Inspired from tcpdump Peter Nixon [article](http://peternixon.net/news/2012/01/28/configure-tcpdump-work-non-root-user-opensuse-using-file-system-capabilities/) and tested on Debian Jessie.*

### Launching

Go into *src/* and choose between running with an available *nodejs* frontend:

    ./run.py -vi wlan0 -f nodejs -a 127.0.0.1:8000

or without a frontend by using only an output directory:

    ./run.py -vi wlan0 -h output/

it might be a good idea to add an exclude IPs option with your server address to avoid capturing your own captured files accessed by one of your frontend clients using unencrypted HTTP requests. You can write one or many IPs.

    ./run.py -vi wlan0 -f nodejs -a 0.0.0.0:8000 -e 192.168.2.10 10.0.0.1

for more options:

    ./run.py --help

**You have to be aware that due to the *tcpflow* latency, it takes around 40 seconds between the time someone sees the image over the unencrypted HTTP traffic and the time it is extracted by *tcpflow*. The positive side to this issue is that the *tcpflow* has always a perfect image reconstruction that was lacking with the other network interceptor tools.**

