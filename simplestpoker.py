"""rules: each player gets a number between 0 and 1.
the player with the highest number (who hasn't folded) wins the hand.
each player must contribute ante to the pot (ante = 100 by default).
players can bet, check, raise, call, and fold.  (just like poker).
most rules are like poker.
"""

import random

class Player:
    def __init__(self, money = 1000):
        self.number = None
        self.money = money
    def move(self):
        pass
    def get_dealt(self, max_num = 1):
        """Deal the player a new number"""
        self.number = random.random() * max_num
    def bet(self, amount):
        """bet the amount if possible, otherwise go all-in.  return the amount bet."""
        bet_amount = min(amount, self.money)
        self.money = self.money - bet_amount
        return bet_amount

class Pot:
    def __init__(self, players = None):
        if not players:
            players = []
        self.players = set(players)
        self.amount = 0
    def add_bet(self, player, bet):
        self.players.add(player)
        self.amount += bet
    def fold_player(self, player):
        self.players.remove(player)

class Poker_Board:
    def __init__(self, num_of_players = 3, init_money = 1000, ante = 100, big_blind = None):
        self.players = [Player(money = init_money) for i in range(num_of_players)]
        self.pots = [Pot()]
        self.ante = ante
        self.big_blind = big_blind
    def deal_hand(self):
        for player in self.players:
            player.get_dealt()
            bet_amount = player.bet(self.ante)
            if bet_amount == self.ante:
                self.pots[main_pot].add_bet(player, bet_amount)
            else:
                
                
                
    

    

def run_game(num_of_players = 3, starting_money = 1000):
    pot = 0
    while True:
        for player in players:
            player.get_dealt()
            print(player.number)

run_game(3, 1000)
        
