# Play 3D tic-tac-toe
# 4 x 4 dimensions

from game import TicTacToe, Player

game = TicTacToe()
game.print_board()
game.make_move((0, 1, 2), Player.USER)
game.make_move((0, 2, 1), Player.AI)
print("After move")
game.print_board()