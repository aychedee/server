public: no
tags: [iOS, iPad, iPhone, web development]
summary: |
  There are basic steps that you can take to make your website more friendly 
  on iOS devices. Debugging is tricky but there are some simple tricks that 
  make it easier. 
  If you ever want to verify users passwords against this hash in a non
  standard way, like from a web app for example, then you need to understand
  how it works.

Simple steps to support iOS devices (iPads and iPhones) on the web
==================================================================


Detecting iOS devices and serving them different templates or css
-----------------------------------------------------------------

The easiest way to do this is to look for 'iPhone' or 'iPad' in the browser's
user agent string. 

Turning off auto correct and auto capitalisation
------------------------------------------------

Logging into a website is frustrating when your username gets capitalised and 
autocorrected to some random word. Any text area on the site that expects non
dictionary entries should have these two settings applied to it.

.. code-block:: html

    <input type="text" autocorrect="off" autocapitalize="off"></input>

You don't need to bother with this setting for input fields with type 
'password' because these already have sensible defaults applied. 


Serve a sensibly sized page
---------------------------

Safari on iOS always determines the viewport size based on portrait 
orientation. When you rotate the device it scales up the whole site.
2. A randomly generated `salt to safeguard against rainbow table attacks <http://www.codinghorror.com/blog/2007/09/rainbow-hash-cracking.html>`_

