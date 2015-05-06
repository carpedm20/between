import between

def on_open(ws):
    ws.send("Hello World!")

def on_message(ws, message):
    print message

def on_error(ws, error):
    print error

def on_close(ws):
    print "### closed ###"

bot = between.Bot("YOUR_ID", "YOUR_PASSWORD",
                  on_open = on_open,
                  on_message = on_message,
                  on_error = on_error
                  on_close = on_close)
bot.run_forever()
