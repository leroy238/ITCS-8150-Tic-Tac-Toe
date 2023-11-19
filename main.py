# Play 3D tic-tac-toe
# 4 x 4 dimensions

from game import TicTacToe, Player

game = TicTacToe()
game.print_board()
game.play_turn(Player.USER, (0, 1, 2))
game.play_turn(Player.AI, (0, 2, 1))
print(game.get_state())
game.print_board()
game.play_turn(Player.USER, (0, 1, 1))
game.play_turn(Player.AI, (0, 3, 1))
print(game.get_state())
game.print_board()
game.play_turn(Player.USER, (0, 1, 0))
game.play_turn(Player.AI, (1, 2, 1))
print(game.get_state())
game.print_board()
game.play_turn(Player.USER, (0, 1, 3))
game.play_turn(Player.AI, (1, 3, 1))
# print("After move")
print(game.get_state())
game.print_board()