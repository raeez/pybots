from pybot import Pybot
import smtplib
from email.mime.text import MIMEText
from twitter import Twitter, OAuth

HOST = "comm.devpayments.com"
CHANNELS = ["#pcilevelonecompliant", "#pcileveltwocompliant"]

p = Pybot(HOST, nick='twitbot')
p.join(CHANNELS)

CONSUMER_KEY = 'FRzVzZs0SSyWgPsR9mxiQw'
CONSUMER_SECRET = 'eoPZSrScusq6gdc33AkPek9nlPYCzuKjPBlGDt91wA'
ACCESS_KEY = '207769300-XNu6GdcoQNP1bRJUDlgQ1PmAgYFQQqqpNFzLDcML'
ACCESS_SECRET = 'CclHmsRsAhGUZ5toATnLdZVl3WBrPq0RNSiIzUKTGJo'

twitter = Twitter(auth=OAuth(ACCESS_KEY, ACCESS_SECRET, CONSUMER_KEY, CONSUMER_SECRET))

while True:
  for msg in p.fetch():

    if msg.channel in CHANNELS and msg.content.find("status") != -1 and msg.content.find("twitbot:") != -1:

      statuses = twitter.statuses.friends_timeline(id="twitbot_")
      email_text = ''
      devpay_matrix = {}
      for s in statuses:
        if devpay_matrix.has_key(s['user']['screen_name']) is False:
          devpay_matrix[s['user']['screen_name']] = s['text']
      for u in devpay_matrix:
        email_text += u + ':\t ' + devpay_matrix[u] + '\n\n'
        p.say(msg.channel, u + ': ' + devpay_matrix[u])

      email = MIMEText(email_text)
      email['Subject'] = 'twitbot reporting for duty'
      email['From'] = 'twitbot@devpayments.com'
      email['To'] = 'all@devpayments.com'
      s = smtplib.SMTP('mail.authsmtp.com', 2525)
      s.login('ac46990', 'kurb5xgzy')
      s.sendmail('twitbot@devpayments.com', ['all@devpayments.com'], email.as_string())
      s.quit()
