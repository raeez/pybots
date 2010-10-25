from pybot import Pybot
from protocol import IRC

p = Pybot("comm.devpayments.com")
p.join("#pcilevelonecompliant")

while True:
  messages = p.fetch()

  for msg in messages:
    content = IRC.getContent("#pcilevelonecompliant", msg)
    user = IRC.getUser(msg)

    if content != "":
      #someone said something in our channel, echo it back
      p.say("#pcilevelonecompliant", "hello " + user + ", you just said: " + repr(content)) 
