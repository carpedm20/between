import between

account = "YOUR_ID"
password = "YOUR_PASSWORD"

client = between.Client(account, password)

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
                                ws.send_image(image_id=attachment['reference'])
                            elif attachment.has_key('sticker'):
                                ws.send_sticker(attachment['sticker']['sticker_id'])
                        elif msg.has_key('content'):
                            ws.send(msg['content'])

bot = between.Bot(client=client, on_message=on_message)
bot.run_forever()
