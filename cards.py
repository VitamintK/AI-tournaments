import random

"""BS"""


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
    def __init__(self, cards = None):
        if cards == None:
            self.cards = []
        else:
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
        return Cards(rmvd)
    def pop_n(self,n = 1):
        """returns and deletes the initial n cards"""
        popped = self.cards[:n]
        del self.cards[:n]
        return Cards(popped)
    def count(self, rank = None, suit = None):
        return len([card for card in self.cards if (not rank or card.rank == rank) and (not suit or card.suit == suit)])
    def shuffle(self):
        random.shuffle(self.cards)
    #def extend(self, cards:Cards):
    #    self.cards.extend(cards.cards)
    def __len__(self):
        return len(self.cards)
    def __str__(self):
        return str(self.cards)
    def __iter__(self):
        return (i for i in self.cards)
    def __add__(self, other):
        if isinstance(other, Cards):
            return Cards(self.cards + other.cards)
        elif isinstance(other, Card):
            return Cards(self.cards + [other])
        else:
            raise TypeError

class Deck(Cards):
    def __init__(self):
        self.cards = [Card(i,j) for i in range(1,14) for j in ['D','C','H','S']]

class Player():
    def __init__(self, cards: Cards, title = None):
        if title == None:
            self.title = random.choice(["Adam","Bob","Chris","Dude"])
        else:
            self.title = title
        self.cards = cards
    def pretty_str(self):
        return ' '.join([str(i) for i in sorted(self.cards)])
    def __len__(self):
        return len(self.cards)
    def __str__(self):
        return self.title
    def move(self):
        #should this be a function of turn_rank?
        pass
    def call_bs(self, play, turn_rank):
        pass

class Human(Player):
    def move(self):
        #this should be a function of turn_rank?
        while True:
            print('---')
            print("It is now your turn to play {}s.".format(Card.trans_dict[turn_rank-1]))
            play_cards = input("Which of these cards {} do you play?\n".format(self.pretty_str())).upper()
            try:
                play_cards = Cards([Card.pretty_to_card(i) for i in play_cards.split()])
            except ValueError:
                print('These are not proper cards values.  Proper values are: a a 2')
                continue
            try:
                assert len(play_cards) >= 1
                return self.cards.remove(play_cards)
            except Exception as e:
                print ("You don't have those cards or you tried playing nothing.")
                #raise e
    def call_bs(self, play, turn_rank):
        bs = input("Call BS?  [y/n] ")
        if bs == 'y':
            return True
        else:
            return False

#I HAVE NO IDEA WHAT I'M DOING!!! subprocesses + shit
import subprocess
#import os
class ExternalAI(Player):
    def __init__(self, cards: Cards, shell_cmd:str):
        #self.f = os.tmpfile()
        self.p = subprocess.Popen(shell_cmd.split(), stdout=subprocess.PIPE, stdin = subprocess.PIPE)
        #idk what to do with the rror... either pipe it to STDOUT or a new PIPE.
        super().__init__(cards)
        #input format: first line will be num of players, and number of cards that each player (e.g. you) has.
        #              second line will be the cards.
        #x =
        self.p.communicate(input= "{} {}\n{}".format(player_amount, hand_size, self.pretty_str()).encode())
        #print(x)
    def move(self, turn_rank):
        #input format: some way to signify that this is the bginning of a move prompt.  the turn rank.  and the hand (optional)
        output = self.p.communicate(input="PLAY\n{}\n{}".format(turn_rank, self.pretty_str()))
            #maybe need b'string here'
        #copy-pasted code from Human class.  poop copy-pasting.  can't think of better method (where to store shared sourcecode)
        try:
            play_cards = Cards([Card.pretty_to_card(i) for i in output.split()])
        except ValueError:
            raise ValueError('These are not proper cards values.  Proper values are e.g.: a a 2')
            #continue
        try:
            assert len(play_cards) >= 1
            return self.cards.remove(play_cards)
        except Exception as e:
            raise e("You don't have those cards or you tried playing nothing.")
    def call_bs(self, play, turn_rank):
        output = self.p.communicate(input="BS\n{}{}".format(turn_rank, play))
        if output.decode() == 1:
            return True
        else:
            return False



class AI(Player):
    def move(self):
        tcount = self.cards.count(rank = turn_rank)
        if tcount > 0:
            return self.cards.remove([Part_Card(rank=turn_rank) for _ in range(tcount)])
        else:
            bluff_rank = range(1,14)[turn_rank - 1 - player_amount]
            while bluff_rank != turn_rank:
                try:
                    return self.cards.remove([Part_Card(rank=bluff_rank)])
                except:
                    
                    pass
                bluff_rank = range(1,14)[bluff_rank - 1 - player_amount]
        return self.cards.pop_n(1)
    def call_bs(self, play, turn_rank):
        print(self.cards.count(rank = turn_rank))
        if 4 - play < self.cards.count(rank = turn_rank):
            print(self.cards)
            return True
            
def i2s(i:int):
    try:
        return ['no', 'one', 'two', 'three', 'four', 'five', 'six'][i]
    except:
        return i
    
def is_bs(player_cards: Cards, turn_rank):
    return not all(card.rank == turn_rank for card in player_cards)

 
deck = Deck()
deck.shuffle()
#(deck)

player_types = [(Human,[]), (ExternalAI, ['python test.py'])]
player_amount = len(player_types)
hand_size = len(deck)//player_amount
#players = [Human(deck.pop_n(hand_size)) for i in range(player_amount)]
players = [player_type(deck.pop_n(hand_size), *args) for player_type, args in player_types]
#player_amount = len(players)
#hand_size = len(deck)//player_amount

winner = False
turn_player = players[0]
turn_rank = 1
com_cards = Cards()
while not winner:
    print('-')
    player_index = players.index(turn_player)
    player_cards = turn_player.move()
    com_cards += player_cards
    print("Player {} claims to play {} {}{}".format(player_index, i2s(len(player_cards)), Card.trans_dict[turn_rank-1], 's'*(len(player_cards) > 1)))
    for player in [p for p in players if p != turn_player]: #rewrite this to be in order starting with turn_player.
        if player.call_bs(len(player_cards), turn_rank):
            if is_bs(player_cards, turn_rank):
                turn_player.cards += com_cards
                print("BS! The cards were {} instead of {} {}{}. {} cards given to {}".format(
                    player_cards, i2s(len(player_cards)), Card.trans_dict[turn_rank-1], 's'*(len(player_cards) > 1),
                    len(com_cards), turn_player))
                com_cards = Cards()
                break
            else:
                print("NOT BS! {} cards given to {}".format(len(com_cards), player))
                player.cards += com_cards
                com_cards = Cards()
                break
    if len(turn_player.cards) == 0:
        print("{} wins!  Congrats".format(turn_player))
        break
    turn_player = players[(player_index + 1)%len(players)]
    turn_rank = (turn_rank)%13 + 1
    #print(turn_rank)
    
print([str(player.cards) for player in players])
