class IRC:

  @classmethod
  def getContent(cls, item):
    if item.find("PRIVMSG") == -1:
      return ""

    parts = item.split(" :")
    return parts[len(parts)-1].rstrip()

  @classmethod
  def getChannel(cls, item):
    if item.find("PRIVMSG") == -1:
      return ""

    parts = item.split("#")
    channel = "#"
    for character in parts[1]:
      if character == ' ':
        break
      else:
        channel += character
    return channel

  @classmethod
  def getUser(cls, item):
    if item.find("PRIVMSG") == -1:
      return ""

    parts = item.split("!")
    if len(parts) > 0:
      return parts[0][1:]
    else:
      return ""
