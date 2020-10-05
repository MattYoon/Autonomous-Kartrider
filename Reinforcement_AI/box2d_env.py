import gym
import numpy as np
from gym import spaces

import Image_Processing.image_processing as ip
import Reinforcement_AI.func as func
import keyinput
import reset_env

# 012 -> 직진, 정지, 후진
# 012 -> 우회전, 방향전환없음, 좌회전
fb_direction = [keyinput.FORWARD, 0, keyinput.BACK]
rl_direction = [keyinput.RIGHT, 0, keyinput.LEFT]

direction_9 = [
    [fb_direction[0], rl_direction[0]],     # 전+우
    [fb_direction[0], rl_direction[1]],     # 전진
    [fb_direction[0], rl_direction[2]],     # 전+좌
    [fb_direction[1], rl_direction[0]],     # 우
    [fb_direction[1], rl_direction[2]]]     # 좌

printLoc = ["전 + 우", "전진", "전 + 좌", "우회전", "좌회전"]


def change_direction(pre_direction, direction):
    """
    입력은 모두 [전후표기, 좌우표기] 이며, 1 전진, 0정지, -1후진 ... 1 우, 0 직진, -1 좌이다.
    :param pre_direction: 저번 방향, [전후, 좌우]
    :param direction: 현재 direction
    :return: direction을 return
    """
    result = direction
    pre_direction = direction_9[pre_direction]
    direction = direction_9[direction]

    if pre_direction[0] == direction[0]:  # 전후가 같을때
        pass
    else:
        func.press_onekey(direction[0])
        func.release_onekey(pre_direction[0])

    if pre_direction[1] == direction[1]:
        pass
    else:
        func.press_onekey(direction[1])
        func.release_onekey(pre_direction[1])

    return result


class KartEnv(gym.Env):
    """Custom Environments follows gym interface"""
    metadata = {'render.modes': ['human']}
    pre_direction = 4
    pre_speed = 0

    def __init__(self, minimap_width, minimap_height):
        super(KartEnv, self).__init__()

        # Action Space 설정
        number_of_actions = 5
        self.action_space = spaces.Discrete(number_of_actions)

        # Observation Space 설정
        # Observation시, 미니맵을 가상화한 것을 그대로 보여주는게 나을거같은데...
        # 하얀색 배경에 선을 그려서 일종의 가상화된 맵을 그려주면 좋을듯
        self.observation_space = spaces.Box(low=0, high=255, shape=(minimap_height, minimap_width, 3), dtype=np.uint8)

    def reset(self):
        print('Reset Called, reset environment')
        func.release_all()
        reset_env.manualReset()
        ip.ipCountdown()
        return self.observation()

    def observation(self):
        # 미니맵 정보를 완전히 받아오는 무언가의 함수
        minimap = 0
        speed = 0
        return minimap, speed

    def step(self, action):
        self.pre_direction = change_direction(self.pre_direction, action)

        minimap, speed = self.observation()
        complete = False

        # 게임 종료에 관한 부분
        if speed == 0:
            # 속도가 0일 때 (벽에 부딛혔을 때)
            print("Crashed to the wall!")
            return minimap, -10, True, {"direction": printLoc[action]}
        if complete:
            # 만약 게임을 완료했다면
            print("Complete Racing!")
            return minimap, 500, complete, {"status": "Complete!"}

        # 여기서 pre_speed와 현재 speed를 비교해야 한다
        reward = self.calculate_reward()
        self.pre_speed = speed

        # 각 Step을 print
        print(reward, complete, printLoc[action])
        return minimap, reward, complete, {"direction": printLoc[action]}

    def calculate_reward(self, observation):
        # 프레임당 점수를 깎을 수 있으나, 비효율적이라 생각됨
        reward = 0

        out_of_track = False
        speed_diff = 0
        reverse = False

        # 미니맵의 길에서 유저가 벗어났을 때
        # 미니맵 플레이어의 위치가 실제 트랙의 위치와 같지 않으므로, 외곽선에 붙거나 하면 넘어갈 수 있음
        # 일종의 충돌 체크용
        # 어떻게 구현할 것이냐?
        # 플레이어의 화살표는 원래 외곽점들의 집합으로 주어지므로, 외곽점들의 집합이 길 안에 속해있는 범위로 계산
        # 예를 들어, 외곽점 집합의 70%가 안에 속해있다면, reward는 -0.6이 됨 (100%가 밖에있다면 -2)
        if out_of_track:
            reward -= 2

        # 속도 비교. 속도가 증가하거나 그대로이면 점수를 1 주고, 속도가 줄어들때엔 reward를 주지 않는다.
        reward += 1 if speed_diff >= 0 else None

        # 뒤로 가는지 비교. 뒤로 갈때는 패널티를 많이 줘야 한다.
        if reverse:
            reward -= 10

        return reward
