def launchAgent():
    import Reinforcement_AI.env.d_image_env as image_env
    from stable_baselines import DQN, HER, DDPG

    model_name = "DQN"

    if model_name == "HER":
        model = HER(
            "CnnPolicy",
            env=image_env.DetailedMiniMapEnv(),
            model_class=DQN
        )
    if model_name == "DDPG":
        model = DDPG(
            policy="CnnPolicy",
            env=image_env.DDPGImageEnv(),
            normalize_observations=True
        )
    else:
        model = DQN(
            "CnnPolicy",  # policy
            env=image_env.DetailedMiniMapEnv(),  # environment
            double_q=True,  # Double Q enable
            prioritized_replay=True,  # Replay buffer enabled
            verbose=0  # log print
        )

    for i in range(100):
        if i != 0:
            if model_name == "HER":
                model = HER.load("detailedmap_HER_" + str(i))
            if model_name == "DDPG":
                model = DDPG.load("detailedmap_DDPG_" + str(i))
            else:
                model = DQN.load("detailedmap_DQN_" + str(i))

        model.learn(total_timesteps=50000)

        model.save("detailedmap_" + model_name + "_" + str(i+1))


if __name__ == "__main__":
    from Image_Processing.image_processing import runIP
    from multiprocessing import Manager

    manager = Manager()
    runIP(manager)
    launchAgent()

