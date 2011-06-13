from pybot import Pybot
from os import mkdir
import logging
import logging.handlers
import re

HOST = "localhost"
CHANNELS = ["#somechannel"]
BOTNICK = "timebot"

p = Pybot(HOST, nick=BOTNICK)
p.join(CHANNELS)

p.say(CHANNELS, "%s reporting for duty!" % BOTNICK)


from datetime import datetime, timedelta
from pytz import timezone
import pytz

utc = pytz.utc
est = timezone('US/Eastern')
pst = timezone('US/Pacific')
jhb = timezone('Africa/Johannesburg')
zones = [pst, est, utc, jhb]
fmt = '%H:%M:%S %Z%z'
def talk(m):
  p.say(msg.channel, m)

while True:
  for msg in p.fetch():
    if msg.channel in CHANNELS:
      if re.search("%s:" % BOTNICK, msg.content):
        czones = [utc.localize(datetime.now()).astimezone(z).strftime(fmt) for z in zones]

        map(talk, czones)
        continue
