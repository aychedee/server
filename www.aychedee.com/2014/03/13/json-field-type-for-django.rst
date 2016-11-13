public: yes
tags: [python, JSON, web]
summary: |
  A JSON field type for django with associated general JSON classes

A JSON field type for Django
============================

At `Metric.io <https://metric.io>`_ we've been finding a need to store JSON
data in Postgresql. You can just use a text field to store JSON, but
Postgresql does have a native JSON type and `using it does have it's advantages <http://www.postgresql.org/docs/9.3/static/functions-json.html>`_.

The PsycoPG2 python adaptor now has native support for JSON types in
Postgresql. However we needed a standard interface for other database types as
well because we use sqlite for development and some unit tests.

The solution was to create a JSON type that could handle input in the form of
Python strings, lists or dicts, as well as JSON strings, lists, and dicts.

You can see what I came up with just below. It uses a meta class to dynamically
switch between three different (JsonDict, JsonList, JsonString) classes based
on the input it is instantiated with.

.. code-block::  python

    from collections import MutableMapping, MutableSequence
    import json


    class _JsonMeta(type):

        def __call__(cls, column_data):
            try:
                pyobj = json.loads(column_data)
                json_string = column_data
            except (ValueError, TypeError):
                pyobj = column_data
                json_string = json.dumps(column_data)
            if isinstance(pyobj, dict):
                return type.__call__(JSON.JsonDict, pyobj, json_string)
            if isinstance(pyobj, list):
                return type.__call__(JSON.JsonList, pyobj, json_string)
            return type.__call__(JSON.JsonString, pyobj, json_string)


    class JSON(object):
        __metaclass__ = _JsonMeta


        class InvalidJSON(Exception):
            pass


        class JsonDict(MutableMapping):

            def __init__(self, pyobj, json_string):
                self._data = {}
                self._data.update(pyobj)
                self.json_string = json_string

            def __setitem__(self, k, v):
                self._data[k] = v
                self.update_json()

            def __delitem__(self, k):
                del self._data[k]
                self.update_json()

            def __getitem__(self, k):
                return self._data[k]

            def __iter__(self):
                return iter(self._data)

            def __len__(self):
                return len(self._data)

            def update_json(self):
                self.json_string = json.dumps(self._data)

            def __unicode__(self):
                return unicode(json.dumps(self._data))


        class JsonString(str):

            def __new__(self, pyobj, json_string):
                self.json_string = json_string
                return str.__new__(self, pyobj)

            def __unicode__(self):
                return "%s" % (self.json_string,)

            __str__ = __unicode__


        class JsonList(MutableSequence):

            def __init__(self, pyobj, json_string):
                self.json_string = json_string
                self._contents = list(pyobj)

            def __delitem__(self, i):
                del self._contents[i]
                self.update_json()

            def __getitem__(self, i):
                return self._contents[i]

            def __len__(self):
                return len(self._contents)

            def __setitem__(self, i, v):
                self._contents[i] = v
                self.update_json()

            def insert(self, i, v):
                self._contents.insert(i, v)
                self.update_json()

            def update_json(self):
                self.json_string = json.dumps(self._contents)

            def __unicode__(self):
                return unicode(json.dumps(self._contents))

The actual Django JSONField is comparatively simple. In the db_type method we
test for the database engine, and use the 'json' type if we have Postgresql
available, otherwise we use a straight 'text' type. The to_python and
get_prep_value methods both have to handle our own Python JSON types, strings,
strings containing encoded JSON, and Python dicts, lists and None. Most of the
logic for which is held in our own JSON type anyway.

.. code-block::  python

     from django.db import models
     from django.utils import six


    class JSONField(six.with_metaclass(models.SubfieldBase, models.TextField)):

        description = 'A JSON database field, returns a string, list or dict type'

        def db_type(self, connection):
            if connection.settings_dict[
                    'ENGINE'] == 'django.db.backends.postgresql_psycopg2':
                return 'json'
            return 'text'

        def to_python(self, value):
            if hasattr(value, 'json_string') or value is None:
                return value
            return JSON(value)

        def get_prep_value(self, value):
            '''The psycopg adaptor returns Python objects,
                but we also have to handle conversion ourselves
            '''
            if isinstance(
                value, JSON.JsonDict) or isinstance(value, JSON.JsonList):
                    return value.json_string
            if isinstance(value, JSON.JsonString):
                return json.dumps(value)
            return value

The next stages will be to add support for querying JSON directly in
Postgresql. I'll update this post as our JSON field types progresses.

NB: There are many other JSON field types for Django available. I checked out a
lot of them before writing my own. But none of them can handle Postgresql's
actual JSON type as well as a plain text db type.
