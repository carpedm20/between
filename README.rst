========
betweeen
========

`Between <https://between.us/?lang=en>`__ of `VCNC <https://between.us/about>`__ for Python.

*How to be loved?* this is the answer for your question.


How to use
==========

1. Date with somebody
2. Install `Between <https://between.us/download/mobile/>`__
3. Write a fun bot
4. **Be loved** by your lover


Installation
============

Simple.

.. code-block:: console

    $ pip install betweeen


Example
=======

.. code-block:: console

    import betweeen

    client = betweeen.Client("YOUR_ID", "YOUR_PASSWORD")
    client.send("Carpe diem!")
    client.send_sticker()
    client.send_image("./test.jpg")


To do
=====

- [x] Login, Authentication
- [x] Send a message
- [x] Send a sticker
- [x] Send an image
- [x] Get recent messages
- [ ] Get uploaded image lists
- [ ] Message long polling


Authors
=======

Taehoon Kim / `@carpedm20 <http://carpedm20.github.io/about/>`__
