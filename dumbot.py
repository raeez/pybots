from pybot import Pybot

p = Pybot("comm.secretsite.com", nick="dumbot")
p.join("#secretchannel")

while True:
  p.say("#secretchannel", "haha, can't catch me")
