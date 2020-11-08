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
    :param env:
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


# 입력이 미니맵에 여러 가지를 첨가한 환경을 만든다.

class DetailedMiniMapEnv(gym.Env):
    """Custom Environments follows gym interface"""
    metadata = {'render.modes': ['human']}
    pre_direction = 4

    def __init__(self):
        super(DetailedMiniMapEnv, self).__init__()

        # Action Space
        action_num = 3
        self.action_space = spaces.Discrete(action_num)

        # Observation Space
        self.observation_space = spaces.Box(low=0, high=1, shape=(142, 179, 3), dtype=np.float)

    def reset(self):
        print("Reset Env")
        func.release_all()
        reset_env.manualReset()
        ip.ipCountdown()
        func.release_all()
        self.pre_direction = 4
        print("check released, ", printLoc[self.pre_direction])
        minimap, _, _, _ = self.observation()
        return minimap

    def observation(self):
        minimap = ip.getSimpleMap() / 255
        # print(minimap.shape)

        # Image Processing에서 값을 받아옴
        finished = ip.isLap2()    # 추후에 추가될 변수, 맵을 완주함을 표시함, bool형태로 받으면 좋을듯

        # 값을 가공함
        speed = ip.getSpeed()   # max값이 250이라 가정
        reverse = ip.getReverse()
        
        # 그대로 return
        return minimap, speed, reverse, finished

    def step(self, action):

        # 방향 바꿈
        self.pre_direction = change_direction(self.pre_direction, action)

        # Observation을 받아옴
        minimap, speed, reverse, finished = self.observation()

        # 이전 속도와 지금 속도를 비교함
        reward = self.calculate_reward(
            speed,  # speed
            finished,
            reverse
        )

        print("Action : " + printLoc[action] + "        reward : " + str(reward))

        return minimap, reward, finished, {"result": "successfully stepped"}

    def calculate_reward(self, speed, finished, reverse):

        # 기본적으로 프레임당 점수를 깎음 (-0.1)
        # 만약 속도가 100 이하면 더 깎음 (-0.4)
        reward = -0.5 if speed < 100 else -0.1

        # 만약 역주행시 더 깎음
        if reverse:
            reward -= 0.5

        # 만약 완주했으면 1250점을 줌
        if finished:
            reward = 1250

        return reward


class DDPGImageEnv(DetailedMiniMapEnv):
    """Custom Environments follows gym interface"""
    metadata = {'render.modes': ['human']}
    pre_direction = 4

    def __init__(self):
        super(DDPGImageEnv, self).__init__()
        self.action_space = spaces.Box(low=0, high=3, shape=(1, ), dtype=np.float)

    def reset(self):
        return super(DDPGImageEnv, self).reset()

    def observation(self):
        return super(DDPGImageEnv, self).observation()

    def step(self, action):
        if 0.0 <= action < 1.0:
            result = 0
        elif 1.0 <= action < 2.0:
            result = 1
        else:
            result = 2
        action = result
        return super(DDPGImageEnv, self).step(action)

    def calculate_reward(self, speed, finished, reverse):
        return super(DDPGImageEnv, self).calculate_reward(speed, finished, reverse)
