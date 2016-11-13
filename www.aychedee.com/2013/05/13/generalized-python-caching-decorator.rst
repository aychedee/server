public: yes
tags: [tools, Python, decorator]
summary: |
  A generalized caching decorator for Python sites

A general caching decorator for Python
======================================

I was writing a new blog engine today that uses plain text markdown files for
the posts. They need to be converted into html before they can be served to the
browser. Generating each response was quite computationally intensive. But at
the same time I didn't want to statically generate the html. It is just
irritating to have to go through a compile step everytime you fix a typo or
make a minor change to a sentence.

So naturally I thought of using a decorator to cache or memoize the posts
function. There are plenty of examples that can handle a function with
positional arguments. But none that I found that could cache a function that
took args as *well* as keyword arguments. Mainly because dictionaries are not
hashable types. That makes them a bit trickier to use as keys. Below is what I
ended up using:

.. code-block:: python

    def cache_me(cache):

        def wrapper(func):
            if NOT_CACHING:
                return func

            def inner(*args, **kwargs):
                hashed_kwargs = hash(frozenset(kwargs.items()))
                try:
                    return cache[(args, hashed_kwargs)]
                except KeyError:
                    cache[(args, hashed_kwargs)] = func(*args, **kwargs)
                    return cache[(args, hashed_kwargs)]

            return inner

        return wrapper

And here shown being actually used:

.. code-block:: python

    @cache_me(cache={})
    post(post_name):
        return Post(post_name).render()

When I am developing I set the global NOT_CACHING to True and then I can get
instant feedback on any changes. With caching turned on the site could now
handle a request every 5ms. Which compares pretty well to 35ms with it off. It
is not perfect. In some cases it will generate a false cache hit because it is
ignoring the keys and only cares about the values of the dictionary.
