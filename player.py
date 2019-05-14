class Player:
  """Class for a human player."""

  def make_move(self, game):
    """Asks user for move."""
    print(game.state)
    move = input('What\'s your move? ')

    if move in ['exit', 'stop', 'quit']:
      print('Quitting...')
      exit()

    while not (len(move.split()) == 2 and all([m.isdigit() for m in move.split()])):
      print('Invalid input. Please try again.')
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
