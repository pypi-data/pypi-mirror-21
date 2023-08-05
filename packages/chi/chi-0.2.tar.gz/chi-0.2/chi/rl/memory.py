import numpy as np


# TODO: make this list-based (i.e. variable sized)

class ReplayMemory:
  def __init__(self, size, dimO, dimA, batch_size=64):
    self.size = size
    so = np.concatenate(np.atleast_1d(size, dimO), axis=0)
    sa = np.concatenate(np.atleast_1d(size, dimA), axis=0)
    self.observations = np.empty(so, dtype=object)
    self.actions = np.empty(sa, dtype=object)
    self.rewards = np.empty(size, dtype=np.float32)
    self.terminals = np.empty(size, dtype=np.bool)
    self.info = np.empty(size, dtype=object)

    self.batch_size = batch_size

    self.n = 0
    self.i = -1

  def reset(self):
    self.n = 0
    self.i = -1

  def enqueue(self, observation, action, reward, terminal, info=None):
    self.i = (self.i + 1) % self.size

    self.observations[self.i, ...] = observation
    self.terminals[self.i] = terminal  # tells whether this observation is the last

    self.actions[self.i, ...] = action
    self.rewards[self.i] = reward

    self.info[self.i, ...] = info

    self.n = min(self.size - 1, self.n + 1)

  def sample_batch(self, size=None):
    size = size or self.batch_size
    indices = np.random.randint(0, self.n - 2, size)

    o = self.observations[indices, ...]
    a = self.actions[indices]
    r = self.rewards[indices]
    t = self.terminals[indices]
    o2 = self.observations[indices + 1, ...]
    # t2 = self.terminals[indices+1] # to return t2 instead of t was a mistake
    info = self.info[indices, ...]

    return o, a, r, t, o2, info

  def __repr__(self):
    indices = range(0, self.n)
    o = self.observations[indices, ...]
    a = self.actions[indices]
    r = self.rewards[indices]
    t = self.terminals[indices]
    info = self.info[indices, ...]

    s = f"Memory with n={self.n}, i={self.i}\nOBSERVATIONS\n{o}\n\nACTIONS\n{a}\n\nREWARDS\n{r}\n\nTERMINALS\n{t}\n"

    return s


def test_rm():
  s = 100
  rm = ReplayMemory(s, 1, 1)

  for i in range(0, 100, 1):
    rm.enqueue(i, i % 3 == 0, i, i, i)

  for i in range(1000):
    o, a, r, t, o2, info = rm.sample_batch(10)
    assert all(o == o2 - 1), "error: o and o2"
    assert all(o != s - 1), "error: o wrap over rm. o = " + str(o)
    assert all(o2 != 0), "error: o2 wrap over rm"


if __name__ == '__main__':
  pass