import deck
import card
import matplotlib.pyplot as plt
import pprint
import datetime
import time 

def batch_create():
  c1 = card.Card('Forging',{},['me548','mech'])
  c2 = card.Card('Partial Fractions (Cover-up)',{},['me597','controls'])
  c3 = card.Card('Ringworld, publication year',{},[])

  d1 = deck.Deck()  
  d1.addCards([c1, c2])

  print('\nPrinting the first deck...')
  d1.printDeck(detailedFlag = True)

  d2 = deck.Deck()
  d2.addCards([c3])

  print('\nPrinting the second deck...')
  d2.printDeck(detailedFlag = True)


  d = d1 + d2
  print('\nPrinting the combined deck...')
  d.printDeck(detailedFlag = True)

  d.save()

def interactive_create():
  d = deck.Deck()
  d.interactiveAdd()
  d.interactiveAdd()

  print('\nPrinting the new deck...')
  d.printDeck(detailedFlag = True)

  d.save('myDeck.json')

def interactiveInsertion(filename):
  d = deck.Deck(filename)

  addFlag = True

  while addFlag:
    d.interactiveAdd()

    print("Add another? ",end = '')
    ans = input()
    if ans != 'y':
      addFlag = False

  d.save(filename)

def tagPrompt(tagList):
  # prompt the user to select a tag from the list
  
  if not tagList:
    # deals with the empty case
    return None

  print('Filter by tag? ',end = '')
  ans = input()

  if ans == 'y':
    tagList.sort() # alphabetically
    for i, tag in enumerate(tagList):
      print('%s) %s'%(i+1,tag))
    print('Selection: ',end = '')
    ans = input()
    print("'%s' tag selected.\n"%(tagList[int(ans)-1]))
    return tagList[int(ans)-1]
  else:
    return None

def test(filename):
  d = deck.Deck(filename)
  t = d.getTagList()

  tag_filter = tagPrompt(t)

  cardLimit = ''
  if cardLimit == '':
    # no limit used
    testList = d.getTestList(tag = tag_filter)
  else:
    # assume the user provided a proper integer input
    testList = d.getTestList(int(cardLimit),tag_filter)
  
  if not testList:
    print('No items require testing.')
    return # no saving required

  testedCount = 0
  for item in testList:
    qf = d.test(item)
    if qf:
      print('Ending test session. %d items reviewed!'%(testedCount))
      break
    testedCount += 1

  # overwrite the working copy
  d.save(filename)
  # also save as a timestamped backup
  timeVal = time.time()
  timeStamp = datetime.datetime.fromtimestamp(timeVal).strftime('%Y%m%d')
  fileParts = filename.split('.')
  fileParts[0] += '-' + timeStamp
  tsFilename = 'backups/'+fileParts[0]+'.'+fileParts[1]
  d.save(tsFilename)

def practice():
  # don't update the deck (training mode)
  pass

def analyze(filename):
  d = deck.Deck(filename)

  timesRemaining, levels = d.getStatistics()

  plt.hist(timesRemaining, 50, histtype='stepfilled')
  plt.title('Testing Histogram')
  plt.xlabel('Time Remaining')
  plt.ylabel('Occurrences')

  plt.figure()
  width = 0.2

  # indices and value lists for the cards past the testing point
  needsTestingIdx = []
  needsTestingVals = []
  # indices and value lists for th cards which don't need testing yet
  notYetIdx = []
  notYetVals = []

  # access the sub-dictionary for cards requiring testing
  levelSection = levels['toBeTested']
  for lev in levelSection:
    needsTestingIdx.append(lev-width)
    needsTestingVals.append(levelSection[lev])
  # access the sub-dictionary for cards not requireing testing
  levelSection = levels['notYet']
  for lev in levels['notYet']:
    notYetIdx.append(lev+width)
    notYetVals.append(levelSection[lev])

  p1 = plt.bar(needsTestingIdx,needsTestingVals, width = width, align='center',color='r',label='Active')
  p2 = plt.bar(notYetIdx,notYetVals, width = width, align='center',color='b',label='Dormant')
  plt.title('Level Distribution')
  plt.xlabel('Levels')
  plt.ylabel('Occurrences')
  plt.show()

def deckPrint(filename):
  d = deck.Deck(filename)
  t = d.getTagList()

  tag_filter = tagPrompt(t)

  if tag_filter:
    t_dict = d.getTags()
    pprint.pprint(t_dict[tag_filter])
  else:
    pprint.pprint(d.getCardList())

if __name__ == '__main__':
  option_list = ['test','stats','interactive','print']
  print('Options:')
  for i, op in enumerate(option_list):
    print('%s) %s'%(i+1,op))
  print('> ',end='')
  user_input = int(input()) - 1
  print("'%s' selected.\n"%(option_list[int(user_input)]))
  filename = 'mewtwo.json'

  if option_list[user_input] == 'test':
    test(filename)
  elif option_list[user_input] == 'stats':
    analyze(filename)
  elif option_list[user_input] == 'interactive':
    interactiveInsertion(filename)
  elif option_list[user_input] == 'print':
    deckPrint(filename)
  else:
    print('Invalid option selected.')

