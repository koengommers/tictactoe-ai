import numpy as np
from ai_player import AIPlayer

class SoftmaxPlayer(AIPlayer):
  """AI that uses softmax policy instead of default e-greedy."""
  def __init__(self, alpha=0.7, theta=0.5, gamma=0.9, win=3, loss=-3, draw=1):
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

    self.alpha = alpha
    self.gamma = gamma
    self.theta = theta

  def make_move(self, game):
    """Chooses move using softmax."""
    mark = self.get_mark(game.turn)
    self.learn(mark, 0, game.state)

    new = True
    s = game.state.repr
    t = tuple(game.state)
    actions = np.zeros(t.count(0))

    for variation, rotations, flip in game.state.variations():
      if variation in self.states[mark].keys():
        new = False
        t = variation
        s = np.reshape(variation, (3,3))
        actions = self.states[mark][variation]
        break

    if new:
      rotations = 0
      flip = 0
    exp = np.exp(actions*self.theta)
    probs = exp/np.sum(exp)
    choice = np.random.choice(len(probs), p=probs)
    zeros = np.argwhere(s == 0)
    c = np.flip(zeros[choice])
    self.last_action[mark] = (t, choice)
    return self.convert_coordinates(c, flip, rotations)
