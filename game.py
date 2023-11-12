
from enum import Enum
import pprint

class GameState(Enum):
    IN_PROGRESS = 1,
    WIN = 2,
    DRAW = 3

class Player(Enum):
  USER = 0,
  AI = 1

class TicTacToe():
  
  def __init__(self):
    self.dim = 4
    self.state = GameState.IN_PROGRESS 
    self.player_turn = Player.USER
    self.board = self.create_board()
  
  def create_board(self):
    return [[["-"] * self.dim] * self.dim] * self.dim

  def play_turn(self, player: Player, pos: (int, int, int)):
    if self.valid_move(pos):
      self.make_move(pos, player)
    else:
      print(f"Invalid move at position {pos}")

  def valid_move(self, pos):
    (z, x, y) = pos
    allowed_values = range(0, self.dim)
    return x in allowed_values and y in allowed_values and z in allowed_values and self.board[z][x][y] == "-"

  def make_move(self, pos, player):
    (z, x, y) = pos
    self.board[z][x][y] = '1' if player == Player.AI else '0'

  def calculate_state(self):
    pass

  def set_state(self, new_state):
    self.state = new_state

  def get_state(self):
    return self.state

  def print_board(self):
    pprint.pprint(self.board)

