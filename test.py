from pybot import Pybot

HOST = "comm.secretsite.com"
CHANNELS = ["#pcilevelonecompliant", "#pcileveltwocompliant"]

p = Pybot(HOST)
p.join(CHANNELS)

while True:
  for msg in p.fetch():
    if msg.channel in CHANNELS:
      #someone said something in our channel, echo it back
      p.say(CHANNELS, "user [%s] just said message[%s] in channel[%s]" % (msg.user, repr(msg.content), msg.channel))
