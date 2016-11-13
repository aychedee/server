public: yes
tags: [AWS, Cloud, Python]
summary: |
  Creating your own personal cloud service with an Amazon micro instance is now
  ridiculously cheap. Especially compared to buying individual parts from
  service providers.

Cheapest personal cloud
=======================

Amazon prices products aggressively. They have used it to dominate the online
sales arena and the continuous price drops they have been making on their
cloud computing product makes for some very cheap virtual servers.

Consider the cheapest option available. A Linux based Micro Instance. Reserved
for 3 years with the Heavy Utilization profile [1]_.

Annual rate: $43.80 = $0.005 x 24 x 364
Upfront cost: $33.33 = $100 / 3 years

Annually that is $77.13, or $6.43 monthly.

These are weird machines though. They are deliberately crippled by Amazon and
are intended for applications that burst for very short periods (less than 10
seconds) and otherwise stay below 20% cpu utilization. If they exceed these
limits they get throttled to 10% of max CPU.

This does not stop them from being excellent personal cloud servers.

I use one for,

 * Serving this site. Feel free to try and DOS it. It is just static files
   behind a memcache server so the CPU is never used.
 * A VPN for my phone and laptop.
 * 1 flask and 2 django sites. Served using uWSGI/NGINX. Also using memcached
   so very light on the CPU.
 * ~15 git repositories.
 * A proxy server for working around geographic internet restrictions, and
   government censorship of the internet.
 * Light, intermittment, data processing for clients.

I do have an entirely separate instance running my postgres server. It wasn't
entirely necessary but since it contains client's data it seemed conceptually
simpler to divide them.

The creation of these machines should be scripted. They should be considered
the disposable product of a script. Refresh them once a week so that you know
that your machine creation script is always fresh and ready to go. Bit rot can
set in pretty quickly if you make small modifications like that all the time.

It takes a certain discipline to always replicate any change you make on the
remote machine into the script but it is well worth it in the long run.

In the interest of sharing I'm putting the abstractable portions of my
machine creation scripts up on github in a package called `kubrick <https://github.com/aychedee/kubrick>`_.

So $6.50 a month for a bundle of services that would cost upwards of $50? $100?
if bought from the individual companies that have sprung up to provide them.
Right now it seems that Amazon Web Services is providing the cheapest personal
cloud platform out there.

.. [1] The light / medium / heavy utilization thing confuses people. It has
   nothing to do with machine resource (CPU, memory IOPS) usage. Heavy utilization
   is the cheapest option if you plan on running the server constantly.

