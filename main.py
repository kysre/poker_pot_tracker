from enum import Enum


class Player:
    def __init__(self, name, starting_stack):
        self.name = name
        self.stack = starting_stack
        self.player_state = PlayerState.NOT_CHOSEN

    def bet(self, amount):
        if self.stack >= amount:
            self.stack -= amount
            return True
        else:
            return False

    def win(self, amount):
        self.stack += amount

    def set_player_state(self, state):
        self.player_state = state


class Game:
    def __init__(self, player_list):
        self.players = player_list
        self.pot = 0
        self.game_state = GameState.PRE_FLOP

    def is_game_ended(self):
        count = 0
        for player in self.players:
            if player.stack > 0:
                count += 1
        return not (count > 1)

    def set_game_state(self, state):
        self.game_state = state

    def print_game_stats(self):
        print(f'State: {self.game_state.name}')
        print('Stacks:')
        for player in self.players:
            if player.player_state != PlayerState.FOLD:
                print(f'{player.name:>12}\t{player.stack}')
        print(f'\n Pot: {self.pot}')

    def is_there_winner(self):
        fold_count = 0
        for player in self.players:
            if player.player_state is PlayerState.FOLD:
                fold_count += 1
        return fold_count == len(players) - 1

    def set_game_state(self, game_state_code):
        if game_state_code == 0:
            self.game_state = GameState.PRE_FLOP
        elif game_state_code == 1:
            self.game_state = GameState.FLOP
        elif game_state_code == 2:
            self.game_state = GameState.TURN
        else:
            self.game_state = GameState.RIVER

    def win(self, winner_name):
        for player in self.players:
            player.set_player_state(PlayerState.NOT_CHOSEN)
            if player.name == winner_name:
                player.stack += self.pot
                self.pot = 0


class GameState(Enum):
    PRE_FLOP = 0
    FLOP = 1
    TURN = 2
    RIVER = 3


class PlayerState(Enum):
    NOT_CHOSEN = 0
    FOLD = -1
    CHECK = 1
    CALL = 2
    RAISE = 3


names = list(input('Please input player names with spaces in between: ').split())
starting_stack_size = int(input('Please input starting stack: '))
players = [Player(name, starting_stack_size) for name in names]

game = Game(players)
player_count = len(players)
sb_index = 0
while not game.is_game_ended():

    for game_state_code in range(4):
        game.set_game_state(game_state_code)
        game.print_game_stats()

        if not game.is_there_winner():
            biggest_bet = 0
            biggest_bet_index = (sb_index + player_count - 1) % player_count
            i = 0

            while (sb_index + i) % player_count != biggest_bet_index:
                player_index = (sb_index + i) % player_count
                if players[player_index].player_state is not PlayerState.FOLD:
                    bet = int(input(f'Please enter {players[player_index].name}\'s bet: '))
                    if bet != -1:
                        if bet > biggest_bet:
                            biggest_bet = bet
                            biggest_bet_index = player_index
                        players[player_index].bet(bet)
                        game.pot += bet
                    else:
                        players[player_index].player_state = PlayerState.FOLD
                i += 1
                print(f'Pot: {game.pot}')

    winner_name = input("Please enter this hand's winner name: ")
    game.win(winner_name)
    sb_index = (sb_index + 1) % player_count
