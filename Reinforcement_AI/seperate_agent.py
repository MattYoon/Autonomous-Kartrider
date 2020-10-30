def launchAgent():
    from stable_baselines import DQN
    import Reinforcement_AI.env.seperate_env as sep_env
    from queue import Queue
    from threading import Thread

    minimap_env = sep_env.MinimapEnv()
    allenv = sep_env.AllEnv()

    minimap_model = DQN(
        "CnnPolicy",  # policy
        minimap_env,  # environment
        double_q=True,  # Double Q enable
        prioritized_replay=True,  # Replay buffer enabled
        verbose=0  # log print
    )

    allenv_model = DQN(
        "MlpPolicy",
        allenv,
        double_q=True,
        prioritized_replay=True,
        verbose=0
    )

    for i in range(100):
        if i != 0:
            minimap_model = DQN.load("KR_minimap_" + str(i))
            allenv_model = DQN.load("KR_allenv_" + str(i))

        que = Queue()

        minimap_model.set_env(minimap_env)
        allenv_model.set_env(allenv)

        # minimap_thread = Thread(target=minimap_model.learn, args=[50000])
        # allenv_thread = Thread(target=allenv_model.learn, args=[50000])
        allenv_thread = Thread(target=lambda q, arg1: q.put(allenv_model.learn(arg1)), args=(que, 50000))
        # test = Pool(processes=1)

        # minimap_thread.start()
        allenv_thread.start()
        # test_result = test.apply_async(allenv_model.learn, (50000, None, 100, "DQN", True, None))
        minimap_model.learn(total_timesteps=50000)

        # allenv_model.learn(total_timesteps=50000)

        # minimap_thread.join()
        allenv_thread.join()

        allenv_model = que.get()
        # return_val = test_result.get()

        minimap_model.save("KR_minimap_" + str(i + 1))
        allenv_model.save("KR_allenv_" + str(i + 1))
        # return_val.save("KR_allenv_" + str(i+1))


if __name__ == "__main__":
    from Image_Processing.image_processing import runIP
    from multiprocessing import Manager

    manager = Manager()
    runIP(manager)
    launchAgent()

