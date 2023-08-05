NoDB
====

|Build Status| |Coverage| |PyPI| |Slack| |Gun.io| |Patreon|

NoDB isn't a database.. but it sort of looks like one.

It's an incredibly simple Pythonic object store based on S3.

Useful for **prototyping**, **casual hacking**, and (maybe) even
low-traffic **server-less backends**!

Features
--------

-  Schema-less!
-  Server-less!
-  Uses S3 as a datastore.
-  Loads to native Python objects with ``cPickle``
-  Alternately use JSON as a storage format for untrusted data
-  Cheap!
-  Fast(ish)

Installation
------------

**NoDB** can be installed easily via ``pip``, like so:

::

    $ pip install nodb

Warning!
--------

**NoDB** is **insecure by default**! Do not use it for untrusted data
before setting ``serializer`` to ``"json"``!

Usage
-----

**NoDB** is super easy to use!

You simply make a NoDB object, point it to your bucket and tell it what
field you want to index on.

.. code:: python

    # Set it up
    from nodb import NoDB

    nodb = NoDB()
    nodb.bucket = "my-s3-bucket"
    nodb.index = "Name"

After that, you can save and load literally anything you want, whenever
you want!

.. code:: python

    # Save an object!
    user = {"Name": "Jeff", "age": 19}
    nodb.save(user)

    # Load our object!
    user = nodb.load("Jeff")
    print user.age # 19

By default, you can save and load any Python object.

Advanced Usage
--------------

Different Serializers
~~~~~~~~~~~~~~~~~~~~~

To use a safer, non-Pickle serializer, just set JSON as your serializer:

.. code:: python

    nodb = NoDB()
    nodb.serializer = "json"

Object Metadata
~~~~~~~~~~~~~~~

You can get metainfo (datetime and UUID) for a given object by passing
``metainfo=True`` to ``load``, likek so:

.. code:: python

    # Load our object and metainfo!
    user, datetime, uuid = nodb.load("Jeff", metainfo=True)

Human Readable Indexes
^^^^^^^^^^^^^^^^^^^^^^

By default, the indexes are hashed. If you want to be able to debug
through the AWS console, set ``human_readable_indexes`` to True:

.. code:: python

    nodb.human_readable_indexes = True

TODO (Maybe?)
-------------

-  **Tests**
-  Different serializers
-  Custom serializers
-  Local file storage
-  Quering ranges (numberic IDs only), etc.
-  Multiple indexes
-  Compression
-  Bucket management
-  Dumps

Related Projects
----------------

-  `Zappa <https://github.com/Miserlou/Zappa>`__ - Python's server-less
   framework!
-  `K.E.V. <https://github.com/capless/kev>`__ - a Python ORM for
   key-value stores based on Redis, S3, and a S3/Redis hybrid backend.

Contributing
------------

This project is still young, so there is still plenty to be done.
Contributions are more than welcome!

Please file tickets for discussion before submitting patches. Pull
requests should target ``master`` and should leave NoDB in a "shippable"
state if merged.

If you are adding a non-trivial amount of new code, please include a
functioning test in your PR. For AWS calls, we use the ``placebo``
library, which you can learn to use `in their
README <https://github.com/garnaat/placebo#usage-as-a-decorator>`__. The
test suite will be run by `Travis
CI <https://travis-ci.org/Miserlou/NoDB>`__ once you open a pull
request.

Please include the GitHub issue or pull request URL that has discussion
related to your changes as a comment in the code
(`example <https://github.com/Miserlou/Zappa/blob/fae2925431b820eaedf088a632022e4120a29f89/zappa/zappa.py#L241-L243>`__).
This greatly helps for project maintainability, as it allows us to trace
back use cases and explain decision making.

License
-------

(C) Rich Jones 2017, MIT License.

.. |Build Status| image:: https://travis-ci.org/Miserlou/NoDB.svg
   :target: https://travis-ci.org/Miserlou/NoDB
.. |Coverage| image:: https://img.shields.io/coveralls/Miserlou/NoDB.svg
   :target: https://coveralls.io/github/Miserlou/NoDB
.. |PyPI| image:: https://img.shields.io/pypi/v/NoDB.svg
   :target: https://pypi.python.org/pypi/nodb
.. |Slack| image:: https://img.shields.io/badge/chat-slack-ff69b4.svg
   :target: https://slack.zappa.io/
.. |Gun.io| image:: https://img.shields.io/badge/made%20by-gun.io-blue.svg
   :target: https://gun.io/
.. |Patreon| image:: https://img.shields.io/badge/support-patreon-brightgreen.svg
   :target: https://patreon.com/zappa


