import between

client = between.Client("YOUR_ID", "YOUR_PASSWORD")

print client.me
print client.lover

for msg in client.get_recent_messages():
    print msg

client.send("Carpe diem!")
client.send_sticker()
client.send_image("./test.jpg")
