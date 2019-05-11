import numpy as np
from tictactoe import TicTacToe
from ai_player import AIPlayer
from softmax_player import SoftmaxPlayer

p1 = AIPlayer()
p2 = SoftmaxPlayer()

# Train e-greedy player against itself.
for _ in range(2000):
  game = TicTacToe(p1, p1)
  game.start()

# Train softmax player against itself.
for _ in range(2000):
  game = TicTacToe(p2, p2)
  game.start()

# Set parameters so that optimal moves are preferred.
p1.epsilon = 0
p2.theta = 1

# Remove stats from training matches.
p1.draws = 0
p1.wins = 0
p1.losses = 0
p2.draws = 0
p2.wins = 0
p2.losses = 0

# E-greedy vs softmax.
for _ in range(100):
  game = TicTacToe(p1, p2)
  game.start()

print('E-greedy wins: {}, Softmax wins: {}, draws: {}'.format(p1.wins, p2.wins, p1.draws))
