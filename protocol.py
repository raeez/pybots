class IRC:
  # TODO write a smart parser: collapses returned items into line structs
  @classmethod
  def getContent(cls, channel, item):
    parts = item.split("PRIVMSG " + channel + " :")
    print item, repr(parts)
    if len(parts) > 1:
      return parts[1].rstrip()
    else:
      return ""


  @classmethod
  def getUser(cls, item):
    parts = item.split("!")
    if len(parts) > 0:
      return parts[0][1:]
    else:
      return ""
