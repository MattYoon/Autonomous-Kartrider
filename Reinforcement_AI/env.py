import time

import gym
from gym import error, spaces, utils
import Image_Processing.image_processing as ip
import numpy as np
import keyinput
import reset_env
from collections import deque

# 012 -> 직진, 정지, 후진
# 012 -> 우회전, 방향전환없음, 좌회전
fb_direction = [keyinput.FORWARD, 0, keyinput.BACK]
rl_direction = [keyinput.RIGHT, 0, keyinput.LEFT]

# 0 전진, 1 전+우, 2 전+좌, 3 우, 4 좌, 5 후, 6 후+우, 7 후+좌, 8 정지
direction_9 = [
    [fb_direction[0], rl_direction[0]],     # 전+우
    [fb_direction[0], rl_direction[1]],     # 전진
    [fb_direction[0], rl_direction[2]],     # 전+좌
    [fb_direction[1], rl_direction[0]],     # 우
    [fb_direction[1], rl_direction[1]],     # 정지
    [fb_direction[1], rl_direction[2]],     # 좌
    [fb_direction[2], rl_direction[0]],     # 후+우
    [fb_direction[2], rl_direction[1]],     # 후진
    [fb_direction[2], rl_direction[2]]]     # 후+좌

printLoc = [
    "전 + 우",
    "전진",
    "전 + 좌",
    "우회전",
    "정지",
    "좌회전",
    "후 + 우",
    "후진",
    "후 + 좌"]



def press_onekey(direction):
    None if direction == 0 else keyinput.PressKey(direction)
    # thread = threading.Thread(target=keyinput.PressKey, args=[direction])
    # thread.start()


def release_onekey(direction):
    None if direction == 0 else keyinput.ReleaseKey(direction)
    # thread = threading.Thread(target=keyinput.ReleaseKey, args=[direction])
    # thread.start()


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
        press_onekey(direction[0])
        release_onekey(pre_direction[0])

    if pre_direction[1] == direction[1]:
        pass
    else:
        press_onekey(direction[1])
        release_onekey(pre_direction[1])

    return result


class KartEnv(gym.Env):
    """Custom ENV follows gym interface"""
    metadata = {'render.modes': ['human']}
    pre_direction = 4
    speed_queue = deque()

    def __init__(self):
        super(KartEnv, self).__init__()

        # Reward 설정
        self.reward_range = (0, 1)

        # Describe Action space (방향 움직임, 총 9방향 (정지까지 포함))
        self.action_space = spaces.Discrete(5)

        # Describe Observation space
        # Box(3, ) 정도? -> 파란선과 플레이어의 거리, 속도, 앞으로의 길의 방향성 (어느쪽으로 휘어있는지)
        self.observation_space = spaces.Box(low=0, high=200, shape=(3,), dtype=np.int32)

        self.speed_queue.append(-10)
        self.speed_queue.append(-10)

    def reset(self):
        # 에피소드의 시작에 불려지며, observation을 돌려준다
        self.speed_queue.clear()
        self.speed_queue.append(-10)
        self.speed_queue.append(-10)
        reset_env.manualReset()
        ip.ipCountdown()

        # get_observation
        # while reset_env.isReset():
        #     i = 0
        road_center = ip.getOrigin()
        road_points = ip.getPoints()
        player_pos = ip.getPlayerVertex()
        road_diff = self.get_road_diff(road_points)

        # observation은 총 3개 - [ 중앙의 정도, 속도, 길의 커브정도] 로 오고
        # 보상으로 중앙의 정도에 대한 보상(reward_diff), 속도에 대한 보상(reward_speed), 거꾸로 갈 때 음수를 주는 보상(reward_backward)이 온다.
        reward_diff, diff = self.reward_player_reddot_diff(road_center, player_pos, road_points, road_diff)

        observation = np.array([diff, -10, road_diff])
        print(observation, self.speed_queue)
        return observation

    def step(self, action):
        # environment에 action을 취하는 것이며
        # 다음 관찰, 보상, 에피소드가 종료되었는지, 기타 정보 4개를 return한다.

        start_step = time.time()
        self.pre_direction = change_direction(self.pre_direction, action)

        road_center = ip.getOrigin()
        road_points = ip.getPoints()
        player_pos = ip.getPlayerVertex()
        reverse = ip.getReverse()
        cur_speed = ip.getSpeed()
        road_diff = self.get_road_diff(road_points)

        self.speed_queue.popleft()
        self.speed_queue.append(cur_speed)

        if self.speed_queue[0] == 0 and self.speed_queue[1] == 0:
            print("Manual Reset Called", self.speed_queue)
            self.reset()


        # observation은 총 3개 - [ 중앙의 정도, 속도, 길의 커브정도] 로 오고
        # 보상으로 중앙의 정도에 대한 보상(reward_diff), 속도에 대한 보상(reward_speed), 거꾸로 갈 때 음수를 주는 보상(reward_backward)이 온다.
        reward_diff, diff = self.reward_player_reddot_diff(road_center, player_pos, road_points, road_diff)
        reward_speed_diff = self.reward_speed_diff()
        reward_backward = self.reward_going_back(reverse)

        observation = np.array([diff, cur_speed, road_diff])

        while True:
            end_time = time.time()
            if end_time - start_step > 0.5:
                break

        self.pre_speed = cur_speed

        print(observation, reward_diff + reward_speed_diff + reward_backward, False, {'direction' : printLoc[action]})
        return observation, reward_diff + reward_speed_diff + reward_backward, False, {'direction' : printLoc[action]}

    def render(self, mode='human'):
        # 이건 사람이 볼 수 있게끔 에이전트를 visualize 하는건데, 이건 필요 없을듯(print 찍게하면 될거같음)
        pass

    def close(self):
        pass

    def get_road_diff(self, waypoints):
        value = abs(waypoints[0][0] - waypoints[2][0]) + abs(waypoints[1][0] - waypoints[3][0])
        return value if value < 200 else 200

    def reward_player_reddot_diff(self, reddot, player, waypoints, road_diff):
        way_width = abs(waypoints[2][0] - waypoints[3][0])
        wayup_width = abs(waypoints[1][0] - waypoints[0][0])
        diff = abs(reddot[0] - player[0])
        print("way_width : ", way_width, " wayup_width : ", wayup_width, " diff : ", diff, " road_diff : ", road_diff)
        if wayup_width * 3 > way_width and diff < way_width * 0.50:    # 시작점 기준
            return 2, diff
        if diff < way_width * 0.50 and road_diff < 30:      # 길이 좁고 직선형일떄
            return 2, diff
        if road_diff > 100 and diff < way_width * 0.6:      # 커브길일때
            return 2, diff

        else:
            return -5, diff

    def reward_speed_diff(self):
        if self.speed_queue[0] < self.speed_queue[1]:
            reward = 1
        elif self.speed_queue[0] == self.speed_queue[1]:
            reward = 0.2
        else:
            reward = 0
        return reward

    def reward_going_back(self, reverse):
        if reverse:
            return -10
        else:
            return 0
