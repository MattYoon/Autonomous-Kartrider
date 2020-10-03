import gym
from gym import error, spaces, utils
# import Image_Processing.image_processing as ip
import numpy as np
import keyinput
import threading
import datetime


# 직진 0, 오른쪽 1, 뒤쪽 2, 왼쪽 3
directLoc = [keyinput.FORWARD, keyinput.RIGHT, keyinput.BACK, keyinput.LEFT]

# 직+오 4, 뒤+오 5, 뒤+좌 6, 직+좌 7
complexLoc = [[directLoc[0], directLoc[1]],
              [directLoc[2], directLoc[1]],
              [directLoc[2], directLoc[3]],
              [directLoc[3], directLoc[1]]]


class KartEnv(gym.Env):
    """Custom ENV follows gym interface"""
    metadata = {'render.modes': ['human']}

    pre_speed = 0

    def __init__(self, arg1, arg2):
        super(KartEnv, self).__init__()

        # Reward 설정
        self.reward_range = (0, 1)

        # Describe Action space (방향 움직임, 총 8방향)
        self.action_space = spaces.Discrete(8)

        # Describe Observation space
        # Box(3, ) 정도? -> 파란선과 플레이어의 거리, 속도, 앞으로의 길의 방향성 (어느쪽으로 휘어있는지)
        self.observation_space = spaces.Box(low=0, high=200, shape=(3, ), dtype=np.int32)




    def reset(self):
        # 에피소드의 시작에 불려지며, observation을 돌려준다
        self.pre_speed = 0
        # 추후에 마우스를 이용할 수 있으면, 환경을 재설정하는 코드를 넣어두자

        # get_observation
        observation = np.array([1, 200, self.get_raod_diff(((0, 0), (100, 0), (50, 0), (100, 50)))])
        return observation

    def step(self, action):
        # environment에 action을 취하는 것이며
        # 다음 관찰, 보상, 에피소드가 종료되었는지, 기타 정보 4개를 return한다.

        start_step = datetime.datetime.now()

        # self.go_direction(action)

        road_center = (50, 50)# ip.getOrigin()
        road_points = ((0, 0), (100, 0), (50, 0), (100, 50))# ip.getPoints()
        player_pos = (50, 55)# ip.getPlayerVertex()
        reverse = False# ip.getReverse()
        cur_speed = 100# ip.getSpeed()

        # observation은 총 3개 - [ 중앙의 정도, 속도, 길의 커브정도] 로 오고
        # 보상으로 중앙의 정도에 대한 보상(reward_diff), 속도에 대한 보상(reward_speed), 거꾸로 갈 때 음수를 주는 보상(reward_backward)이 온다.
        reward_diff, diff = self.reward_player_reddot_diff(road_center, player_pos, road_points)
        reward_speed_diff = self.reward_speed_diff(cur_speed)
        reward_backward = self.reward_going_back(reverse)

        observation = np.array([diff, cur_speed, self.get_raod_diff(road_points)])

        while datetime.datetime.now() - start_step >= datetime.timedelta(seconds=1.0):
            pass

        return observation, reward_diff + reward_speed_diff + reward_backward, False, {}



    def render(self, mode='human'):
        # 이건 사람이 볼 수 있게끔 에이전트를 visualize 하는건데, 이건 필요 없을듯(print 찍게하면 될거같음)
        pass

    def close(self):
        pass



    def get_raod_diff(self, waypoints):
        value = abs(waypoints[0][0] - waypoints[2][0]) + abs(waypoints[1][0] - waypoints[3][0])
        return value if value < 200 else 200


    def reward_player_reddot_diff(self, reddot, player, waypoints):
        way_width = abs(waypoints[2][0] - waypoints[3][0])
        diff = abs(reddot[0] - player[0])
        if diff < way_width * 0.15:
            return 1, diff
        else:
            return -0.5, diff

    def reward_speed_diff(self, speed):
        if self.pre_speed < speed:
            reward = 1
        elif self.pre_speed == speed:
            reward = 0.2
        else:
            reward = -1
        self.pre_speed = speed
        return reward

    def reward_going_back(self, reverse):
        if reverse:
            return -10
        else:
            return 0


    def go_direction(self, direction):
        self.go_onedirection(direction) if direction < 4 else self.go_complex(direction)

    def go_onedirection(self, direction):
        thread = threading.Thread(target=keyinput.PressAndRelease, args=[directLoc[direction], 1])
        thread.start()

    def go_complex(self, direction):
        thread1 = threading.Thread(target=keyinput.PressAndRelease, args=[complexLoc[direction - 4][0], 1])
        thread2 = threading.Thread(target=keyinput.PressAndRelease, args=[complexLoc[direction - 4][1], 1])
        thread1.start()
        thread2.start()