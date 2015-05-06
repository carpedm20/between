========
between
========

.. image:: https://fbcdn-profile-a.akamaihd.net/hprofile-ak-xap1/v/t1.0-1/p200x200/10517518_750265521675300_788817894578396496_n.png?oh=7ca341ef155d138a5a44367e2ea16352&oe=55CBB403&__gda__=1438880194_5cb73422083338e6855db51023441766

`Between <https://between.us/?lang=en>`__ of `VCNC <https://between.us/about>`__ for Python.

*How to be loved?* This is the answer for your question.


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

    $ pip install between


Example
=======

Simple commands:

.. code-block:: python

    import between

    client = between.Client("YOUR_ID", "YOUR_PASSWORD")
    client.send("Carpe diem!")
    client.send_sticker()
    client.send_sticker("85_12")
    client.send_image("./test.jpg")
    print client.get_recent_messages()

`Simple bot <https://github.com/carpedm20/between/blob/master/examples/simplebot.py>`__:

.. code-block:: python

   import between

   def on_message(ws, message):
      print message

   def on_open(ws):
      ws.send("Hello World!")

   bot = between.Bot("YOUR_ID", "YOUR_PASSWORD", on_open=on_open, on_message=on_message)
   bot.run_forever()

`Echo bot <https://github.com/carpedm20/between/blob/master/examples/echobot.py>`__:

.. code-block:: python

   import between

   client = between.Client("YOUR_ID", "YOUR_PASSWORD")

   me = client.me.account_id
   lover = client.lover.account_id

   def on_message(ws, message):
      print message

      if message.has_key('p'):
         if message['p'] == 'events':
               for event in message['m']['events']:
                  if event['action'] == 'EA_ADD':
                     msg = event['messageEvent']['message']

                     if msg['from'] != me:
                           if msg.has_key('attachments'):
                              attachment = msg['attachments'][0]

                              if attachment.has_key('reference'):
                                 # echo image
                                 ws.send_image(image_id=attachment['reference'])

                              elif attachment.has_key('sticker'):
                                 # echo sticker
                                 ws.send_sticker(attachment['sticker']['sticker_id'])
                           elif msg.has_key('content'):
                              # echo message
                              ws.send(msg['content'])

   bot = between.Bot(client=client, on_message=on_message)
   bot.run_forever()


Features
========

- Login and authentication
- Send a message
- Send a sticker
- Send an image
- Get recent messages
- Message long polling
- Get uploaded image lists (in progress)
- *This work is not connected with Between or VCNC Corporation*


Screenshot
==========

.. image:: https://raw.githubusercontent.com/carpedm20/between/master/contents/demo.png
   :width: 90%


Authors
=======

Taehoon Kim / `@carpedm20 <http://carpedm20.github.io/about/>`__
