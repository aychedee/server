public: yes
tags: [sysadmin, Linux]
summary: |
  This little trick has saved us a lot of time recently

Quickly force a reboot under Linux
==================================

It is quite possible for a linux server to be get into a state where the
standard reboot command does not work. Or takes a long time because multiple
programs (I'm looking at you NFS...) have to timeout first.

When you have physical access to a machine you can always just powercycle it.
But when your 'machine' is a virtualised entity in the Pacific North-East
that isn't an option.

Luckily Linux exposes an interface to directly control the kernel using SysRq
key codes. It lives at `/proc/sysrq-trigger`.

.. code-block:: bash

    ls -l /proc/sysrq-trigger
    --w------- 1 root root 0 May 24 08:06 /proc/sysrq-trigger

ASCII characters you echo to it will be interpreted as if you had just pressed
Alt + SysRq + *Char*. So for an immediate forced reboot you can do:

.. code-block:: bash

    sudo echo "s" > /proc/sysrq-trigger
    sudo echo "b" > /proc/sysrq-trigger

This (s)yncs the filesystem and then re(b)oots the machine. Absolutely nothing
stops this happening. So that NFS mount with an open bash sessions CD'd
somewhere into it cannot tell the reboot process to wait for 10 minutes.

A safer sequence of characters is supposed to be REISUB. Which is: Switch
keyboard from (r)aw mode, send SIGTERM, (e)xit, to all process except init,
send SIGKILL, (i)nterrupt, to all processes, except init, (s)ync all mounted
filesystems, (u)nmount and remount all filesystems read only, then re(b)oot the
machine.

But if you are ssh'd into a remote server I have no idea how you would enter
anything after RE since by that time your connection will have died due to the
ssh server exiting. SUB is the most you will need and in practice SB is fine.

A `full list of the SysRq keys are available on Wikipedia. <http://en.wikipedia.org/wiki/Magic_SysRq_key>`_
