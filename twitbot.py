from pybot import Pybot
import smtplib
from email.mime.text import MIMEText
from twitter import Twitter, OAuth

HOST = "comm.secretsite.com"
CHANNELS = ["#pcilevelonecompliant", "#pcileveltwocompliant"]

p = Pybot(HOST, nick='twitbot')
p.join(CHANNELS)

CONSUMER_KEY = 'V'
CONSUMER_SECRET = 'X'
ACCESS_KEY = 'Y'
ACCESS_SECRET = 'Z'

twitter = Twitter(auth=OAuth(ACCESS_KEY, ACCESS_SECRET, CONSUMER_KEY, CONSUMER_SECRET))

while True:
  for msg in p.fetch():

    if msg.channel in CHANNELS and msg.content.find("status") != -1 and msg.content.find("twitbot:") != -1:

      statuses = twitter.statuses.friends_timeline(id="twitbot_")
      email_text = ''
      matrix = {}
      for s in statuses:
        if matrix.has_key(s['user']['screen_name']) is False:
          matrix[s['user']['screen_name']] = s['text']
      for u in matrix:
        email_text += u + ':\t ' + matrix[u] + '\n\n'
        p.say(msg.channel, u + ': ' + matrix[u])

      email = MIMEText(email_text)
      email['Subject'] = 'twitbot reporting for duty'
      email['From'] = 'twitbot@someplace.com'
      email['To'] = 'people@someplace.com'
      s = smtplib.SMTP('mail.authsmtp.com', 2525)
      s.login(USER, PASS)
      s.sendmail('twitbot@someplace.com', ['all@someplace.com'], email.as_string())
      s.quit()
