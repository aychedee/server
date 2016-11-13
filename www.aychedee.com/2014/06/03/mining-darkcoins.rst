public: yes
tags: [linux, cryptocurrency]
summary: |
  Howto setup your ubuntu machine as a darkcoin cpu miner, using upstart to
  start and stop it.

Howto setup your ubuntu machine for cpu mining darkcoins
========================================================

Darkcoin is the newest cryptocurrency that I consider different enough to be
interesting. It uses `a novel method of splitting up and pooling transactions <https://www.darkcoin.io/intro.html>`_
that they call DarkSend (Ooooh!). Which functions in a very similar manner to
the `mixing services <https://en.bitcoin.it/wiki/Mixing_service>`_ that are
available for Bitcoin. However being built into the currency guarantees they
are widely used and would make tracing the path of a given chunk of value
through the block chain tricky. The `Darkcoin white paper from March 2014 <https://www.darkcoin.io/downloads/DarkcoinWhitepaper.pdf>`_
isn't *that* difficult to grok if you want to know all the details.

Below is a guide to setting up an Ubuntu/Debian machine as a Darkcoin CPU miner.


Step 1: Install dependencies
----------------------------

.. code-block:: bash

    sudo apt-get update
    sudo apt-get install -y git make automake libcurl4-nss-dev

Step 2: Clone and build the miner
---------------------------------

.. code-block:: bash

    git clone https://github.com/elmad/darkcoin-cpuminer-1.3-avx-aes.git drkminer
    cd drkminer && ./autogen.sh && ./configure CFLAGS="-O3" && make

That will take awhile to complete on a slower machine. Go make a cup of tea.

Step 3: Copy the miner onto your path
-------------------------------------

.. code-block:: bash

    sudo cp primeminer /usr/local/bin

Step 4: Create an upstart job
-----------------------------

.. code-block:: bash

Create a text file at /etc/init/primeminer.conf. Add the following text to it
and then save it.

.. code-block:: bash

    ## Primecoin miner
    #

    description "Primecoin Miner"

    start on runlevel [2345]
    stop on runlevel [!2345]

    expect fork
    respawn

    exec /usr/local/bin/primeminer -pooluser=XXXXXXXX -poolip=176.34.128.129 -poolport=1337 -genproclimit=1 -poolpassword=PASSWORD &> /dev/null

You will need to replace the 'XXXXXXXX' with your own XPM deposit address. You
can generate one of these by installing the `primecoin client <http://sourceforge.net/projects/primecoin/files/>`_,
running it, and looking under the 'Receive' tab. The address is the long weird
looking combination of letters and numbers in the right hand column.
Alternatively you can sign up for a BTC-e account and use the XPM deposit
address they generate for you.

Your poolip is also meant to be region specific. So you pick it from these
options:

::

  EU: 176.34.128.129
  US: 54.200.248.75
  ASIA: 54.251.179.44

poolpassword=PASSWORD is correct. There is no password. Or the password is
public at the moment.


Step 5: Start the miner and follow the log file to watch it work
----------------------------------------------------------------

.. code-block:: bash

    sudo service primeminer start
    sudo tail -f /var/log/upstart/primeminer.log

Stopping and restarting the miner can be done with:

.. code-block:: bash

    sudo service primeminer restart
    sudo service primeminer stop

The miner will automatically start every time you reboot your machine.


Wrap up
-------

Well I hope that helps some people get started. Obviously this relies on you
using some form of Linux. But then you should be doing that anyway.
