import deck
import card
import matplotlib.pyplot as plt

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

def programming_batch():
  frontList = ['Travelling Salesman Problem','A* Search Algorithm','Djikstra\'s Shortest Path Algorithm', \
  'Linked List','Cycle Checking for Linked Lists','Binary Search','Bubble Sort','Selection Sort',\
  'Insertion Sort', 'Heapsort', 'Radix Sort','Mergesort','Quicksort','Fisher-Yates Shuffling']
  tags = ['programming']

  c = [card.Card(x,ref={},tags=tags) for x in frontList]
  d = deck.Deck()
  d.addCards(c)

  print("Printing the programming deck...")
  d.printDeck()

  d.save('pDeck.json')


def interactive_create():
  d = deck.Deck()
  d.interactiveAdd()
  d.interactiveAdd()

  print('\nPrinting the new deck...')
  d.printDeck(detailedFlag = True)

  d.save('myDeck.json')

def interactiveAdd():
  d = deck.Deck('default')

  print('\nPrinting the loaded deck...')
  d.printDeck(detailedFlag = False)

  d.interactiveAdd()

  print('\nPrinting the modified deck...')
  d.printDeck(detailedFlag = True)

  d.save()

def getTag(tagList):
  if not tagList:
    # deals with the empty case as well
    return None

  print('Filter by tag? ',end = '')
  ans = input()

  if ans == 'y':
    for i, tag in enumerate(tagList):
      print('%s - %s'%(i+1,tag))
    print('Selection: ',end = '')
    ans = input()
    print("'%s' tag selected.\n"%(tagList[int(ans)-1]))
    return tagList[int(ans)-1]
  else:
    return None

def test(filename):
  d = deck.Deck(filename)
  t = d.getTagList()

  tag_filter = getTag(t)

  print('Items to practice: ',end='')
  cardLimit = input()
  if cardLimit == '':
    # no limit used
    testList = d.getTestList(tag = tag_filter)
  else:
    # assume the user provided a proper integer input
    testList = d.getTestList(int(cardLimit),tag_filter)
  print(testList)

  for item in testList:
    qf = d.test(item)
    if qf:
      print('Aborting test session.')
      break

  d.save('myDeck.json')

def practice():
  # don't update the deck (training mode)
  pass

def analyze(filename):
  d = deck.Deck(filename)

  timesRemaining, levels = d.getStatistics()
  print(timesRemaining)
  plt.hist(timesRemaining, 50, histtype='stepfilled')
  plt.title('Testing Histogram')
  plt.xlabel('Time Remaining')
  plt.ylabel('Occurrences')

  plt.figure()
  plt.hist(levels, 50, histtype='stepfilled')
  plt.title('Level Histogram')
  plt.xlabel('Levels')
  plt.ylabel('Occurrences')
  plt.show()

if __name__ == '__main__':
  option_list = ['test','stats','interactive']
  print('Options:')
  for i, op in enumerate(option_list):
    print('%s - %s'%(i+1,op))
  print('> ',end='')
  user_input = int(input()) - 1
  print("'%s' selected.\n"%(option_list[int(user_input)-1]))
  filename = 'mewtwo.json'

  if option_list[user_input] == 'test':
    test(filename)
  elif option_list[user_input] == 'stats':
    analyze(filename)
  elif option_list[user_input] == 'interactive':
    interactiveAdd(filename)
  else:
    print('Invalid option selected.')

