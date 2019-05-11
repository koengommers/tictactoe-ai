import numpy as np
from itertools import product

class State:
  """Represents a game state."""
  def __init__(self, start=None):
    if start is not None:
      self.repr = start
    else:
      self.repr = np.zeros((3, 3), dtype='int')

  def set(self, x, y, val):
    """Set a value on the board."""
    self.repr[y][x] = val

  def get(self, x, y):
    """Get a value on the board."""
    return self.repr[y][x]

  def variations(self):
    """Returns different orientations that are similar to the state."""
    flips = [self.repr, np.fliplr(self.repr)]
    flipped = range(2)
    rotations = range(4)
    variations = product(flipped, rotations)
    for flip, rotation in variations:
      yield tuple(np.rot90(flips[flip], k=rotation).flatten()), rotation, flip

  def val_to_string(self, val):
    """Represent a value on the board."""
    if val == -1:
      return 'X'
    elif val == 1:
      return 'O'
    return '_'

  def row_to_string(self, row):
    """Represent a row on the board."""
    return ' '.join([self.val_to_string(val) for val in row])

  def __str__(self):
    """Represent the board."""
    return '\n'.join([self.row_to_string(row) for row in self.repr])

  def __iter__(self):
    return iter(self.repr.flatten())

  def __hash__(self):
    return hash(tuple(self))

  def __eq__(self, other):
    if type(self) == type(other):
      return tuple(self) == tuple(other)
    return NotImplemented

  def __ne__(self, other):
    if type(self) == type(other):
      return tuple(self) != tuple(other)
    return NotImplemented
