public: yes
tags: [Nginx, uWSGI, literate programming]
summary: |
  Software projects built with personality can be so much easier to use

The importance of memorability: tyrants, vassals, and broodlords
================================================================

Over the last week we've been moving our servers from Apache to Nginx and
uWSGI. It's been great. There is a definite elegance to the design of Nginx
that is missing from Apache. 

One of the things that really jumps out is how much easier the documentation is 
to read. Even though the grammar might be poor. It is still easy to understand. 

Part of that I think is the coherent and memorable naming system. Things just 
make sense. When your uWSGI vassal accepts a request from the Emperor it 
becomes loyal, when a non-loyal vassal dies it is put on a blacklist. The 
emperor process can be run in Tyrant mode if, from the docs:

    If you want to allows users editing/customizing their config files, 
    you cannot trust their loyalty allowing them to omit uid ang gid prameters.

    For this case the Tyrant mode is available (add --emperor-tyrant).

There is a certain amount of whimsy to all this documentation but the concepts 
are very clear and really stick with you. Compare it with some of the Apache 
documentation. Which is all grammatically correct but totally obtuse and almost
impossible to understand,

    %{LA-U:variable} can be used for look-aheads which perform an internal
    (URL-based) sub-request to determine the final value of variable. This
    can be used to access variable for rewriting which is not available at
    the current stage, but will be set in a later phase.  

    For instance, to rewrite according to the REMOTE_USER variable from
    within the per-server context (httpd.conf file) you must use
    %{LA-U:REMOTE_USER} - this variable is set by the authorization phases,
    which come after the URL translation phase (during which mod_rewrite
    operates)
    
None of this is EVER clear. One of the most annoying things that I came across 
in Apache was their misuse of *environment variable* and *ENV*. One would think
that this has something to do with the OS'es environment. Of course you would 
be wrong. Well not wrong in all cases. But sometimes wrong... Fuck, I'm glad to 
be moving to Nginx anyway. If you can't tell. 
