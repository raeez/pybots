from pybot import Pybot

p = Pybot("comm.devpayments.com", nick="dumbot")
p.join("#secretchannel")

while True:
  p.say("#secretchannel", "haha, can't catch me")
