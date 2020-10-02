from stable_baselines.common.env_checker import check_env
import gym

test = True

if test:
    import Reinforcement_AI.test_env as env
else:
    import Reinforcement_AI.env as env

env = env.KartEnv(1, 2)
check_env(env)