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


class BoxKartEnv(gym.GoalEnv):
    """Custom Environments follows gym interface"""
    metadata = {'render.modes': ['human']}
    pre_direction = 4
    pre_speed = 0

    def __init__(self):
        super(BoxKartEnv, self).__init__()

        # Action Space 설정
        number_of_actions = 3
        self.action_space = spaces.Discrete(number_of_actions)

        self.reward_range = (0, 1)

        # Observation Space 설정
        # Observation시, 미니맵을 가상화한 것을 그대로 보여주는게 나을거같은데...
        # 하얀색 배경에 선을 그려서 일종의 가상화된 맵을 그려주면 좋을듯
        # self.observation_space_1 = spaces.Box(low=0, high=255, shape=([minimap_height, minimap_width, 3], 1, ), dtype=np.uint8)
        self.observation_space_2 = spaces.Tuple((
            spaces.Box(low=0, high=255, shape=(102, 179, 3), dtype=np.uint8),   # minimap
            spaces.Box(low=0, high=300, shape=(1, ), dtype=np.uint8),           # speed
            spaces.Box(low=0, high=200, shape=(1, ), dtype=np.uint8),           # mid_diff
            spaces.Box(low=-100, high=100, shape=(1, ), dtype=np.uint8),        # road_diff
            spaces.Box(low=0, high=1, shape=(1, ), dtype=np.uint8)              # reversed
        ))
        # self.observation_space = flatdim(self.observation_space_2)
        self.observation_space = spaces.Box(low=-np.inf, high=np.inf, shape=(54778, ), dtype=np.float32)

    def reset(self):
        print('Reset Called, reset environment')
        func.release_all()
        reset_env.manualReset()
        ip.ipCountdown()
        func.release_all()
        self.pre_direction = 4
        value = self.observation()[0]
        print(value)
        return value

    def observation(self):
        # 미니맵 정보를 완전히 받아오는 무언가의 함수
        minimap = np.ravel(list(ip.getSimpleMap()), order='C')
        # print(minimap.shape)
        # print(minimap)
        way_middle_pos = (ip.getOrigin())
        way_dot_pos = ip.getPoints()
        player_pos = ip.getPlayerVertex()
        speed = np.array([ip.getSpeed()])
        reverse = np.array([1 if ip.getReverse() else 0])

        curved = np.array([(way_dot_pos[0][0] - way_dot_pos[2][0]) + (way_dot_pos[1][0] - way_dot_pos[3][0])])
        middle_diff = np.array([abs(way_middle_pos[0] - player_pos[0])])

        way_down_length = abs(way_dot_pos[2][0] - way_dot_pos[3][0])

        # print(speed, middle_diff, curved, reverse)

        result = np.concatenate((minimap, speed, middle_diff, curved, reverse))
        result = np.array(result, dtype=np.float32)
        return result, speed, reverse, middle_diff, way_down_length

        # result = (minimap,
        #           np.array(speed, dtype=np.uint8),
        #           np.array(middle_diff, dtype=np.uint8),
        #           np.array(curved, dtype=np.uint8),
        #           np.array(reverse, dtype=np.uint8))

    def step(self, action):
        self.pre_direction = change_direction(self.pre_direction, action)

        observation, speed, reverse, middle_diff, way_down_length = self.observation()
        complete = False

        # 게임 종료에 관한 부분
        if speed == 0:
            # 속도가 0일 때 (벽에 부딛혔을 때)
            print("Crashed to the wall!")
            return observation, -10, True, {"direction": printLoc[action]}
        if complete:
            # 만약 게임을 완료했다면
            print("Complete Racing!")
            return observation, 500, complete, {"status": "Complete!"}

        # 여기서 pre_speed와 현재 speed를 비교해야 한다
        reward = self.calculate_reward(
            speed[0],
            reverse[0],
            middle_diff[0],
            way_down_length)
        self.pre_speed = speed[0]

        # 각 Step을 print
        print(reward, complete, printLoc[action])
        return observation, reward, complete, {"direction": printLoc[action]}

    def calculate_reward(self, speed, reversed, middle_diff, way_down_length):
        # 프레임당 점수를 깎을 수 있으나, 비효율적이라 생각됨
        reward = 0

        out_of_track = True if middle_diff * 2 > way_down_length else False
        # print("speed_diff :", speed, " ", self.pre_speed)
        speed_diff = speed - self.pre_speed
        reverse = 1 if reversed else 0

        # 미니맵의 길에서 유저가 벗어났을 때
        # 미니맵 플레이어의 위치가 실제 트랙의 위치와 같지 않으므로, 외곽선에 붙거나 하면 넘어갈 수 있음
        # 일종의 충돌 체크용
        # 어떻게 구현할 것이냐?
        # 플레이어의 화살표는 원래 외곽점들의 집합으로 주어지므로, 외곽점들의 집합이 길 안에 속해있는 범위로 계산
        # 예를 들어, 외곽점 집합의 70%가 안에 속해있다면, reward는 -0.6이 됨 (100%가 밖에있다면 -2)
        if out_of_track:
            reward -= 4
        else:
            reward += 1

        # 속도 비교. 속도가 증가하거나 그대로이면 점수를 1 주고, 속도가 줄어들때엔 reward를 주지 않는다.
        # print("speed diff : ", speed_diff)
        if speed_diff >= 0:
            reward += 1
        else:
            pass
        # reward += 1 if speed_diff >= 0 else None

        # 전진만 하는 걸 막는 부분. 벽에 부딛히면 속도가 떨어지는 점을 이용해, 100 이하는 -를 준다.
        if speed < 100:
            reward -= 4

        # 뒤로 가는지 비교. 뒤로 갈때는 패널티를 많이 줘야 한다.
        if reverse:
            reward -= 20

        return reward
