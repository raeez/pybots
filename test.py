from pybot import Pybot

p = Pybot("comm.devpayments.com")
p.join("#pcilevelonecompliant")

while True:
  temp = p.fetch()

  for line in temp:
    parts = line.split("PRIVMSG #pcilevelonecompliant :")
    if len(parts) > 1:
      p.say("#pcilevelonecompliant", parts[1])
