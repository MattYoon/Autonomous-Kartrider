# 일반적인 강화학습 환경과 동일하게 맞춤
# 한 바퀴를 주어진 시간 내에 주행하는 것이 목표임
# 한 바퀴를 도는 데 걸리는 시간이 한 episode이며 (대략 12500 timestep)
# 그때까지 완주를 기다림
# 완주하기 전까지는 프레임당 점수를 깎고 (역주행시, 속도 100이하로 감소시 더 깎음)
# 완주하면 1250점을 줌
# 최적의 상황은 결과값이 >0인 상황 (각 timestep마다 점수가 0.1점씩 깎여서 1250점이 깎이고 1250점을 받는 상황)

def launchAgent(model_name: str):
    """
    :param model_name: 실행시킬 모델의 종류. HER, DDPG, PPO2 혹은 기타값(DQN)이어야 함
                        현재는 의도상 PPO2로 세팅할 것
    :return: 1000회의 사이클을 돌고 난 이후의 모델
    """
    import Reinforcement_AI.env.e_enhanced_image_env as image_env
    from stable_baselines import DQN, HER, DDPG, PPO2
    from stable_baselines.common import make_vec_env

    print("Current Env is " + model_name)

    if model_name == "HER":
        env = image_env.DetailedMiniMapEnv()
        model = HER(
            "CnnPolicy",
            env=env,
            model_class=DQN
        )
    if model_name == "DDPG":
        env = image_env.DDPGImageEnv()
        model = DDPG(
            policy="CnnPolicy",
            env=env,
            normalize_observations=True
        )
    if model_name == "PPO2":
        env = make_vec_env(image_env.DetailedMiniMapEnv, n_envs=1)
        model = PPO2(
            policy="CnnPolicy",
            env=env,
            verbose=1
        )
    else:
        env = image_env.DetailedMiniMapEnv()
        model = DQN(
            "CnnPolicy",  # policy
            env=env,  # environment
            double_q=True,  # Double Q enable
            prioritized_replay=True,  # Replay buffer enabled
            verbose=0  # log print
        )

    for i in range(1000):
        if i != 0:
            if model_name == "HER":
                model = HER.load("detailedmap_HER_" + str(i), env)
            if model_name == "DDPG":
                model = DDPG.load("detailedmap_DDPG_" + str(i), env)
            if model_name == "PPO2":
                model = PPO2.load("detailedmap_PPO2_" + str(i), env)
            else:
                model = DQN.load("detailedmap_DQN_" + str(i), env)

        # print('model learn start')
        model.learn(total_timesteps=12500)  #FPS가 130이상 넘어갈때의 최소수치
        print("this model is : detailedmap_" + model_name + "_" + str(i+1))
        # print('model learn finished')

        # print('model save start')
        model.save("detailedmap_" + model_name + "_" + str(i+1))
        del model
        # print('model save end')

    return model

if __name__ == "__main__":
    from Image_Processing.image_processing import runIP
    from multiprocessing import Manager

    manager = Manager()
    runIP(manager)
    launchAgent("PPO2")

