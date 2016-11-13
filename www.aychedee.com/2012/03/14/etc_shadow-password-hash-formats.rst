public: yes
tags: [Linux, sysadmin, security]
summary: |
  The /etc/shadow file stores user passwords as hashes in a particular format.
  If you ever want to verify users passwords against this hash in a non
  standard way, like from a web app for example, then you need to understand
  how it works.

Understanding and generating the hash stored in /etc/shadow
===========================================================

The /etc/shadow file stores user passwords as hashes in a particular format.  If
you ever want to verify users passwords against this hash in a non standard
way, like from a web app for example, then you need to understand how it works.

Each row in /etc/shadow is a string with 9 fields separated by ':'. A typical
line looks like this:

.. code-block:: bash

    aychedee:$6$vb1tLY1qiY$M.1ZCqKtJBxBtZm1gRi8Bbkn39KU0YJW1cuMFzTRANcNKFKR4RmAQVk4rqQQCkaJT6wXqjUkFcA/qNxLyqW.U/:15405:0:99999:7:::

The nine different fields are:

1. The local username
2. The password hash, more on this later
3. Number of days since the start of unix time (01/01/1970) that the password
   was last changed
4. Minimum number of days before the password can be changed
5. Maximum number of days before the password must be changed. 99999 means that
   the user will not be forced to change their password
6. Number of days before forcing the password change that the user will be
   warned.
7. The number of days after expiration that the account will be disabled
8. Days since the start of unix time that the account has been disabled
9. Currently unused but reserved for future use

Most of those fields are generally unused by Linux distros. The important ones
are the username and hash. The hash field itself is comprised of three
different fields. They are separated by '$' and represent:

1. Some characters which represents the cryptographic hashing mechanism used to
   generate the actual hash
2. A randomly generated `salt to safeguard against rainbow table attacks <http://www.codinghorror.com/blog/2007/09/rainbow-hash-cracking.html>`_
3. The hash which results from joining the users password with the stored salt
   and running it through the hashing mechanism specified in the first field

Make sense?

So that first field before the salt and actual hash can have a finite set of
possible values. The standard methods supported by GNU/Linux are:

Available algorithms:

 $1$
    md5
 $2a$
    Blowfish
 $2y$
    Blowfish, with correct handling of 8 bit characters
 $5$
    sha256
 $6$
    sha512

In practice you shouldn't use anything but sha512. The mkpasswd command will
create the hash string for you and can be used by other programs to check an
existing hash. Given the password hash above, if you wanted to check if a given
password matched it you would run the following command:

.. code-block:: bash

    mkpasswd --method=sha512 --salt=vb1tLY1qiY PASSWORD

The equivalent using python looks like this:

.. code-block:: python

    import crypt

    crypt.crypt('PASSWORD', '$6$vb1tLY1qiY')

Both will return an exact copy of the hash. for the given salt and password.
Notice how using the Python library you actually pass in the method as part of
the salt string. A salt string starting with '$5$' would use sha256 for example.

You can then compare this hash with the hash in /etc/shadow, or anywhere else
that they might be stored. Like in a central datbase if you are using NSS.

If you don't provide mkpasswd with a salt it will automatically generate a
random salt. This is usually what you want to do if you are creating a password
for the first time.

