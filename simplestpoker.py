#rules: each player gets a number between 0 and 1.
import random

class Player:
    def __init__(self, number = None):
        self.number = number
    def move(self):
        pass
    def get_dealt(self, max_num = 1):
        """Deal the player a new number"""
        self.number = random.random() * max_num

def run_game(num_of_players = 3):
    players = [Player() for i in range(num_of_players)]
    while True:
        for player in players:
            player.get_dealt()
            print(player.number)

run_game()
        
