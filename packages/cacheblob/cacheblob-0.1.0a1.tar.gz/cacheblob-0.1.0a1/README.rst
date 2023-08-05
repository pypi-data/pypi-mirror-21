python-cacheblob
================

cacheblob is a key-value interface for expiring items.

Installation
------------

pip install python-cacheblob

Usage
-----

.. code-block:: python

    import datetime
    from cacheblob import Cacheblob

    cache = Cacheblob.cache(handler='mongo')
    cache.store(index='index2', value='value2', duration=datetime.timedelta(days=1))
    for item in cache.fetch_all():
        print item

Use Case
--------

cacheblob was designed for data sources that should age and expire. Using it should be as
simple as setting an expiry time (or duration) on your data. 

As such, cacheblob avoids imposing too many design decisions upon the user beyond those
necessary for its expiry functionality. It decouples the interface and the storage
mechanism by allowing arbitrary underlying storage systems, called *handlers* in
cacheblob.

Cacheblob has an *item* concept, which is a key-value pair with an expiry time. Most
handlers except strings for values or will work with any values that can be converted to
strings. Not all handlers are necessarily subject to this limitation.

Cacheblob was designed to be lightweight by default, and to be flexible, by allowing the
user to choose their underlying storage model. Worried about concurrency? Use a handler
that allows concurrent access. You want your items as files on disk for easy access by
programs that expect them as such? Use a file-backed handler. Choose your own
consistency-availability-tolerance trade-off.

The current implemented handlers are:

- handler: A lightweight wrapper that uses Python's in-memory storage
- mongo: Store items in a Mongo database
- sqlite: Store items in a SQLite database
- plaintext: Store items as files in a folder on disk
- gzip: Store items as gzip files in a folder on disk

Authors
-------

rdj - https://oddacious.github.io
