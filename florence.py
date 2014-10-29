import deck
import sys
import card
import pylab

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

def interactive_add():
  d = deck.Deck('default')

  print('\nPrinting the loaded deck...')
  d.printDeck(detailedFlag = False)

  d.interactiveAdd()

  print('\nPrinting the modified deck...')
  d.printDeck(detailedFlag = True)

  d.save()

def test(filename):
  d = deck.Deck(filename)

  # print('\nPrinting the loaded deck...')
  # d.printDeck(detailedFlag = False)

  print('Items to practice: ',end='')
  cardLimit = input()
  if cardLimit == '':
    # no limit used
    testList = d.getTestList()
  else:
    # assume the user provided a proper integer input
    testList = d.getTestList(int(cardLimit))
  print(testList)

  for item in testList:
    d.test(item)

  d.save('myDeck2.json')

def practice():
  # don't update the deck (training mode)
  pass

def analyze(filename):
  d = deck.Deck(filename)

  timesRemaining, levels = d.getStatistics()
  print(timesRemaining)
  pylab.hist(timesRemaining, 50, histtype='stepfilled')
  pylab.title('Testing Histogram')
  pylab.xlabel('Time Remaining')
  pylab.ylabel('Occurrences')

  pylab.figure()
  pylab.hist(levels, 50, histtype='stepfilled')
  pylab.title('Level Histogram')
  pylab.xlabel('Levels')
  pylab.ylabel('Occurrences')
  pylab.show()

if __name__ == '__main__':
  if len(sys.argv) < 2:
    print('Usage: p3 ./florence <operation>')
  else:
    op = sys.argv[1]
    if op == 'test':
      test(sys.argv[2])
    elif op == 'practice':
      practice()
    elif op == 'analyze':
      analyze(sys.argv[2])
    elif op == 'batch':
      programming_batch()
    elif op == 'interactive':
      interactive_add()
    else:
      print('%s is not a valid operation.'%(op))