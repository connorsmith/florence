import json 
import time
import card
import webbrowser
from random import randint

from sys import maxsize

def getResponse(restrictToInt = False):
  while True:
    try:
      if restrictToInt:
        print('Enter level: ',end='')
      else:
        print('Enter level or command: ',end='')
      response = input()

      if not restrictToInt and response in ['s','r','q','d']:
        return response
      else:
        return int(response)

    except ValueError:
      if restrictToInt:
        print("Valid inputs are integers in [0,5].")
      else:
        print("Valid inputs are 's','r','q','d', or [0,5].")

class Deck:
  # CONSTRUCTOR
  def __init__(self, filename = None):
    if filename:
      if filename == 'default':
        loaded = json.load(open('mewtwo.json'))
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

  def getCardList(self):
    return list(self.cards.keys())

  def getTags(self):
    return self.tags

  def getTagList(self):
    return list(self.tags.keys())

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

    print('Ref Field: ', end='')
    refString = input()
    if refString:
      # answer was provided, ask if it was a url or a ref
      print("Press Enter if 'url', or 'r' for 'ref': ",end='')
      refType = input()
      if refType:
        refDict = {'ref':refString}
      else:
        refDict = {'url':refString}
    else:
      # empty by default
      refDict = {}
    newCard = card.Card(front = front, tags = tagList, ref = refDict)

    # should probably add a confirmation here
    print("Confirm Card: '%s' with tags: %s" %(front, tagList))
    print('(y/n): ',end = '')
    ans = input()
    if ans == 'y':
      self.addCards([newCard])
    else:
      print('Cancelled.')

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
  def save(self, filename = 'mewtwo.json'):
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

  def showReference(self, key):
    cardBack = self[key]
    if not cardBack['ref']:
      print('No reference information to display.')
    else:
      if 'ref' in cardBack['ref']:
        print(cardBack['ref']['ref'])
      elif 'url' in cardBack['ref']:
        webbrowser.open_new_tab(cardBack['ref']['url'])
      elif 'png' in cardBack['ref']:
        print('.png file found.')
      else:
        print('Unknown ref format(s): %s'%(list(cardBack['ref'].keys())))

  def deleteCard(self, key):
    # remove the card from the card list
    print("Enter 'y' to confirm deletion: ",end = '')
    confirmationString = input()

    if confirmationString != 'y':
      print('Delete cancelled.')
      return

    del self.cards[key]

    # remove the card from the tag lists
    tagDeletionList = [] # supports the removal of tags
    for tagList in self.tags:
      if key in self.tags[tagList]:
        self.tags[tagList].remove(key)
        if self.tags[tagList] == []:
          tagDeletionList.append(tagList)

    # remove the tags that no longer have any associated cards
    for tagToRemove in tagDeletionList:
      del self.tags[tagToRemove]

    print('Card successfully deleted.')

  # TESTING AN INDIVIDUAL CARD
  def test(self, key):
    print('\nFront: %s' %(key))
    print('Hours past due: %.2f' %(self.getSecondsUntilTest(key)/(-3600)))
    
    response = getResponse(restrictToInt = False)

    if response == 's':
      print("Skipped.")
      return False
    elif response == 'd':
      self.deleteCard(key)
      return False
    elif response == 'q':
      return True
    elif response == 'r':
      # display reference information
      self.showReference(key)
      response = getResponse(restrictToInt = True)

    newMeta = {}

    # concept level adjustment
    if response < 3:
      # unsuccessful recall, reset to level 1
      newMeta['level'] = 1
    else:
      # successful recall, incremement the level
      newMeta['level'] = self[key]['meta']['level'] + 1

    # easiness factor adjustment
    oldEF = self[key]['meta']['efactor']
    newEF = oldEF - 0.8 + 0.28 * response - 0.02 * response ** 2
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
      newInterval = 6 * 24 * 60 * 60 # six days in seconds
    else:
      newInterval = 24 * 60 * 60 # one day in seconds
    intervalRandomness = randint(-600,600) # +/- 10 minutes
    newMeta['interval'] = newInterval + intervalRandomness

    # updating the lastTested field
    newMeta['lastTested'] = time.time()

    self.setMeta(key, newMeta)
    return False

  # CARD SET RETRIEVAL
  def getTestList(self, cardLim = None, tag = None):
    
    # get all of the cards with the correct tag
    taggedCards = self.getCards(tag)
    testDict = {} # holds the cards and the time past the test point

    # figure out the upper limit on the cards to practice
    if cardLim == None:
      cardsRemaining = maxsize # very large value
    else:
      cardsRemaining = cardLim

    # iterate through all of the cards in the taggedCards dictionary
    for key in taggedCards:
      if cardsRemaining <= 0:
        # card limit reached
        break
      # get the time relative to the testing point
      timeToInterval = self.getSecondsUntilTest(key)
      if timeToInterval < 0:
        # card is due to be tested (past the testing point)
        testDict[key] = timeToInterval
        cardsRemaining -= 1

    # return a list of keys sorted by how far past their test points they are
    return sorted(testDict,key=testDict.__getitem__)

  # DECK ANALYTICS
  def printDeck(self, detailedFlag = False):
    c = self.cards
    for key in c:
      print('Front: %s' %(key))
      if detailedFlag:
        print(c[key],'\n')

  def getStatistics(self, tag = None):
    timesRemaining = [] # create a list of the times remaining
    levels = {'toBeTested':{},'notYet':{}}
    
    # get all of the cards with the correct tag
    taggedCards = self.getCards(tag)

    # iterate through the tagged cards
    for key in taggedCards:
      cardLevel = self.getLevel(key)

      hours = self.getSecondsUntilTest(key) / (60*60)
      timesRemaining.append(hours)

      if hours < 0:
        levelKey = 'toBeTested'
      else:
        levelKey = 'notYet'

      if cardLevel in levels[levelKey]: 
        levels[levelKey][cardLevel] += 1
      else:
        levels[levelKey][cardLevel] = 1

    return (timesRemaining, levels)

