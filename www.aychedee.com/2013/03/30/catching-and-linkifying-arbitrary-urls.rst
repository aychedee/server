public: yes
tags: [python, regex, web]
summary: |
  Finding and turning into links arbitrary urls from user input

Catching and linkifying arbitrary urls in user input
====================================================

`RogueShell <http://www.rogueshell.com/>`_ users have asked for a couple of
improvements to the public site chat. A few People wanted to be able to use the
IRC command "/me" and everyone thought that pasted links should be made
clickable.

Adding support for "/me" was pretty simple. But matching urls was trickier.
The solutions I found were all relying on their being some kind of url'ish
prefix (like "://" or "www") but I wanted to match the most basic url pattern
that people might use: example.com or example.co.nz as well. Google does it in
gchat after all.

So I approached it from a slightly different position. I decided that a url
would be a "." that isn't followed by another period and does not have a space
on either side

I decided it would be better to have a few false positives than to limit people
to having to use a protocol marker. And I could safely assume that any urls
without a protocol should be http. So the regex I came up with was:

.. code-block:: python

    re.compile(r"""[^\s]             # not whitespace
                   [a-zA-Z0-9:/\-]+  # the protocol and domain name
                   \.(?!\.)          # A literal '.' not followed by another
                   [\w\-\./\?=&%~#]+ # country and path components
                   [^\s]             # not whitespace""", re.VERBOSE)

You can see the regex working in an `interactive Python console here <https://www.pythonanywhere.com/gists/5276197/url_regex.py/ipython2>`_

I'm sure there are a few edge cases that I haven't thought of. But as they
come up I'll keep this post updated with them.
