
from enum import Enum
import pprint

class GameState(Enum):
    IN_PROGRESS = 1,
    AI_WIN = 2,
    USER_WIN = 3,
    DRAW = 4

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
    return [[ ['-' for _ in range(self.dim)] for _ in range(self.dim)] for _ in range(self.dim)]

  def play_turn(self, player: Player, pos: (int, int, int)):
    if self.valid_move(pos):
      self.make_move(pos, player)
    else:
      print(f"Invalid move at position {pos}")
    self.calculate_state()
    print(self.get_state())

  def valid_move(self, pos):
    (z, x, y) = pos
    allowed_values = range(0, self.dim)
    return x in allowed_values and y in allowed_values and z in allowed_values and self.board[z][x][y] == "-"

  def make_move(self, pos, player):
    (z, x, y) = pos
    self.board[z][x][y] = '1' if player == Player.AI else '0'

  def four_in_a_row(self, player: Player, values):
    token = '1' if player == Player.AI else '0'
    return values.count(token) == self.dim

  def has_won(self, player: Player):
    for layer in range(self.dim):
      for row in range(self.dim):
        if self.four_in_a_row(player, self.board[layer][row][:]):
          return True
        for col in range(self.dim):
          if row == 0: # to avoid executing this for every pos in layer
            if self.four_in_a_row(player, self.board[layer][:][col]):
              return True
          if layer == 0 and row == 0 and col == 0:
            # check for diagonal across layers
            top_left_to_bottom_right = [self.board[0][row][col], self.board[1][row + 1][col + 1], self.board[2][row + 2][col + 2], self.board[3][row + 3][col + 3]]
            if self.four_in_a_row(player, top_left_to_bottom_right):
              return True
          if layer == 0 and row == 0 and col == self.dim - 1:
            top_right_to_bottom_left = [self.board[0][row][col], self.board[1][row + 1][col - 1], self.board[2][row + 2][col - 2], self.board[3][row + 3][col - 3]]
            if self.four_in_a_row(player, top_right_to_bottom_left):
              return True
            pass
          if layer == 0:
            # check for straight down
            if self.four_in_a_row(player, self.board[:][row][col]):
              return True

          
  def calculate_state(self):
    if self.has_won(Player.AI):
      self.set_state(GameState.AI_WIN)
    elif self.has_won(Player.USER):
      self.set_state(GameState.USER_WIN)
    elif self.is_draw():
      self.set_state(GameState.DRAW)
    else:
      self.set_state(GameState.IN_PROGRESS)

  def set_state(self, new_state: GameState):
    self.state = new_state

  def get_state(self):
    return self.state

  def print_board(self):
    pprint.pprint(self.board)

