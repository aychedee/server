public: yes
tags: [iPad, Apple, cloud, PythonAnywhere]
summary: |
  After a bit of hard work we have working browser based consoles for 
  the iPad. A handy server admin solution

Browser based consoles for the iPad
===================================

The last three weeks has been fun. What looked like a painful task has turned
into something that I am very happy with and am glad to have helped make work. 

`PythonAnywhere <http://www.pythonanywhere.com/>`_ now supports the iPad with 
a browser based console. I think the interface looks good, some might even say
pretty:

.. image:: /static/pythonanywhere-ipad-console.png
   :height: 1024
   :width: 768
   :scale: 100
   :alt: PythonAnywhere bash console on an ipad

We decided to add an extra row of keys. After all, using vim or bash without
Esc or Ctrl respectively can be somewhat difficult. 

`There are some excellent existing resources <http://xaviesteve.com/2899/ipad-iphone-mobile-html-css-template-for-web-apps/>`_
with information about how to style elements so they fit into the iOS look and
feel so that part wasn't too hard. It would be very nice if the developer was
able to tell the iPad keyboard to pop out but I guess that would be asking too
much.

It is very useful having a persistent Bash or IPython console in a Safari
tab. Especially useful for server administration. 

The connection to the console server is done over a websocket. The downside to
this is that because the technology is fairly recent most proxy servers still
don't know how to deal with it and end up mangling the Origin header and 
breaking the connection. A possible fix for this is moving to secure websockets
because proxy servers are can't really mess up encrypted traffic as long as it 
it going over a standard port. But in the medium to long term this might not 
even be necessary.

This is an example of what the standard console listing looks like:

.. image:: /static/pythonanywhere-console-nav.png
   :height: 642
   :width: 768
   :scale: 100
   :alt: PythonAnywhere console listing

I typically keep an ssh connection open to any of the servers I am using and a 
couple of Python consoles that act as scratch spaces for figuring out library
APIs or other more extended calculations.  

Using the internet on an iPad still makes me feels a bit dirty, but 
as a secondary device I could see it eventually being a handy thing and I
think anything we, the web developer community, can do to make them more useful
is definitely worth the effort. 

One thing I will say about working on the iPad, it give you an
appreciation for pixel perfect design. It gives you a strong incentive to make
everything look just right when the surrounding frame is so well thought out.

