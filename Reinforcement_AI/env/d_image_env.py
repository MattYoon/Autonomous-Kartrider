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
    pre_speed = 0

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
        minimap, _, _, _ = self.observation()
        return minimap

    def observation(self):
        minimap = ip.getSimpleMap() / 255
        print(minimap.shape)

        # Image Processing에서 값을 받아옴
        way_middle_pos = ip.getOrigin()
        way_dot_pos = ip.getPoints()
        player_pos = ip.getPlayerVertex()

        # 값을 가공함
        speed = min(ip.getSpeed() / 250, 1)
        middle_diff = min(abs(way_middle_pos[0] - player_pos[0]) / 80, 1)
        reverse = ip.getReverse()

        # 추가로 저장해야 할 값 설정
        self.way_width = abs(way_dot_pos[2][0] - way_dot_pos[3][0])
        self.way_player_diff = max(abs(way_dot_pos[2][0] - player_pos[0]), abs(way_dot_pos[3][0] - player_pos[0]))

        # 그대로 return
        return minimap, speed, middle_diff, reverse

    def step(self, action):

        # 방향 바꿈
        self.pre_direction = change_direction(self.pre_direction, action)

        # Observation을 받아옴
        minimap, speed, middle_diff, reverse = self.observation()

        # reset 호출하는 경우
        # 속도가 30 이하일 때 (보통 벽에 부딛혔을 때)
        if speed < 0.12:
            print("Crashed to the wall or speed is < 30, Reset")
            minimap = self.reset()
            return minimap, -10, False, {"result": "reset called"}
        # 역주행시
        if reverse:
            print("Reverse Racing")
            minimap = self.reset()
            return minimap, -20, False, {"result": "reset called"}

        # 이전 속도와 지금 속도를 비교함
        reward = self.calculate_reward(
            speed,  # speed
            middle_diff  # middle_diff
        )
        self.pre_speed = speed

        print("Action : " + printLoc[action] + "        reward : " + str(reward))

        return minimap, reward, False, {"result": "successfully stepped"}

    def calculate_reward(self, speed, middle_diff):
        # 프레임당 점수를 깎을 수 있으나, 비효율적일 것임

        # reward값 설정
        reward = 0.0

        # 플레이어가 맵 밖으로 나갔는지 측정
        out_of_track = True if middle_diff * 80 * 2 > self.way_width or self.way_player_diff > self.way_width else False

        # 속도 달라짐 정도 측정
        speed_diff = speed - self.pre_speed

        # 미니맵의 길에서 유저가 벗어났을 때
        reward += 1 if not out_of_track else -5

        # 속도 비교해서 증가하거나 그대로면 +0.1, 아니면 0점
        reward += 0.1 if speed_diff >= 0.0 else 0

        # 전진만 하는 걸 막는 부분. 벽에 부딛히면 속도가 떨어지는 점을 이용해, 100 이하는 -를 준다.
        reward -= 4 if speed < 0.4 else 0

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

    def calculate_reward(self, speed, middle_diff):
        return super(DDPGImageEnv, self).calculate_reward(speed, middle_diff)
