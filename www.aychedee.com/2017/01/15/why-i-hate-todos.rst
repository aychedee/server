public: yes
tags: [style, development]
summary: |
  Adding notes to yourself in your own code are fine. But they are a horrible
  way to try and make sure a problem gets fixed in the future.

Why I hate TODOs in shared code bases
=====================================

Whenever I am reading code and I come across a "TODO" I find myself getting irritated by it. If I'm working on code
around it then I have to read this cryptic note, and try and understand what some developer in the distant past
was trying to communicate to me.

But why do I find them so annoying? I’m going to explain that here.

First off, what is a TODO? It’s a note, explaining an area for improvement, or a missing
piece of functionality that you imagine you’ll need later.

A few examples taken from real code bases on github:

.. code-block:: c

    /* TODO remove once all users are switched to gpiod_* API */

`pwm_backlight.h <https://github.com/torvalds/linux/blob/5924bbecd0267d87c24110cbe2041b5075173a25/include/linux/pwm_backlight.h>`_


.. code-block:: c

    ToDo: Needs to be done more properly for AMD/Intel specifics

`topology.c <https://github.com/torvalds/linux/blob/5924bbecd0267d87c24110cbe2041b5075173a25/tools/power/cpupower/utils/helpers/topology.c>`_

.. code-block:: c

    * TODO: make PID parameters tuned automatically,

`pid.c <https://github.com/torvalds/linux/blob/5924bbecd0267d87c24110cbe2041b5075173a25/tools/thermal/tmon/pid.c>`_

They seem harmless enough. And why would I think they’re inappropriate for a shared codebase?

1. If they’re important they should be somewhere else. Put them in your bug tracker, create a ticket, write a detailed reason why this bit of code is going to cause big problems later, let them be properly prioritised by the whole team

2. If they’re not important then please don’t waste your time writing them, and don’t waste other developers time forcing them to read them to understand that they’re not even important

3. If they’re important and completely minor, then just do the work and fix them immediately - You currently have the best understanding of the problem. Making a comment that “TODO: foo will explode under bar circumstances” is going to be meaningless to the next person. They’re going to have to read all the surrounding code and build up their own mental model of what’s happening. Why not save everyone the time and just do it now? If it’s actually important of course.

4. They don’t expire. A TODO from 5 years ago when the business had an entirely different focus is still going to be sitting in the code. Forcing developers to ask themselves “Is this still relevant?”


It's not that I think they are never appropriate, I can think of exactly two cases where they can work:

1. When it’s just you working on a project or...
2. When you don’t have any other form of task tracking, project planning, or bug tracking, i.e the TODOs represent all the things you need to do before you will consider your project finished

You know who disagrees with me though? Linus Torvalds and seemingly every other
developer working on the Linux kernel. So ¯\_(ツ)_/¯   But that is one project
where the code is forced to represent the entire project. Individual folders
feature plain text TODO files which are clearly meant to represent forward
planning.

