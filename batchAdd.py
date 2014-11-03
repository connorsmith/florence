import deck
import card

# select the deck these cards are to be added to
d1 = deck.Deck('mew.json')

# put all of the cards here
cardFronts = ["Newton's Law of Universal Gravitation",'Kinetic Energy']

# put all of the tags here (the same for all cards)
tagSet = ['physics']

cardList = [card.Card(front,{},tagSet) for front in cardFronts]
d1.addCards(cardList)

# choose where to save the deck
d1.save('mewtwo.json')
