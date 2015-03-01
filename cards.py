import random

class Card():
    a_high = True
    suit_ord = ['D', 'C', 'H', 'S']
    def __init__(self, rank: int, suit: str):
        self.rank = rank
        self.suit = suit
    def __str__(self):
        trans_dict = ['A'] + [str(i) for i in range(2,10)] + ['T','J','Q','K']
        return trans_dict[self.rank - 1] + self.suit
    def __gt__(self, other):
        return self.rank > other.rank or (self.rank == other.rank and
                                          Card.suit_ord.index(self.suit) > Card.suit_ord.index(other.suit))
    def __eq__(self, other):
        return self.rank == other.rank and self.suit == other.suit

class Player():
    def __init__(self, hand):
        self.hand = hand
    def pretty_str(self):
        return ' '.join([str(i) for i in sorted(self.hand)])
    def __str__(self):
        return "{} <- size {}".format(self.hand, len(self.hand))
    def move(self):
        pass

class Human(Player):
    def move(self):
        play_cards = input("Which of these cards {} do you play?".format(self.pretty_str()))
        return 0,0

deck = [Card(i,j) for i in range(1,14) for j in ['D','C','H','S']]
random.shuffle(deck)
#(deck)

player_amount = 3
hand_size = len(deck)//player_amount
players = [Human(deck[:hand_size]) for i in range(3)]
winner = False
turnplayer = players[0]
while not winner:
    player_cards, player_claim = turnplayer.move()
    break
    
print(players)
