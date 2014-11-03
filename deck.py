import json 
import time
import sys
import card

class Deck:
  # CONSTRUCTOR
  def __init__(self, filename = None):
    if filename:
      if filename == 'default':
        loaded = json.load(open('myDeck.json'))
      else:
        loaded = json.load(open(filename))
      self.cards = loaded['cards']
      self.tags = loaded['tags']
    else:
      self.cards = {}
      self.tags = {}

  def getCards(self, tag = None):
    if tag:
      filteredCards = {}
      for card in self.tags[tag]:
        filteredCards[card] = self.cards[card]
      return filteredCards
    else:
      return self.cards

  def getTags(self):
    return self.tags

  def convert(self):
    # temporary function for converting decks into the new format
    for cardFront in self.cards:
      if self.cards[cardFront]['tags']:
        for tag in self.cards[cardFront]['tags']:
          if tag not in self.tags:
            self.tags[tag] = [cardFront]
          else:
            self.tags[tag].append(cardFront)
    savePack = {'cards': self.cards, 'tags': self.tags}
    json.dump(savePack, fp = open('mewtwo.json','w'), indent = 4)

  # BASIC OPERATOR OVERLOADING
  def __contains__(self, key):
    return key in self.cards

  def __iter__(self):
    return self.cards.__iter__()

  def __getitem__(self,index):
    return self.cards[index]

  # ADDING CARDS TO THE DECK
  def _addCard(self, front, back):
    # helper function for deck insertion (front = key, back = value)
    curTime = time.time()
    if front not in self.cards:
      self.cards[front] = back
      metaDict = dict(added = curTime, lastTested = curTime, level = 0, interval = 0.0, efactor = 2.5)
      self.cards[front]['meta'] = metaDict

      # remove the tags from the card and move them to the tag dictionary
      for tag in self.cards[front].pop("tags", []):
        if tag not in self.tags:
          self.tags[tag] = [front]
        else:
          self.tags[tag].append(front)
    else:
      print('Card \'%s\' already in deck.'%(front))

  def addCards(self, cardsList):
    # given a list of cards, at them to the deck
    for card in cardsList:
      # iterate through the list of cards
      self._addCard(card.getFront(), card.getBack())
      print('Added card \'%s\' to deck.'%(card.getFront()))

  def interactiveAdd(self):
    # create a card interactively and then add it to the deck
    print('Front: ', end='') 
    front = input()

    print('Tag List: ', end='')
    tagString = input()
    # split by commas and remove additional whitespace
    tagList = [x.strip() for x in tagString.split(',')]

    newCard = card.Card(front = front, tags = tagList)

    # should probably add a confirmation here
    print("Confirm Card: '%s' with tags: %s" %(front, tagList))
    print('(y/n):',end = '')
    ans = input()
    if ans == 'y':
      self.addCards([newCard])

  def __add__(self, other):
    # needs testing
    # overloading for deck concatenation
    for key in other.getCards:
      # iterate through the keys in the other dictionary
      print('Key: %s'%(key))
      self._addCard(key, other[key]) 

    otherTags = other.getTags()
    for tag in otherTags:
      # iterate through all the tags in the dictionary
      for taggedCard in otherTags:
        # iterate through all of the cards in each tag list
        if tag not in self.tags:
          self.tags[tag] = [cardFront]
        else:
          if taggedCard not in self.tags[tag]:
            self.tags[tag].append(cardFront)
    return self

  def replace(self, replacement):
    pass

  # SAVING
  def save(self, filename = 'myDeck.json'):
    savePack = {'cards':self.getCards(), 'tags':self.getTags()}
    json.dump(savePack, fp = open(filename,'w'), indent = 4)

  def export(self):
    pass

  # ACCESSORS AND MUTATORS
  def intervalExceeded(self, key):
    return self.getSecondsSinceTest(key) > self[key]['meta']['interval']

  def getSecondsSinceTest(self, key):
    curTime = time.time()
    cardBack = self[key]
    timeSince = curTime - cardBack['meta']['lastTested']
    return timeSince

  def getSecondsUntilTest(self, key):
    curTime = time.time()
    cardBack = self[key]
    timeSince = curTime - cardBack['meta']['lastTested']
    return cardBack['meta']['interval'] - timeSince

  def getLevel(self, key):
    return self[key]['meta']['level']

  def setMeta(self, cardKey, meta):
    # meta is dicionary containing values to be modified
    for key in meta.keys():
      self.cards[cardKey]['meta'][key] = meta[key]

  # TESTING AN INDIVIDUAL CARD
  def test(self, key):
    print('\nFront: %s' %(key))
    print('Hours since last test: %.2f' %(self.getSecondsSinceTest(key)/3600))
    
    recall = input('Enter level: ')

    if recall == 's':
      print("Skipped.")
      return False
    elif recall == 'q':
      return True
    else:
      recall = int(recall)

    newMeta = {}

    # concept level adjustment
    if recall < 3:
      # unsuccessful recall, reset to level 1
      newMeta['level'] = 1
    else:
      # successful recall, incremement the level
      newMeta['level'] = self[key]['meta']['level'] + 1

    # easiness factor adjustment
    oldEF = self[key]['meta']['efactor']
    newEF = oldEF - 0.8 + 0.28 * recall - 0.02 * recall ** 2
    if newEF > 2.5:
      newEF = 2.5
    elif newEF < 1.3:
      newEF = 1.3
    newMeta['efactor'] = newEF

    # setting the new interval
    oldInterval = self[key]['meta']['interval']
    if self[key]['meta']['level'] > 2:
      newInterval = oldInterval * newEF
    elif self[key]['meta']['level'] == 2:
      newInterval = 6 * 24 * 60 * 60 # six days seconds
    else:
      newInterval = 24 * 60 * 60 # one day in seconds
    newMeta['interval'] = newInterval

    # updating the lastTested field
    newMeta['lastTested'] = time.time()

    self.setMeta(key, newMeta)
    return False

  # CARD SET RETRIEVAL
  def getTestList(self, cardLim = None, tag = None):
    
    # get all of the cards with the correct tag
    taggedCards = self.getCards(tag)
    testList = [] # to be returned

    # figure out the upper limit on the cards to practice
    if not cardLim:
      cardsRemaining = sys.maxsize # very large value
    else:
      cardsRemaining = cardLim

    # iterate through all of the cards in the taggedCards dictionary
    for key in taggedCards:
      if cardsRemaining <= 0:
        # card limit reached
        break
      if self.intervalExceeded(key):
        # card is due to be tested
        testList.append(key)
        cardsRemaining -= 1
    return testList

  def getPracticeList(self):
    pass

  # DECK ANALYTICS
  def printDeck(self, detailedFlag = False):
    c = self.cards
    for key in c:
      print('Front: %s' %(key))
      if detailedFlag:
        print(c[key],'\n')

  def getStatistics(self, tag = 'programming'):
    timesRemaining = [] # create a list of the times remaining
    levels = [] # create a list of the levels for the cards
    
    # get all of the cards with the correct tag
    taggedCards = self.getCards(tag)

    # iterate through the tagged cards
    for key in taggedCards:
      hours = self.getSecondsUntilTest(key) / (60*60)
      timesRemaining.append(hours)
      levels.append(self.getLevel(key))

    return (timesRemaining, levels)

