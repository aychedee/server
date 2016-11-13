public: yes
tags: [linux, learning, utilities, cli-usage-examples]
summary: |
  nmap is a very powerful network scanning tool that is useful for discovering
  and debugging servers.

How do I use nmap to...
=======================

As I slowly `read my way through the Unix man pages <http://www.aychedee.com/2013/07/10/man-man/>`_
I am reminded just how god damn cryptic they can actually be. As a user of Linux
you often find yourself googling for simple usage examples for common CLI
utilities. So today I'm going to provide that for nmap.

How do I use nmap to find all machines on a network
---------------------------------------------------

.. code-block:: bash

    :~$ nmap -Pn -p 5900 192.168.0.0/24 | grep -B 4 open


How do I use nmap to find all machines running VNC (or any service) on a network
--------------------------------------------------------------------------------

I have to do this at work sometimes when I have forgotten the IP addresses of
certain servers. It scans every IP on the network and reports whether the port
on each IP is open or filtered / closed. Our grep filters that list to only
show machines with the port actually open.

.. code-block:: bash

    :~$ nmap -Pn -p 5900 192.168.0.0/24 | grep -B 4 open

Changing the `-p` option lets you alter the target port. so `-p 80` will find
all HTTP servers. `-p 22` finds all the SSH servers.

Using a `-Pn` scan (which ignores ping responses and just tries each port)
takes a *really* long time if you don't limit the port range. By default nmap
scans the port range 1 - 65535. So even on a class C network with only 256
possible IP addresses it will scan 16,776,960 ports. That takes over 4 hours on
my work network.
