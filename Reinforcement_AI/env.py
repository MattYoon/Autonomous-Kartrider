import Image_Processing.image_processing as ip
import keyinput
import threading
import time
import gym
from gym import spaces

# 직진 0, 오른쪽 1, 뒤쪽 2, 왼쪽 3
directLoc = [keyinput.FORWARD, keyinput.RIGHT, keyinput.BACK, keyinput.LEFT]

# 직+오 4, 뒤+오 5, 뒤+좌 6, 직+좌 7
complexLoc = [[directLoc[0], directLoc[1]],
              [directLoc[2], directLoc[1]],
              [directLoc[2], directLoc[3]],
              [directLoc[3], directLoc[1]]]





def go_forward():
    # thread = threading.Thread(target=keyinput.PressKey, args=[keyinput.FORWARD])
    # time.sleep(3)
    # thread.start()8

    print("origin : ", ip.getOrigin())
    # print("originshape : ", ip.getOrigin().shape)
    playercon = ip.getPlayerCon()
    print("playercon : ", playercon)
    print(len(playercon), len(playercon[0]), len(playercon[0][0]))

go_forward()


def get_highest(loc):
    for i in range(len(loc)):
        if loc[i][0][1] == 57:
            return loc[i][0][0]


class CustomEnv(gym.Env):
    """Custom ENV follows gym interface"""
    metadata = {'render.modes': ['human']}

    pre_speed = 0

    def __init__(self, arg1, arg2):
        super(CustomEnv, self).__init__()

        # Reward 설정
        self.reward_range = (0, 1)

        # Describe Action space (방향 움직임, 총 8방향)
        self.action_space = spaces.Discrete(8)

        # Describe Observation space
        # Box(3, ) 정도? -> 파란선과 플레이어의 거리, 속도, 앞으로의 길의 방향성 (어느쪽으로 휘어있는지)
        self.observation_space = spaces.Box(2, )




    def reset(self):
        pass
        # 추후에 마우스를 이용할 수 있으면, 환경을 재설정하는 코드를 넣어두자

    def step(self, action):
        self.go_direction(action)

        wanted = ip.getOrigin()[0]
        player = get_highest(ip.getPlayerCon())

        diff_reward = 1 if abs(wanted-player) < 20 else -1
        speed = ip.getSpeed()
        speed_reward = 1 if self.pre_speed < speed else -1
        pre_speed = speed


        reward = diff * 0.1




        pass

    def go_direction(self, direction):
        self.go_onedirection(direction) if direction < 4 else self.go_complex(direction)

    def go_onedirection(self, direction):
        thread = threading.Thread(target=keyinput.PressAndRelease, args=[directLoc[direction], 1])
        thread.start()

    def go_complex(self, direction):
        thread1 = threading.Thread(target=keyinput.PressAndRelease, args=[complexLoc[direction + 4][0], 1])
        thread2 = threading.Thread(target=keyinput.PressAndRelease, args=[complexLoc[direction + 4][1], 1])
        thread1.start()
        thread2.start()

    def render(self, mode='human'):
        pass

    def close(self):
        pass
