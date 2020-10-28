from threading import Thread

from stable_baselines import DQN

import Reinforcement_AI.env.seperate_env as sep_env

minimap_env = sep_env.MinimapEnv()
allenv = sep_env.AllEnv()


minimap_model = DQN(
    "LnCnnPolicy",    # policy
    minimap_env,    # environment
    double_q=True,  # Double Q enable
    prioritized_replay=True,    # Replay buffer enabled
    verbose=1       # log print
)

allenv_model = DQN(
    "LnMlpPolicy",
    allenv,
    double_q=True,
    prioritized_replay=True,
    verbose=1
)

for i in range(100):
    if i != 0:
        minimap_model = DQN.load("KR_minimap_" + str(i))
        allenv_model = DQN.load("KR_allenv_" + str(i))

    minimap_model.set_env(minimap_env)
    allenv_model.set_env(allenv)

    minimap_thread = Thread(target=minimap_model.learn, args=[50000])
    allenv_thread = Thread(target=allenv_model.learn, args=[50000])

    minimap_thread.start()
    allenv_thread.start()

    minimap_thread.join()
    allenv_thread.join()

    minimap_model.save("KR_minimap_" + str(i+1))
    allenv_model.save("KR_allenv_" + str(i+1))
