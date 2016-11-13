public: yes
tags: [Linux, Python]
summary: |
  A Common need when scripting a complex system is to have processes that only
  run if they are not already running. On Linux you can do this without 
  using the filesytem

Using domain sockets on Linux instead of lockfiles
==================================================

If you have a script on a server that you want to make sure is run frequently 
but also might run for an arbitrary amount of time then you typically want to 
make sure that it is never started before the previous run has finished. 

The standard way of achieving this is to create a temporary lockfile. When
your script starts it checks for the existence of the lockfile and exits if it 
does. Even better, the lockfile might contain the PID of the process that
created it. If that process is still running then exit, else overwrite the 
lockfile with one of your own. 

Of course what if a process with that PID does exist but isn't the correct 
process? This is a rare state but could happen for a number of reasons. Maybe
the power goes off and the new set of PIDS that exist when the server comes
back up overlap with whatever is in that lockfile. 

A better solution on a Linux system is to use a named domain socket. Some
example Python code is below. 

.. code-block:: python

    import socket
    import sys
    import time

    def get_lock(process_name):
        global lock_socket
        lock_socket = socket.socket(socket.AF_UNIX, socket.SOCK_DGRAM)
        try:
            lock_socket.bind('\0' + process_name)
            print 'I got the lock'
        except socket.error:
            print 'lock exists'
            sys.exit()


    get_lock('running_test')
    while True:
        time.sleep(3)

This has the advantage that you never leave lockfiles lying around and you can
be sure that the process that is currently bound to the socket is really the 
one that you think it is. 
