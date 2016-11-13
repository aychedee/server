public: yes
tags: [linux, learning]
summary: |
  So much ASCII, so little time

man man
=======

People learn things in all kinds of different ways. For me, nothing beats just
using something in a real world application. But there is a lot to be said for
randomly poring through the reference material. If you have Linux installed
then you have ready access to the the world's most arcane and obtuse reference.
Unix man pages!

.. code-block:: bash

    :~$ apropos . | wc -l
    7015

You can use the `apropos` command to search these manual pages and their
descriptions. Or you can use "." to match all of them, and pipe them to `wc -l`
which tells you how many lines of output it gave. On my system there are 7015.

In the interest of brute force learning I am making an attempt to read them all
over the next year. That is about 20 a day. Manageable.

On Linux, man pages are divided into 9 different sections. Described below.
This table is lifted from `man man`, natch.

1. Executable programs or shell commands
2. System calls (functions provided by the kernel)
3. Library calls (functions within program libraries)
4. Special files (usually found in /dev)
5. File formats and conventions eg /etc/passwd
6. Games
7. Miscellaneous (including macro packages and conventions), e.g. man(7), groff(7)
8. System administration commands (usually only for root)
9. Kernel routines [Non standard]

 You can limit your search to sections by passing `-s` to apropos. The entry
 counts for each section on my system are:


.. code-block:: bash

    :~$ apropos -s 1 . | wc -l
    1536
    :~$ apropos -s 2 . | wc -l
    428
    :~$ apropos -s 3 . | wc -l
    3948
    :~$ apropos -s 4 . | wc -l
    60
    :~$ apropos -s 5 . | wc -l
    280
    :~$ apropos -s 6 . | wc -l
    17
    :~$ apropos -s 7 . | wc -l
    205
    :~$ apropos -s 8 . | wc -l
    541
    :~$ apropos -s 9 . | wc -l
    .: nothing appropriate.
    0

As you can see the bulk of the entries are for library calls, and shell
commands. Since my main goal is to gain a deeper understanding of Linux I think
I'm going to start with section 2.

.. code-block:: bash

    :~$ apropos -s 2 . | less

Will give you a list of my next 21 days worth of reading material. Wish me
luck.
