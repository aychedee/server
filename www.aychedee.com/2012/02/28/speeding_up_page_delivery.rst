public: yes
tags: []
summary: |
  A minor change to the way your servers send their initial content
  can make a big difference in latency.

Speeding up page delivery with initial recieve window (initrwnd)
================================================================

A simple tip for reducing latency is increasing the number of packets that your
webserver sends after the initial request. For small static sites this can 
really decrease your latency. Even works well for largeer sites. Google uses it
so you might as well. 

Who doesn't want to seem faster?

On any Linux server with a kernel later than 2.6.32 these are the steps. From a 
bash console:

.. code-block:: bash

    aychedee.com:~$ ip route show

This gives you the currently configured routes. Look for the one called
default. It should look something like this:

.. code-block:: bash

    default via 10.10.10.10 dev eth0  metric 100

You are going to copy it exactly and add an extra element at the end like this:

.. code-block:: bash

    aychedee.com:~$ sudo ip route change default via 10.10.10.10 dev eth0  metric 100 initcwnd 12 initrwnd 12

What this means is that your server defaults to sending up to 12 packets of data when an IP 
request is made of it. The default is 3 on older kernels and 10 since 3.0.0. 
The size of these packets depends on the `maximum segment size (MSS) <http://en.wikipedia.org/wiki/Maximum_segment_size>`_

These settings will not survive a reboot so you will have to put them into a
boot script if you want them to persist. 

