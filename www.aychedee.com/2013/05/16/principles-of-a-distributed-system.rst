public: yes
tags: [design, fault tolerance, self healing]
summary: |
  Some ideas on designing a fault tolerant, system with complex interactions
  between the disparate parts

Principles of a distributed system
==================================

As what we are building at `PythonAnywhere <https://www.pythonanywhere.com>`_
becomes more complex the interactions between systems also start to multiply.

The dependency graph starts looking tangled and working out what components
depend on each other during the deployment process can be painful and error
prone.

So I have been thinking a lot about what a perfect, fault tolerant, distributed
system might look like.

 * Starting order should not be important
 * Services that require other services should wait gracefully
 * Services should be advertised on the network instead of having to be known
   about before hand
 * A service going away should not cause a cascading meltdown

Most of these problems are generally solved by operating your own DNS service
so that addresses for machines are not hard coded IP numbers and you can load
balance. But this is still not as elegant as the idea of having a complex
service that self assembles out of simple components. Especially if you can
also scale by just bringing up new servers that provide whichever service is
under heaviest load.

Maybe it's worthwhile `investigating using UpNP <http://pupnp.sourceforge.net/>`_
or `Zeroconf <https://help.ubuntu.com/community/HowToZeroconf>`_. Though neither
really assists with service advertisement out of the box.
