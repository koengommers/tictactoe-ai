import numpy as np

class AIPlayer:
  """AI Player that makes moves using e-greedy q-learning."""

  def __init__(self, alpha=0.7, epsilon=0.5, gamma=0.9, win=3, loss=-3, draw=1):
    """Inits with certain hyperparameters and reward values."""
    self.states = {
      'x': dict(),
      'o': dict()
    }
    self.last_action = {
      'x': None,
      'o': None
    }

    self.win_reward = win
    self.loss_reward = loss
    self.draw_reward = draw

    self.wins = 0
    self.losses = 0
    self.draws = 0

    self.epsilon = epsilon
    self.alpha = alpha
    self.gamma = gamma

  def games_played(self):
    """Returns number of games played."""
    return self.wins + self.losses + self.draws

  def get_mark(self, turn):
    """Returns the mark given a turn value, either -1 or 1."""
    return 'x' if turn == -1 else 'o'

  def learn(self, mark, reward, next_state=None):
    """Updates q table after a move."""
    if self.last_action[mark] is not None:
      current_state, action = self.last_action[mark]

      max_next_state = 0
      if next_state is not None:
        for variation, _, _ in next_state.variations():
          if variation in self.states[mark].keys():
            actions = self.states[mark][variation]
            max_next_state = np.amax(actions)

      if current_state in self.states[mark].keys():
        actions = self.states[mark][current_state]
      else:
        actions = np.zeros(current_state.count(0))
        self.states[mark][current_state] = actions

      old_q = actions[action]

      pred_error = reward + (self.gamma * max_next_state) - old_q
      update = self.alpha * pred_error

      self.states[mark][current_state][action] += update

      self.last_action[mark] = None

  def make_move(self, game):
    """Returns coordinates of where to place a new mark."""
    mark = self.get_mark(game.turn)
    self.learn(mark, 0, game.state)
    if np.random.rand() < self.epsilon:
      return self.random_action(game.state, mark)
    else:
      return self.best_action(game.state, mark)

  def random_action(self, state, mark, new_guaranteed=False):
    """Returns coordinates randomly from empty places on the board."""
    new = True
    s = state.repr
    t = tuple(state)
    if not new_guaranteed:
      for variation, rotations, flip in state.variations():
        if variation in self.states[mark].keys():
          new = False
          t = variation
          s = np.reshape(variation, (3,3))
          break

    if new:
      flip = 0
      rotations = 0
    choice = np.random.randint(t.count(0))
    zeros = np.argwhere(s == 0)
    c = np.flip(zeros[choice])
    self.last_action[mark] = (t, choice)
    return self.convert_coordinates(c, flip, rotations)

  def best_action(self, state, mark):
    """Returns the action with the highest q value."""
    for variation, rotations, flip in state.variations():
      if variation in self.states[mark].keys():
        actions = self.states[mark][variation]
        choice = np.random.choice(np.argwhere(actions == np.amax(actions)).flatten())
        s = np.reshape(variation, (3,3))
        zeros = np.argwhere(s == 0)
        c = np.flip(zeros[choice])
        self.last_action[mark] = (variation, choice)
        return self.convert_coordinates(c, flip, rotations)
    return self.random_action(state, mark, new_guaranteed=True)

  def convert_coordinates(self, c, flip, rotations):
    """Rotates and/or flips coordinates."""
    c -= 1
    if rotations == 1:
      c = np.dot(np.array([[0, -1], [1, 0]]), c)
    elif rotations == 2:
      c = np.dot(np.array([[-1, 0], [0, -1]]), c)
    elif rotations == 3:
      c = np.dot(np.array([[0, 1], [-1, 0]]), c)
    if flip == 1:
      c[0] *= -1
    c += 1
    return tuple(c)

  def draw(self, turn):
    """Processes a match draw."""
    self.draws += 1
    mark = self.get_mark(turn)
    self.learn(mark, self.draw_reward)

  def lose(self, turn):
    """Processes a match loss."""
    self.losses += 1
    mark = self.get_mark(turn)
    self.learn(mark, self.loss_reward)

  def victory(self, turn):
    """Processes a match victory."""
    self.wins += 1
    mark = self.get_mark(turn)
    self.learn(mark, self.win_reward)
