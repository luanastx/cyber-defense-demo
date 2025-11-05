"""
Ambiente Gym simples onde cada passo é um fluxo.
Ação: 0 = permitir, 1 = bloquear
Recompensa:
- Se fluxo é malicious (label=1) e bloquear -> +1
- Se fluxo é malicious e permitir -> -1
- Se benign e bloquear -> -0.5 (falso positivo)
- Se benign e permitir -> +0.1
Observação: Este é um ambiente simplificado para treinar a política.
"""
import gym
from gym import spaces
import numpy as np

class FlowBlockEnv(gym.Env):
    def __init__(self, X, y):
        super().__init__()
        self.X = X
        self.y = y
        self.n = len(X)
        self.idx = 0
        self.observation_space = spaces.Box(low=-np.inf, high=np.inf, shape=(X.shape[1],), dtype=np.float32)
        self.action_space = spaces.Discrete(2)

    def step(self, action):
        obs = self.X[self.idx]
        label = self.y[self.idx]
        # reward logic
        if label == 1 and action == 1:
            reward = 1.0
        elif label == 1 and action == 0:
            reward = -1.0
        elif label == 0 and action == 1:
            reward = -0.5
        else:
            reward = 0.1
        self.idx += 1
        done = (self.idx >= self.n)
        next_obs = self.X[self.idx] if not done else np.zeros_like(obs)
        return next_obs.astype(np.float32), reward, done, {"label": int(label)}

    def reset(self):
        self.idx = 0
        # shuffle for variedade
        perm = np.random.permutation(self.n)
        self.X = self.X[perm]
        self.y = self.y[perm]
        return self.X[0].astype(np.float32)