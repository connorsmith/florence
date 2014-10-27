class Card:
  def __init__(self, front, ref = {}, tags = [], meta = {}):
    self.cardFront  = cardFront(front)
    self.cardBack   = cardBack(ref, tags, meta)

  def getFront(self):
    return self.cardFront.getFront()

  def getBack(self):
    return self.cardBack.getBack()

  def __str__(self):
    return '<%s> tagged as %s' % (self.front,self.back['tags']) 

class cardBack:
  def __init__(self, ref = {}, tags = [], meta = {}):
    self.back = {}
    self.back['ref']  = ref
    self.back['tags'] = tags
    self.back['meta'] = meta

  def getBack(self):
    return self.back

  def setMeta(self, key, value):
    self.back['meta'][key] = value

class cardFront:
  def __init__(self, front):
    self.front = front

  def getFront(self):
    return self.front

