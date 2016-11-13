public: yes
tags: [git, PythonAnywhere, Python]
summary: |
  By adding private git repos to PythonAnywhere it becomes a well integrated
  and flexible part of your development environment. `Originally published on the PythonAnyhere blog last week <http://blog.pythonanywhere.com/43/>`_.

Adding private git repos to your PythonAnywhere account
=======================================================

At PythonAnywhere we love github as much as the next person. It's great! We use
it for our main private repository and have a few public ones up there as well.

But sometimes you just want a private place to backup your little project to.
And if you are like me you have about 30 little projects that are the software
equivalent of napkin scribbling. Or maybe you think github is a little bit too
cool. Maybe it's trying too hard?

.. image:: http://www.pythonanywhere.com/static/anywhere/images/git-fresh.jpg
   :alt: incidentally Git Fresh are PythonAnywhere's favourite Miami based R&B-Hip-Hop like product

*incidentally Git Fresh are PythonAnywhere's favourite Miami based R&B-Hip-Hop like product*

So sure you could just make those repos public but urgh. Not everything is public.
Sometimes they are private to just you or sometimes you want to work on
something with just a couple of other collaborators.

On PythonAnywhere with a premium account you can set up as many private repos
as you want, as long as they fit within the diskspace limitations[1], for $5 a
month.

So, here's how it works
-----------------------


PythonAnywhere has web based Bash consoles. We are going to use one of those to
create a git repository. Then on your local machine we are going to clone
it and make a commit. Then push that commit back up to your new private repo on
PythonAnywhere.

The first thing you will need is a PythonAnywhere account. [So go here](https://www.pythonanywhere.com/pricing/)
and sign up for one and then come back.

Now visit your consoles tab and start a fresh Bash session.

Once inside you will be at a prompt that looks something like this and we
can make our first remote repo

.. code-block:: bash

    <username>@PythonAnywhere:~$ mkdir my_repo.git
    <username>@PythonAnywhere:~$ cd my_repo.git
    <username>@PythonAnywhere:~$ git init --bare

You can call your repo whatever you want. There is no potential for namespace
collisions because everything is inside your own account.

Now, from your local machine you can clone that repo using

.. code-block:: bash

    ~/:$ git clone <username>@ssh.pythonanywhere.com:my_repo.git

If you haven't added your public key to /home/<username>/.ssh/authorized_keys
then this step will ask you for your PythonAnywhere account password.

You can now add a file, make your first commit and push back to
PythonAnywhere.

.. code-block:: bash

    ~/:$ cd my_repo
    ~/:$ touch README.md
    ~/:$ git add README.md
    ~/:$ git commit -m"Initial commit on my private PythonAnywhere repo"
    ~/:$ git push origin master

And that is it! Feel free to set up shared accounts to collaborate with others
or work directly on your repo via our in browser editor.


Some additional tips and hints
---------------------------------


Below are a couple more tips for people using PythonAnywhere as their git
repository.

The git repo on PythonAnywhere is a bare repo. That means it has no working
tree. You cannot work directly inside it. If you want to hack on your project
directly from PythonAnywhere you will need to do a local clone. From a
PythonAnywhere Bash console run,

.. code-block:: bash

    <username>@PythonAnywhere:~$ git clone my_repo.git my_repo

Then do your work inside my_repo and push back to origin if you want to pull
those changes outside PythonAnywhere.

Your PythonAnywhere git repos work over SSH. To enable pushing and pulling
without having to enter passwords you can add your public key to your account.
There are many ways to do this. But the following commands will work even if
you have never created a Public/Private key pair before. If you have an
existing key pair just skip the ssh-keygen part.

.. code-block:: bash

    ~/:$ ssh-keygen -t rsa
    ~/:$ ssh-copy-id <username>@ssh.pythonanywhere.com

Another way to make ssh access to a remote server easier is to put some
settings into ~/.ssh/config.

My section for PythonAnywhere looks like this:

.. code-block:: bash

    Host paw
    HostName ssh.pythonanywhere.com
    User hansel
    IdentityFile ~/.ssh/my_pythonanywhere.key

This means that if I want to connect to PythonAnywhere all I need to type is

.. code-block:: bash

    ~/:$ ssh paw

It even autocompletes :)

Another benefit is that I can clone one of my repos from PythonAnywhere with


    ~/:$ git clone paw:my_repo.git


[1] Well, limited by disk space, but not quantity of repos, have a look at our account types for more info.
