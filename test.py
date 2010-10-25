from pybot import Pybot
from protocol import IRC

p = Pybot("comm.devpayments.com")
p.join("#pcilevelonecompliant")

while True:
  temp = p.fetch()

  for line in temp:
    content = IRC.getContent("#pcilevelonecompliant", line)
    user = IRC.getUser(line)

    if content != "":
      #someone said something in our channel, echo it back
      p.say("#pcilevelonecompliant", "hello " + user + ", you just said: " + repr(content)) 
