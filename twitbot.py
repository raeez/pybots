from pybot import Pybot
import smtplib
from email.mime.text import MIMEText

import sys
sys.path.append('twitter/')

from twitter import Api

HOST = "comm.devpayments.com"
CHANNELS = ["#pcilevelonecompliant", "#pcileveltwocompliant"]

p = Pybot(HOST, nick='twitbot')
p.join(CHANNELS)


api = Api(username='twitbot_', password='twitbot', access_token_key='FRzVzZs0SSyWgPsR9mxiQw', access_token_secret='eoPZSrScusq6gdc33AkPek9nlPYCzuKjPBlGDt91wA')


while True:
  for msg in p.fetch():
    if msg.channel in CHANNELS and msg.content.find("status") != -1 and msg.content.find("twitbot:") != -1:

      workers = api.GetFriends()
      status = [api.GetUserTimeline(s) for s in workers]
      print repr(status)

      email = MIMEText('twitbot reporting for duty')
      email['Subject'] = 'twitbot reporting for duty'
      email['From'] = 'twitbot'
      email['To'] = 'all@devpayments.com'
      s = smtplib.SMTP('mail.authsmtp.com', 2525)
      s.login('ac46990', 'kurb5xgzy')
      #s.sendmail('twitbot', ['all@devpayments.com'], email.as_string())
      s.quit()

      #p.say(CHANNELS, email.as_string())
      p.say(CHANNELS, str(status))
