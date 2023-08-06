===============================
Kinto Pusher
===============================

.. image:: https://img.shields.io/travis/Kinto/kinto-pusher.svg
        :target: https://travis-ci.org/Kinto/kinto-pusher

.. image:: https://img.shields.io/pypi/v/kinto-pusher.svg
        :target: https://pypi.python.org/pypi/kinto-pusher

Plug `Kinto notifications <http://kinto.readthedocs.io/en/latest/core/reference/notifications.html>`_
into `Pusher.com <http://pusher.com>`_.

* `Online demo <https://kinto.github.io/kinto-pusher/>`_


Install
-------

::

    pip install kinto-pusher

Depending on your environment, it might be necessary to install the `ffi system library <https://sourceware.org/libffi/>`_ with ``sudo apt-get install libffi-dev``.


Setup
-----

In the Kinto-based application settings:

.. code-block:: ini

    kinto.includes = kinto_pusher

    pusher.app_id = <pusher-app-id>
    pusher.key = <pusher-key>
    pusher.secret = <pusher-secret>
    pusher.cluster = eu

    kinto.event_listeners = pusher
    kinto.event_listeners.pusher.use = kinto_pusher.listener

    kinto.event_listeners.pusher.channel = {bucket_id}-{collection_id}-{resource_name}
    kinto.event_listeners.pusher.resources = bucket collection group record
    kinto.event_listeners.pusher.actions = create update delete


TODO
----

- Add view for authenticated channels


Changelog
=========

0.6.0 (2017-04-25)
------------------

- Upgrade to Kinto 6 and Python 3.5 (#21)


0.5.0 (2017-02-21)
------------------

- Fixing some common 500 with the plugin (#20)

0.4.0 (2016-12-02)
------------------

- Add the plugin version in the capability. (#12)
- Handle the ``pusher.cluster`` option. (#17)
- Update to super Kinto 5.0


0.3.0 (2016-05-23)
------------------

- Project renamed to *Kinto-fxa* to match the rename of ``cliquet`` to
  ``kinto.core``.

- Update to ``kinto.core`` for compatibility with Kinto 3.0. This
  release is no longer compatible with Kinto < 3.0, please upgrade!


0.2.0 (2015-11-20)
------------------

- Add HTML demo with *Kinto* and *Leaflet*
- Works with *Cliquet* 2.11


0.1.0 (2015-11-05)
------------------

- Initial working proof-of-concept.


