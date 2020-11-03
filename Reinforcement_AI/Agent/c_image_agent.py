# 에이전트의 Reset에 대해
# 에이전트는 timestep만큼 step을 밟고, 이후 reset한다.
# 따라서, 환경에서 reset을 수행하지 말고, timestep을 적절하게 설정해서 스스로 loss를 줄이게끔 한다.
# FPS가 130정도 나온다고 잡고, 12950이 95초이니, 일단 제대로 도는지를 테스트하기 위해서는
# Timestep을 130 * 30정도로 하고 돌려보는게 나을듯






def launchAgent():
    import Reinforcement_AI.env.d_image_env as image_env
    from stable_baselines import DQN, HER, DDPG, PPO2
    from stable_baselines.common import make_vec_env

    model_name = "PPO2"

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
    if model_name == "PPO2":
        # env = image_env.DetailedMiniMapEnv()
        env = make_vec_env(image_env.DetailedMiniMapEnv, n_envs=1)
        model = PPO2(
            policy="CnnPolicy",
            env=env,
            verbose=1
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
                model.set_env(image_env.DetailedMiniMapEnv())
            if model_name == "DDPG":
                model = DDPG.load("detailedmap_DDPG_" + str(i))
                model.set_env(image_env.DDPGImageEnv())
            if model_name == "PPO2":
                model = PPO2.load("detailedmap_PPO2_" + str(i))
                ppo2_env = make_vec_env(image_env.DetailedMiniMapEnv, n_envs=1)
                model.set_env(ppo2_env)
            else:
                model = DQN.load("detailedmap_DQN_" + str(i))
                model.set_env(image_env.DetailedMiniMapEnv())

        model.learn(total_timesteps=3900)

        model.save("detailedmap_" + model_name + "_" + str(i+1))
        del model

if __name__ == "__main__":
    from Image_Processing.image_processing import runIP
    from multiprocessing import Manager

    manager = Manager()
    runIP(manager)
    launchAgent()

