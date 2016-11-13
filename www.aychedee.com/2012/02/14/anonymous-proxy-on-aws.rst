public: yes
tags: [AWS, digital freedom, civil rights]
summary: |
  Configuring an anon proxy server is easy and a pretty cool way to help
  people around the world deal with government censorship.

Configuring an anonymous proxy server on aws with Ubuntu 12.04 and Squid3
=========================================================================

*Updated for Ubuntu 12.10 on the 04/11/2012*

My little sister is travelling around Vietnam at the moment and was
annoyed to find Facebook blocked and mentioned it to me over Skype. I knew it
was pretty easy to circumvent these geographic restrictions using a proxy so I
told her I would sort something out in a couple of hours. Well it took a bit
longer than that but the actual instructions are pretty simple.

Quick summary:

    1. Install squid3 and apache2-utils
    2. Change /etc/squid/squid.conf
    3. Create users and passwords
    4. Open firewall if necessary

So first off you'll need to install squid3 and apache2-utils.

.. code-block:: bash

    apt-get install squid3, apache2-utils

once you have installed squid3 the next part is modifying the config
file. Mine looks like this:

.. code-block:: squidconf

    # Squid proxy server settings

    http_port 3128
    visible_hostname squidworth
    auth_param basic program /usr/lib/squid3/ncsa_auth /etc/squid3/passwd

    refresh_pattern ^ftp:           1440    20%     10080
    refresh_pattern ^gopher:        1440    0%      1440
    refresh_pattern -i (/cgi-bin/|\?) 0     0%      0
    refresh_pattern .               0       20%     4320

    acl manager url_regex -i ^cache_object:// +i ^https?://[^/]+/squid-internal-mgr/

    acl localhost src 127.0.0.1/32 ::1
    acl to_localhost dst 127.0.0.0/8 0.0.0.0/32 ::1

    acl localnet src 10.0.0.0/8     # RFC 1918 possible internal network
    acl localnet src 172.16.0.0/12  # RFC 1918 possible internal network
    acl localnet src 192.168.0.0/16 # RFC 1918 possible internal network
    acl localnet src fc00::/7       # RFC 4193 local private network range
    acl localnet src fe80::/10      # RFC 4291 link-local (directly plugged) machines

    acl wwwusers src all
    acl ncsa_auth proxy_auth REQUIRED

    acl SSL_ports port 443
    acl Safe_ports port 80          # http
    acl Safe_ports port 21          # ftp
    acl Safe_ports port 443         # https
    acl Safe_ports port 70          # gopher
    acl Safe_ports port 210         # wais
    acl Safe_ports port 1025-65535  # unregistered ports
    acl Safe_ports port 280         # http-mgmt
    acl Safe_ports port 488         # gss-http
    acl Safe_ports port 591         # filemaker
    acl Safe_ports port 777         # multiling http
    acl CONNECT method CONNECT

    http_access allow manager localhost
    http_access allow ncsa_auth
    http_access deny !Safe_ports
    http_access deny CONNECT !SSL_ports
    http_access deny to_localhost
    http_access allow localhost

    http_access deny all

    follow_x_forwarded_for deny all
    forwarded_for off


One of the most important bits is making sure that you have
'forwarded_for off'. That means that the proxy will be anonymizing
connections and not letting the other server know who made the request.

If the configuration is not working for you try increasing the verbosity of the
logging by putting

    debug_options ALL,5

At the end of your squid.conf.

The final step is creating a user and password. Or users and passwords.
We are using super simple basic authentication in this example but there are
lots of other backends that you could use instead of ncsa_auth.

To create a user/pass combination run this command:

.. code-block:: bash

     htpasswd /etc/squid3/passwd squid_user

This will prompt you to set a password. Make as many users as you need.
htpasswd is provided by the apache2-utils package in case you were wondering
why we installed it up front.

If you are running this on AWS like I am you will then need to allow incoming
traffic on port 3128 to your server. So add it as an inbound TCP rule to the
security group.

Then restart squid and try and set up your browser to point to your new proxy
server using the port you specified. Default is 3128. When you visit a website
now your reported IP address should be that of your AWS server. Also handy for
watching `The Daily Show <http://www.thedailyshow.com/>`_ in the UK.
