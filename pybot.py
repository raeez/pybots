import socket
from protocol import IRC

class Pybot:
  def __init__(self, host, port=6667, nick="pybot"):
    print "Creating Pybot: %s@%s"
    self.conn = socket.socket()
    self.conn.connect((host, port))
    self.conn.send("NICK %s\r\n" % nick)
    self.conn.send("USER %s %s bla :%s\r\n" % (nick, nick, nick))
    
    self.readbuffer = ""

    self.joined = {}

  def join(self, channel):
    self.conn.send("JOIN %s \r\n" % channel)
    self.joined[channel] = 1

  def say(self, channel, msg):
    content = "PRIVMSG " + channel + " :" + str(msg).rstrip() + "\r\n"
    self.conn.send(content)

  def fetch(self, bytes=4096):

    lines = self.fetch_raw(bytes)

    class Message:
      pass

    messages = []
    for l in lines:
      m = Message()
      m.user = IRC.getUser(l)
      m.content = IRC.getContent(l)
      m.channel = IRC.getChannel(l)
      messages.append(m)
    return messages

  def fetch_raw(self, bytes=4096):
    self.readbuffer = self.readbuffer + self.conn.recv(bytes)
    lines = self.readbuffer.split("\n")
    self.readbuffer = lines.pop()

    print self.readbuffer, lines

    return lines
