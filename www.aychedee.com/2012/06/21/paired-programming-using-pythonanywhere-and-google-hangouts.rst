public: yes
tags: [XP, paired programming, Google]
summary: |
  Combining a variety of tools into a useful suite 

Paired programming using PythonAnywhere and Google Hangouts
===========================================================

All of our work on PythonAnywhere is done paired. For those not familiar with
Extreme Programming (Don't look at me like that, I didn't name it...) this 
means that all production code is written by two people at once, both actively
involved, constantly discussing the best solution to a problem and always 
arguing over how to implement it. Pretty intense. 

Normally we are all in the same office so the setup is quite simple. We just 
share a desk and one person drives the keyboard. Sometimes we'll break off to
do some separate research. But mostly all our work is done at one desk in front
of a couple of monitors. 

One of my colleagues was off in the country for a week and wanted to do some
remote pairing. Over the course of the week we tried a variety of different 
options.

First off we started by using our shared consoles and skype. This is a pretty
good solution. We were sharing a separate console for each task. So we had one
for each of:

    1. Vim
    2. Git
    3. Dev machine (running on AWS)
    4. IPython as a scratchpad

The problem with this is it didn't give us a good way of sharing anything that
we were running locally. Skype's screen sharing support for Linux just didn't 
work for us unfortunately. Really all we wanted was to share a local terminal
window so that we could see the results of running our integration tests. 

What did work surprisingly well was Google Hangouts. And the way that you can 
alternate between screen sharing, video, or even a bit of music is very nice.
It has a few rough edges. It times you out for inactivity. But inactivity is
defined as not clicking around through the interface. Which is kind of stupid
and did cut us off a few times. Anyway, it's worth trying out. 
