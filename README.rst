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

Simple commands:

.. code-block:: python

    import betweeen

    client = betweeen.Client("YOUR_ID", "YOUR_PASSWORD")
    client.send("Carpe diem!")
    client.send_sticker()
    client.send_image("./test.jpg")

`Simple bot <https://github.com/carpedm20/between/blob/master/examples/simplebot.py>`__:

.. code-block:: python

   import betweeen

   def on_message(ws, message):
      print message

   def on_open(ws):
      ws.send("Hello World!")

   bot = betweeen.Bot("YOUR_ID", "YOUR_PASSWORD", on_open=on_open, on_message=on_message)
   bot.run_forever()

`Echo bot <https://github.com/carpedm20/between/blob/master/examples/echobot.py>`__:

.. code-block:: python

   import between

   client = betweeen.Client("YOUR_ID", "YOUR_PASSWORD")

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


Authors
=======

Taehoon Kim / `@carpedm20 <http://carpedm20.github.io/about/>`__
