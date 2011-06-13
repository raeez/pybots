from pybot import Pybot
from os import mkdir
from os import popen
import logging
import logging.handlers
import re

HOST = "localhost"
CHANNELS = ["#somechannel"]
BOTNICK = "logbot"

p = Pybot(HOST, nick='logbot')
p.join(CHANNELS)

LOG = True

MAIL_HOST = ''
FROM_ADDR = ''
TO_ADDR = ''
SUBJECT = ''
MAIL_ADMINS = ['admin@domain.com']

class Logger(dict):
  """docstring for Logger"""
  def __init__(self, system_name):
    super(Logger, self).__init__()

    self.system_name = str(system_name)
    try:
      mkdir('log')
    except OSError:
      pass # directory exists

    self.filename = 'log/' + self.system_name + '.log'
    
    #formatters
    self.email_formatter = logging.Formatter('''
              Message type:       %(levelname)s
              Location:           %(pathname)s:%(lineno)d
              Module:             %(module)s
              Function:           %(funcName)s
              Time:               %(asctime)s

              Message:

              %(message)s
              ''')
    self.file_formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")

    #handlers
    self.handlers = []

    self.file_handler = logging.handlers.RotatingFileHandler(self.filename, maxBytes=1000000000, backupCount=5)
    self.file_handler.setLevel(logging.DEBUG)
    self.file_handler.setFormatter(self.file_formatter)
    self.handlers.append(self.file_handler)

    self.email_handler = logging.handlers.SMTPHandler(MAIL_HOST, FROM_ADDR, MAIL_ADMINS, SUBJECT)
    self.email_handler.setLevel(logging.ERROR)
    self.email_handler.setFormatter(self.email_formatter)
    #self.handlers.append(self.email_handlers) #TODO get the mail server up and running

    self.create_logger('system')
    self['system'].info('Created an instance of Logger!')

  def create_logger(self, logname):
    new_logger = logging.getLogger(logname)
    new_logger.setLevel(logging.DEBUG)
  
    for h in self.handlers:
      new_logger.addHandler(h)

    self[logname] = new_logger

  def add_logger(self, logname, logger):
    logger.setLevel(logging.DEBUG)

    for h in self.handlers:
      logger.addHandler(h)

    self[logname] = logger

log = Logger('logbot')

p.say(CHANNELS, "logbot reporting for duty!")

while True:
  for msg in p.fetch():
    if msg.channel in CHANNELS:
      if re.search('%s:' % BOTNICK, msg.content, flags=re.IGNORECASE):

        if re.search('mode', msg.content, flags=re.IGNORECASE):
          if LOG is True:
            p.say(msg.channel, "watching your every move...")
          else:
            p.say(msg.channel, "turning a blind eye...")
          continue

        elif re.search('public', msg.content, flags=re.IGNORECASE):
          LOG = True
          p.say(msg.channel, "logbot logging on")
          continue

        if re.search('private', msg.content, flags=re.IGNORECASE):
          LOG = False
          p.say(msg.channel, "logbot logging off. Do your illegal things!")
          continue

        res = re.search('query=\d+', msg.content, flags=re.IGNORECASE)
        if res:
          query = int(res.group(0).split('=')[1])
          logdata = popen('tail -' + str(query) +' log/logbot.log').read()
          p.say(msg.user, logdata)
          continue

      if LOG:
        log['system'].info("[%s] %s:\t%s" % (msg.channel, msg.user, msg.content))
      
      #someone said something in our channel, log it!
