from stable_baselines.common.vec_env import DummyVecEnv
from stable_baselines.common.policies import MlpPolicy
from stable_baselines.her import GoalSelectionStrategy, HERGoalEnvWrapper
from stable_baselines.common.bit_flipping_env import BitFlippingEnv
from stable_baselines import DQN, TRPO, HER, ACER, ACKTR
from stable_baselines.common import make_vec_env
import Reinforcement_AI.env as Kart
import random
import numpy as np

env = Kart.KartEnv()
vec_env = make_vec_env(Kart.KartEnv, n_envs=1)

# model = DQN("MlpPolicy", env, verbose=1)          # DQN 모델
# model = TRPO("MlpPolicy", env, verbose=1)         # TPRO 모델
# model = ACER("MlpPolicy", env, verbose=1)         # ACER 모델
model = ACKTR("MlpPolicy", env, verbose=1)          # ACKTR 모델



obs = env.reset()
while True:
    action, _states = model.predict(obs)
    obs, rewards, dones, info = env.step(action)            # (gap)
    print(obs, rewards, dones, info)
