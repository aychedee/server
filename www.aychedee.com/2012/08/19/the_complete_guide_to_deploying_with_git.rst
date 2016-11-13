public: yes
tags: [git, deploying, devops]
summary: |
  For small or simple projects deploying with git can be a seamless process 
  which has the side benefit of encouraging proper usage of DVCS.

The complete guide to deploying with git
========================================

For simple web projects git makes an excellent deployment tool. It uses 
underlying protocols that are available on most platforms and it will even
force version control on those who are reluctant to use it. 

This guide will start with the most basic possible methods of deploying web
sites using git and then build to more complicated examples.

The simple case: Deploying a static site
----------------------------------------

The simplest site to deploy with git would be one that used html and css only. 
Just a static collection of files that you wanted to push to a remote server. 
To make this even simpler we are going to suppose that the machine you are 
creating the site on and the machine that you are deploying to are the same.

Create a repository that you can push to
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

The first step is creating a git repository that can act as a remote. These 
repos are called 'bare' repos and they are a directory with '.git' tacked on
the end. They contain all the information of a normal git repository but they
do not have the working tree files. You should not try and work in them
directly. 

Let's suppose you have a git repo called 'Gretel' in your home folder. 

To create a bare repo alongside your 'Gretel' repo you would run:

.. code-block:: bash

    $ cd ~
    $ git clone --bare ~/Gretel

This creates a directory in your home directory called 'Gretel.git'. You can 
now add that bare repo as a remote to your original repo. 

.. code-block:: bash

    $ cd ~/Gretel
    $ git remote add web-site ~/Gretel.git

Now listing the remotes give the following output. 

.. code-block:: bash

    $ git remote -v 
    web ../Gretel.git (fetch)
    web ../Gretel.git (push)

Great, we can push or pull from our new bare repo. Now if you understand what
we are doing here you will see that any of this can also be done over an ssh
connection. But we will get to that later... What we actually want to do now is
to perform an action after we push to that repo. The hook we will create is the
'post-receive' hook. It is run immediately after the repo receives a push from 
a remote. 

.. code-block:: bash

    $ vim ~/Gretel.git/hooks/post-receive

In this file we are going to place the following script

.. code-block:: bash

    #!/bin/sh
    SITE_NAME="Gretel"
    echo "Checking out repo to /var/www/$SITE_NAME"
    GIT_WORK_TREE=/var/www/$SITE_NAME git checkout -f
    echo "Restarting Apache..."
    apache2ctl restart
    echo "Site should be up!"
   
And then make it executable

.. code-block:: bash

    $ chmod a+x ~/Gretel.git/hooks/post-receive

This assumes that you have a site being served by Apache with a document root 
of '/var/www/Gretel' and that the user who did the push has the necessary 
permissions to write to that directory and restart Apache. 

The really interesting line is 

.. code-block:: bash

    GIT_WORK_TREE=/var/www/$SITE_NAME git checkout -f

It tells git to do a forced checkout, overwriting files if necessary. The 
GIT_WORK_TREE environment variable, that we set before we run the checkout,
tells git where you want this fresh checkout to be. You should set it to 
whatever location your web server is looking for files. So the same path that's
set in your Apache DocumentRoot or the equivalent for whatever web server you
may be using.

Now, whenever we have made a commit we can do a:

.. code-block:: bash

    git push web
    
And an updated copy of our web site is checked out and available to the web server.

That is essentially it. Next we will look at a more advanced case which adds
a bit more complexity but is still largely similar.

The more advanced case: Deploying a django web application
----------------------------------------------------------

Building on what we did on with a static site. We can now use git to deploy a
Python django web application which is hosted on a Linux server somewhere in
the cloud. 

Creating a git repository on a remote server  and adding it locally
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

This next example assumes that you have root access on a Linux server called 
gretel.com on which we have properly set up `passwordless ssh access <http://www.packetsource.com/article/ssh/40064/how-to-setup-password-less-ssh-using-public-private-keys>`_.

There is also a web server of some variety that is configured to look for a 
WSGI application at /srv/www.gretel.com/gretel/wsgi.py.

The application that we want to deploy is on your local machine in a git
repository in your home directory called Gretel. So: "~/Gretel".

The first step is creating the remote repository on the server. Compressing the
whole repository and copying it directly up is simplest. Then we can ssh in and
uncompress it and create a bare repo. 

.. code-block:: bash

    $ tar -C ~/ -zcvf /tmp/gretel.tgz ~/Gretel
    $ scp /tmp/gretel.tgz aychedee@www.gretel.com:/tmp/
    $ ssh aychedee@www.gretel.com
    aychedee@gretel $ tar -C /srv/ -zxf /tmp/gretel.tgz
    aychedee@gretel $ cd /srv
    aychedee@gretel $ git clone --bare /srv/gretel
    aychedee@gretel $ exit

Now we can add this remote repository to our local git repo. 
 
.. code-block:: bash

    $ git remote add live aychedee@www.gretel.com:/srv/gretel.git

The remote repository needs some kind of post-receive hook. The file 
/srv/gretel.git/hooks/post-receive on the remote server could look something 
like this:

.. code-block:: bash

    #!/bin/sh
    REPO_NAME="gretel"
    export WHERE_AMI_I=live
    echo "Checking out repo to /srv/$REPO_NAME"
    GIT_WORK_TREE=/srv/$REPO_NAME git checkout -f
    echo "Bouncing the webserver"
    services uwsgi restart
    echo "Site should be up and refreshed!"
   
The only thing that we are doing slightly differently here is adding an
environment variable that can be used by our web application to alter its 
settings. Access the live database, look for templates in a different 
directory. That kind of thing. 

Now that we have this set up whenever we do a commit and:

.. code-block:: bash

    $ git push live 

The new version of your web application will be served. Rolling back to a
previous version is as simple as doing a git reset and another push to live. 

If you have any questions or suggestions for improvements to this guide then 
please let me know at `hansel@interpretthis.org`_.

.. _hansel@interpretthis.org: hansel@interpretthis.org
