def launchAgent(env_name: int, model_name: str, test_mode=False, filepath=None):
    """
    :param test_mode: 에이전트를 테스트 모드로 불러와 주행시킬지를 확인하는 모드입니다. 이럴 시에 학습은 이루어지지 않으며, 주행만 이루어집니다.
    :param env_name: 불러올 환경의 이름입니다.
        1 : 미니맵 이미지를 사용하지 않은, 점 사이의 거리 계산을 한 환경입니다.
        2 : 미니맵 이미지를 사용하고, 보상을 업데이트한 모델입니다.
        다른 값(기본) : 현재 쓰는 모델입니다. 미니맵 이미지를 사용하고, 보상을 다시 업데이트한 모델입니다.
    :param model_name: 설정할 모델의 이름입니다.
        DQN : DQN 모델을 불러옵니다.
        HER : HER 모델을 불러옵니다.
        다른 값(기본) : PPO2 모델을 불러옵니다.
    :return: 마지막으로 episode를 수행한 모델을 return합니다.
    """

    from stable_baselines import DQN, HER, PPO2

    if env_name == 1:
        from Reinforcement_AI.env.a_env import KartEnv
        kart_env = KartEnv()
        policy = "MlpPolicy"
    elif env_name == 2:
        from Reinforcement_AI.env.d_image_env import DetailedMiniMapEnv as DetailedMiniMapEnv1
        kart_env = DetailedMiniMapEnv1()
        policy = "CnnPolicy"
    elif env_name == 3:
        from Reinforcement_AI.env.a_env2 import KartEnv
        kart_env = KartEnv()
        policy = "MlpPolicy"
    elif env_name == 4:
        from Reinforcement_AI.env.a_env3 import KartEnv
        kart_env = KartEnv()
        policy = "MlpPolicy"
    else: #env_name == "detailed_minimap_enhanced" or env_name == "4":
        from Reinforcement_AI.env.e_enhanced_image_env import DetailedMiniMapEnv as DetailedMiniMapEnv2
        kart_env = DetailedMiniMapEnv2()
        policy = "CnnPolicy"


    if model_name == "DQN":
        model = DQN(policy=policy, env=kart_env, double_q=True, prioritized_replay=True, verbose=1)
    elif model_name == "HER":
        model = HER(policy=policy, env=kart_env, model_class=DQN, verbose=1)
    else: # model_name == "PPO2"
        model = PPO2(policy=policy, learning_rate=0.0001, env=kart_env, verbose=1)

    if test_mode:       # 테스트 모드일때 에이전트 불러와서 작동하게함
        model.load(filepath)
        kart_env.set_continuos(True)

        while True:
            observation = kart_env.reset()
            while True:
                action, _states = model.predict(observation)
                observation, rewards, dones, info = kart_env.step(action)
                if dones:
                    break

    else:
        for i in range(1000):
            model.learn(total_timesteps=12500)
            model.save(str(env_name) + "_" + model_name + "_" + str(i+1))


if __name__ == "__main__":

    import sys
    import time
    import os

    PATH = os.path.dirname(os.path.realpath(__file__))

    if len(sys.argv) != 2:
        print("프로그램에 심각한 에러 발생! 종료합니다.")
        time.sleep(2)

    if sys.argv[1] == "1":
        filepath = PATH + "/Best_Agent/PPO2_best"
    elif sys.argv[1] == "2":
        filepath = PATH + "/Best_Agent/PPO2_best2"
    else:
        print("프로그램에 심각한 에러 발생! 종료합니다.")
        time.sleep(2)




    # 에이전트 및 환경 설정
    agent = "PPO2"
    env = 3
    """
    env: 불러올 환경의 이름입니다. (int)
        1 : 미니맵 이미지를 사용하지 않은, 점 사이의 거리 계산을 한 환경입니다.
        2 : 미니맵 이미지를 사용하고, 보상을 업데이트한 모델입니다.
        3 : 1의 버전에서 개선된 모델입니다.
        4 : 3의 버전에서 부스터를 사용하도록 개선된 모델입니다.
        다른 값(기본) : 현재 쓰는 모델입니다. 미니맵 이미지를 사용하고, 보상을 다시 업데이트한 모델입니다.
    agent: 설정할 모델의 이름입니다.
        DQN : DQN 모델을 불러옵니다.
        HER : HER 모델을 불러옵니다.
        다른 값(기본) : PPO2 모델을 불러옵니다.
    """

    if env == 2:
        launchAgent(env, agent)
    else:
        from Image_Processing.image_processing import runIP
        from multiprocessing import Manager

        manager = Manager()
        runIP(manager)
        launchAgent(env, agent, test_mode=True, filepath=filepath)


