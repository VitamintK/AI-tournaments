import random

class Card():
    a_high = True
    suit_ord = ['D', 'C', 'H', 'S']
    trans_dict = ['A'] + [str(i) for i in range(2,10)] + ['T','J','Q','K']
    def __init__(self, rank: int, suit: str):
        self.rank = rank
        self.suit = suit
    def __str__(self):
        return Card.trans_dict[self.rank - 1] + str(self.suit)
    def __repr__(self):
        return str(self)
    def __gt__(self, other):
        return self.rank > other.rank or (self.rank == other.rank and
                                          Card.suit_ord.index(self.suit) > Card.suit_ord.index(other.suit))
    def __eq__(self, other):
        return self.rank == other.rank and self.suit == other.suit
    def rev_trans(prank):
        return Card.trans_dict.index(prank) + 1
    def pretty_to_card(pretty):
        try:
            pr, ps = pretty
            return Card(Card.rev_trans(pr), ps)
        except ValueError:
            if pretty in Card.suit_ord:
                return Part_Card(suit = pretty)
            else:
                return Part_Card(rank = Card.rev_trans(pretty))

class Part_Card(Card):
    def __init__(self, rank = None, suit = None):
        self.rank = rank
        self.suit = suit
    def __eq__(self, other):
        if self.rank:
            return self.rank == other.rank
        elif self.suit:
            return self.suit == other.suit

class Cards():
    def __init__(self, cards):
        self.cards = cards
    def remove(self, cards):
        rmvd = []
        crdcopy = self.cards[:]
        for i in cards:
            for j in crdcopy:
                if j == i:
                    crdcopy.remove(i)
                    rmvd.append(j)
                    break
            else:
                raise KeyError("{} not found in {}".format(i, self.cards))
        self.cards = crdcopy
        return rmvd
    def pop_n(self,n):
        """returns and deletes the initial n cards"""
        popped = self.cards[:n]
        del self.cards[:n]
        return Cards(popped)
    def shuffle(self):
        random.shuffle(self.cards)
    def __len__(self):
        return len(self.cards)
    def __str__(self):
        return str(self.cards)
    def __iter__(self):
        return (i for i in self.cards)

class Deck(Cards):
    def __init__(self):
        self.cards = [Card(i,j) for i in range(1,14) for j in ['D','C','H','S']]

class Player():
    def __init__(self, cards: Cards):
        self.cards = cards
    def pretty_str(self):
        return ' '.join([str(i) for i in sorted(self.cards)])
    def __len__(self):
        return len(self.cards)
    def __str__(self):
        return "{} <- size {}".format(self.cards, len(self.cards))
    def move(self):
        pass
    def call_bs(self, play):
        pass

class Human(Player):
    def move(self):
        while True:
            print('---')
            print("It is now your turn to play {}s.".format(Card.trans_dict[turn_rank-1]))
            play_cards = input("Which of these cards {} do you play?\n".format(self.pretty_str())).upper()
            play_cards = Cards([Card.pretty_to_card(i) for i in play_cards.split()])
            try:
                assert len(play_cards) >= 1
                return self.cards.remove(play_cards)
            except Exception as e:
                print ('Those are not proper cards values.  Example of proper values is: Ac 4d Kd')
                #raise e
    def call_bs(self, play):
        pass

def i2s(i:int):
    try:
        return ['no', 'one', 'two', 'three', 'four', 'five', 'six'][i]
    except:
        return i
    
 
deck = Deck()
deck.shuffle()
#(deck)

player_amount = 3
hand_size = len(deck)//player_amount
players = [Human(deck.pop_n(hand_size)) for i in range(3)]
winner = False
turn_player = players[0]
turn_rank = 1
while not winner:
    player_index = players.index(turn_player)
    player_cards = turn_player.move()
    print("Player {} played {} {}{}".format(player_index, i2s(len(player_cards)), Card.trans_dict[turn_rank-1], 's'*(len(player_cards) > 1)))
    for player in [p for p in players if p != turn_player]:
        player.call_bs(len(player_cards))
    
    turn_player = players[(player_index + 1)%len(players)]
    turn_rank = (turn_rank + 1)%13
    
print(players)
