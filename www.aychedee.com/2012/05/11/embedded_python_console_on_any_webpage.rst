public: yes
tags: [IPython, Python, web development]
summary: |
  Embeddable Python console for any web page. The code is simple. 

Embedding a PythonAnywhere console in any web page / blog post
==============================================================


Once you've built a web based Python console then you can pretty much stick it
any where you want. 

Anonymous `PythonAnywhere <http://www.pythonanywhere.com/>`_  consoles can now
be embedded in a blog post like this:


.. raw:: html

    <iframe
        style="width: 740px; height: 480px; border: none;"
        name="embedded_python_anywhere"
        src="https://www.pythonanywhere.com/embedded/">
    </iframe>

The code for doing this is very simple. 

.. code-block:: html

    <iframe
        style="width: 640px; height: 480px; border: none;"
        name="embedded_python_anywhere"
        src="https://www.pythonanywhere.com/embedded/">
    </iframe>

Each console session actually follows the user around based on their a 
session-id cookie. So if you want to start afresh you'll have to clear that 
cookie. Otherwise it's actually an interesting feature because all your objects
and imports still exist.

Now, wouldn't it be cool if you could also specify a block of 
code for it to run as well...

