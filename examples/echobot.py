import betweeen

client = betweeen.Client("YOUR_ID", "YOUR_PASSWORD")

def on_message(ws, message):
    print message

client.run_forever(on_message)
