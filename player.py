class Player:
  """Class for a human player."""

  def make_move(self, game):
    """Asks user for move."""
    print(game.state)
    move = input('What\'s your move? ')
    return [int(x) - 1 for x in move.split()]

  def draw(self, turn):
    """Processes a match draw."""
    print('It\'s a draw!')

  def lose(self, turn):
    """Processes a match loss."""
    print('You lost.')

  def victory(self, turn):
    """Processes a match victory."""
    print('You won!')
