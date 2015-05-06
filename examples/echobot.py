import betweeen

def on_message(ws, message):
    print message

def on_open(ws):
    ws.send("Hello World!")

bot = betweeen.Bot("YOUR_ID", "YOUR_PASSWORD", on_open=on_open, on_message=on_message)
bot.run_forever()
