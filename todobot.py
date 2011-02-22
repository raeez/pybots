from pybot import Pybot

HOST = "comm.secretsite.com"
CHANNELS = ["#pcilevelonecompliant", "#pcileveltwocompliant", "#general"]

p = Pybot(HOST, nick="todobot")
p.join("#general")

#create a new pybot : Pybot(hostname, port=394024, nick='somenick'
#tell pybot to join a channel: p.join("#channelname")
#fetch available messages : p.fetch() ----> [msg, msg, msg, msg]
#say something in a particular channel : p.say("#channelgoeshere", "thing to say goes here")

FILENAME = 'todobot.data'

class TodoList:
  def __init__(self):
    self.file = open(FILENAME, 'r')
    items = self.file.readlines()
    if len(items) > 0:
      self.items = [f.rstrip() for f in items]
    else:
      self.items = []
    self.file.close()

  def save(self):
    self.file = open(FILENAME, 'w')
    for i in self.items:
      print >>self.file, i
    self.file.close()
  
  def add(self, i):
    self.items.append(i)
    self.save()

  def remove(self, i):
    if i > len(self.items)-1:
      raise IndexError
    del self.items[i]
    self.save()

todo = TodoList()

while True:
  for msg in p.fetch():
    #msg is an object that represents a single user's message sent to the server
    #msg.channel
    #msg.content
    #msg.user

    if msg.channel in CHANNELS:
      if msg.content.find("todobot:") != -1:

        if msg.content.find("list") != -1:
          p.say(msg.channel, "Todo list:")
          for i,thing in enumerate(todo.items):
            p.say(msg.channel, "%d: %s" % (i,thing))

        elif msg.content.find("add") != -1:
          index_of_add_cmd = msg.content.find("add ")
          thing_to_add = msg.content[index_of_add_cmd + len("add "):]
          todo.add(thing_to_add)

          p.say(msg.channel,"Added item %s" % thing_to_add)

        elif msg.content.find("done") != -1:
          number = -1
          try:
            number = int(msg.content.split("done ")[1].rstrip())
            item = todo.items[number]
            print 'got number %d out of %d which is %s' % (number, len(todo.items), todo.items[number])
            todo.remove(number)
            p.say(msg.channel, "Removed item %s" % item)
            continue
          except:
            p.say(msg.channel, "Don't understand which item you want me to remove!!")
            continue
