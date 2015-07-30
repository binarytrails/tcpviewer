# TCP Viewer

We wrap tcpflow in the backend to arrange data for dynamic visualisation for the frontend.

Our goal is to raise awareness about the quantity of personal information available to everyone connected to a network. We accomplish this using a fun and interactive image board.

The majority of people don't understand the network traffic. Knowing the OSI model and protocols by heart can be painful. We believe that our tool will bring more people into networking by making visualization accessible and fun.

The code base was written during HackPrinceton 2015.

## Tcpflow

In order to capture the network traffic as a normal user, you need to allow *tcpflow* to capture raw packets and give it the permissions to manipulate the network interfaces. Of course, we need a group dedicated for this purpose to limit this capability to only a certain group of users.

    su
    groupadd pcap
    usermod -a -G pcap user
    chgrp pcap /usr/bin/tcpflow
    chmod 750 /usr/bin/tcpflow
    setcap cap_net_raw,cap_net_admin=eip /usr/bin/tcpflow
    exit

*Inspired from tcpdump Peter Nixon [article](http://peternixon.net/news/2012/01/28/configure-tcpdump-work-non-root-user-opensuse-using-file-system-capabilities/) and tested on Debian Jessie.*

