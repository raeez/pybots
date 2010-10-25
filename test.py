from pybot import Pybot

p = Pybot("comm.devpayments.com")
p.join("#pcilevelonecompliant")

while True:
  messages = p.fetch()

  for msg in messages:
    if msg.content != "":
      #someone said something in our channel, echo it back
      p.say("#pcilevelonecompliant", "user [%s] just said message[%s] in channel[%s]" % (msg.user, repr(msg.content), msg.channel)) 
