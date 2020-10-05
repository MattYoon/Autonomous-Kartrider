from stable_baselines import DQN  # , TRPO, HER, ACER, ACKTR

# import Reinforcement_AI.env as Kart
from Reinforcement_AI.box2d_env import BoxKartEnv

#import tensorflow as tf

#sess = tf.Session(config=tf.ConfigProto(log_device_placement=True))

env = BoxKartEnv()
# dummyenv = FlattenObservation(env)
# dummyenv = DummyVecEnv([BoxKartEnv()])
# env = make_vec_env(Kart.KartEnv, n_envs=1)



model = DQN("MlpPolicy", env, double_q=True, prioritized_replay=True, verbose=1)  # DQN 모델
for i in range(100):
    if i != 0:
        model = DQN.load("kartrider_" + str(i))
    model.set_env(env)
    model.learn(total_timesteps=50000)
    model.save("kartrider_" + str(i+1))
    del model


# model = TRPO("MlpPolicy", env, verbose=1)        2 # TPRO 모델
# model = ACER("MlpPolicy", env, verbose=1)         # ACER 모델
# model = ACKTR("MlpPolicy", env, verbose=1)          # ACKTR 모델


obs = env.reset()
while True:
    action, _states = model.predict(obs)
    obs, rewards, dones, info = env.step(action)            # (gap)
    print(obs, rewards, dones, info)
