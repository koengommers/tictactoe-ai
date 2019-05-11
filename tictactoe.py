import numpy as np
from state import State

class TicTacToe:
  """Represents a TicTacToe game."""
  def __init__(self, player1, player2):
    self.state = State()
    self.turn = -1
    self.players = np.random.permutation([player1, player2])

  def switch_turn(self):
    self.turn *= -1

  def handle_move(self, x, y):
    """Handles a move given by a player."""
    self.state.set(x, y, self.turn)
    self.switch_turn()

  def is_free(self, x, y):
    """Check if value on board is empty."""
    return self.state.get(x, y) == 0

  def is_within_boundaries(self, x, y):
    """Check if move is within board dimensions."""
    return x in range(3) and y in range(3)

  def valid_move(self, move):
    """Check if a move is valid."""
    is_valid_move = move and self.is_within_boundaries(*move) and self.is_free(*move)
    if move and not is_valid_move:
      print('Invalid move')
    return is_valid_move

  def is_full(self):
    """Check if board is full."""
    return np.all(self.state.repr)

  def is_victory(self):
    """Checks if there is a victory."""
    rows = self.state.repr
    columns = self.state.repr.T
    diagonals = np.array([np.diag(self.state.repr), np.diag(np.fliplr(self.state.repr))])
    checks = np.concatenate((rows, columns, diagonals))
    for check in checks:
      if np.abs(np.sum(check)) == 3:
        return True
    return False

  def game_over(self):
    """Checks if there is a game ending situation."""
    if self.is_victory():
      if self.turn == -1:
        self.players[0].lose(-1)
        self.players[1].victory(1)
      elif self.turn == 1:
        self.players[0].victory(-1)
        self.players[1].lose(1)
      return True
    elif self.is_full():
      self.players[0].draw(-1)
      self.players[1].draw(1)
      return True
    return False

  def start(self):
    """Starts the game loop."""
    while not self.game_over():
      player = self.players[0 if self.turn == -1 else 1]
      move = None
      while not self.valid_move(move):
        move = player.make_move(self)
      self.handle_move(*move)
