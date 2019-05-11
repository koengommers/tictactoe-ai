import time
from tictactoe import TicTacToe
from player import Player
from ai_player import AIPlayer

p1 = Player()
p2 = AIPlayer()

# Train with 10000 games against itself.
print('Learning...')
t = time.time()
for _ in range(10000):
  game = TicTacToe(p2, p2)
  game.start()
print('Learned {} unique states from {:.0f} games in {:.2f} seconds'.format(
  len(p2.states['x']) + len(p2.states['o']),
  p2.games_played()/2,
  time.time() - t
))

# Only perform best moves.
p2.epsilon = 0

# Play against human player.
while True:
  game = TicTacToe(p1, p2)
  game.start()
