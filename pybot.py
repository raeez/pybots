import socket
from protocol import IRC

class Pybot:
  def __init__(self, host, port=6667, nick="pybot"):
    print "Creating Pybot: %s@%s" % (nick, host)
    self.conn = socket.socket()
    self.conn.connect((host, port))
    self.conn.send("NICK %s\r\n" % nick)
    self.conn.send("USER %s %s bla :%s\r\n" % (nick, nick, nick))
    
    self.readbuffer = ""

    self.joined = {}

  def pong(self, server):
    print "sending a pong! %s" % server
    self.conn.send("PONG %s \r\n" % server)

  def _join(self, channel):
    self.conn.send("JOIN %s \r\n" % channel)
    self.joined[channel] = 1

  def join(self, channel):
    if isinstance(channel, str):
      self._join(channel)
    if isinstance(channel, list):
      for c in channel:
        self._join(c)

  def _post(self, channel, msg):
    content = "PRIVMSG " + channel + " :" + str(msg).rstrip() + "\r\n"
    self.conn.send(content)

  def say(self, channel, msg):
    if isinstance(channel, str):
      self._post(channel, msg)

    if isinstance(channel, list):
      for c in channel:
        self._post(c, msg)
      
  def _fetch(self, bytes=4096):
    self.readbuffer = self.readbuffer + self.conn.recv(bytes)
    lines = self.readbuffer.split("\n")
    self.readbuffer = lines.pop()

    print self.readbuffer, lines
    return lines

  def fetch(self, bytes=4096):
    lines = self._fetch(bytes)

    class Message:
      pass

    messages = []
    for l in lines:
      if IRC.isPing(l):
        self.pong(IRC.pingServer(l))
        continue
      m = Message()
      m.user = IRC.getUser(l)
      m.content = IRC.getContent(l)
      m.channel = IRC.getChannel(l)
      messages.append(m)
    return messages
