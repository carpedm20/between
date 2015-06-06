import between

client = between.Client("YOUR_ID", "YOUR_PASSWORD")

me = client.me.id
lover = client.lover.id

def on_message(ws, message):
    print message

    if message.has_key('p'):
        if message['p'] == 'events':
            for event in message['m']['events']:
                if event['action'] == 'EA_ADD':
                    msg = event['messageEvent']['message']

                    if msg['from'] != me: # this will not work.. see issue #3
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
