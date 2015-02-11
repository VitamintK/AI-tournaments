#rules: each player gets a number between 0 and 1.
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

class Poker_Board:
    def __init__(self, num_of_players = 3, init_money = 1000):
        self.players = [Player(money = init_money) for i in range(num_of_players)]
        self.pot = 0
    

    

def run_game(num_of_players = 3, starting_money = 1000):
    pot = 0
    while True:
        for player in players:
            player.get_dealt()
            print(player.number)

run_game(3, 1000)
        
