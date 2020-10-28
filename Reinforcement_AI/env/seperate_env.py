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


def change_direction(pre_direction, direction, env="env2"):
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

    if env == "env1":
        return result

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


# 입력을 따로따로 받는 환경을 만든다.
# Env1은 미니맵이 Observation Space, 방향 3개가 Action Space인 환경 (Action Space를 변경할 수도 있을 것이다)
# Env2는 기타 정보 + Env1의 Action Space가 Observation Space, 최종적으로 방향 3개가 Action Space인 환경
# 학습할 때는 Agent 2개가 있고, Env1을 먼저 돌려서 나온 결과값을 Env2에 넣어서 학습한다.

# Env1 디테일한 설정
# 1.reset은 어떻게 할 것인가?
#   reset은 Env2의 Agent가 reset하라고 하면 reset해야 한다.
#   reset은 step에서 done이 true일 때 실행된다.
#   step에서 done이 true일때를 어떻게 판별하는가? 전역 변수를 두고 설정하는 수밖에 없을듯


# Reset 관련 설정
# 1. Env2에서 Reset명령을 내리면
# 2. 전역 변수로 설정된 Flag가 True로 바뀜
# 3. 이후 Env1에서 해당 전역 변수를 감지함
# 4. Env1에서 제대로 된 Reset 실행


# 전역 변수
global_reset_flag = False       # reset flag
Env1_action = 3                 # Env1의 action 결과
Env1_observated = False
Env2_observated = True


class MinimapEnv(gym.Env):
    """Custom Environments follows gym interface"""
    metadata = {'render.modes': ['human']}
    pre_direction = 4

    def __init__(self):
        super(MinimapEnv, self).__init__()

        # Action Space 설정
        num_of_action_space = 3     # 전, 전+우, 전+좌 3개
        self.action_space = spaces.Discrete(num_of_action_space)

        # Reward range는 일단 설정하지 말아보자

        # Observation Space 설정
        self.observation_space = spaces.Box(low=0, high=1, shape=(102, 179, 3), dtype=np.float)

    def reset(self):
        print('Env1에서 Reset이 호출되었습니다. Image Processing 라이브러리를 통해 Reset합니다.')
        func.release_all()
        reset_env.manualReset()
        ip.ipCountdown()
        func.release_all()
        self.pre_direction = 4   # action 관련 초기화 값. 다르게 줄 수도 있다.
        value = self.observation()      # 다시 미니맵을 관찰한 값을 넘겨준다.

        
        # Reset Flag 재설정
        global global_reset_flag
        global_reset_flag = False
        print("Env1 reset complete")

        return value

    def observation(self):
        # 먼저 미니맵을 가져온다.
        minimap = ip.getSimpleMap() / 255

        # 그대로 return하면 된다.
        return minimap

    def step(self, action):

        print("env1 step")
        # Env2가 observation complete 상태일 때까지 대기
        global Env1_observated
        global Env2_observated
        while not Env2_observated:
            i = 0

        # Env1의 step이 진행되었으므로 True로 변경
        Env1_observated = True
        Env2_observated = False

        # 현재 방향과 저번 방향을 바꿈
        self.pre_direction = change_direction(self.pre_direction, action, env="env1")

        # 전역 변수에 action을 저장
        global Env1_action
        Env1_action = action

        # Observation을 받아옴
        observation = self.observation()

        # 전역변수의 값을 계속 체크해서, 전역 변수가 특정 값이면 reset을 호출함
        global global_reset_flag
        if global_reset_flag:
            print("global reset flag is true")
            self.reset()
            return observation, -10, False, {"result": "Global Reset Flag is True"}

        # 보통의 경우, 보상을 주지 않고, 완주했을 때만 보상을 줌
        reward = self.calculate_reward(observation)
        print("Env1 steped, action is ", action)

        return observation, reward, False, {"result": "Env1 one frame passed"}

    def calculate_reward(self, observation):
        return -0.1


class AllEnv(gym.Env):
    """Custom Environments follows gym interface"""
    metadata = {'render.modes': ['human']}
    pre_direction = 4
    pre_speed = 0

    def __init__(self):
        super(AllEnv, self).__init__()

        # Action Space 설정
        num_of_action_space = 3     # 전, 전+우, 전+좌 3개
        self.action_space = spaces.Discrete(num_of_action_space)

        # Reward range는 일단 설정하지 말아보자

        # Observation Space 설정
        self.observation_space = spaces.Box(low=0, high=1, shape=(5, ), dtype=np.float)

        # 기타 값 설정
        # 플레이어와 중앙선 사이의 전체 비율 측정을 위한, 길의 너비
        self.way_width = 0

    def reset(self):
        # Global reset flag를 true로 바꾸고, reset될때까지 대기
        print('Env2의 Reset이 호출되었습니다. Global Flag를 True로 바꾸고 기다립니다.')
        global global_reset_flag
        global_reset_flag = True
        while global_reset_flag:
            i = 0

        print('Global Flag가 False로 변경되었습니다.')

        # reset이 호출되었으면, 정상적인 observation을 return함.
        self.pre_direction = 4   # action 관련 초기화 값. 다르게 줄 수도 있다.
        value = self.observation()      # 다시 observation 한 값을 return
        return value

    def observation(self):

        # Image Processing에서 값을 받아옴
        way_middle_pos = ip.getOrigin()
        way_dot_pos = ip.getPoints()
        player_pos = ip.getPlayerVertex()
        
        # Env1에서 값을 가져옴
        global Env1_action

        # 값을 가공함
        speed = min(ip.getSpeed() / 250, 1)
        curved = min((way_dot_pos[0][0] - way_dot_pos[2][0]) + (way_dot_pos[1][0] - way_dot_pos[3][0]), 1)
        middle_diff = min(abs(way_middle_pos[0] - player_pos[0])/80, 1)
        reverse = 1 if ip.getReverse() else 0
        e1_act = Env1_action / 2

        # 추가로 저장해야 할 값 설정
        self.way_width = abs(way_dot_pos[2][0] - way_dot_pos[3][0])

        # 그대로 return
        return np.array([speed, curved, middle_diff, reverse, e1_act])

    def step(self, action):

        print("env2 step")

        # Env2가 observation complete 상태일 때까지 대기
        global Env1_observated
        global Env2_observated
        while not Env1_observated:
            i = 0

        # Env2의 step이 진행되었으므로 True로 변경
        Env1_observated = False
        Env2_observated = True

        # 현재 방향과 저번 방향을 바꿈
        self.pre_direction = change_direction(self.pre_direction, action, env="env2")

        # Observation을 받아옴
        observation = self.observation()

        # reset을 호출하는 경우
        # 속도가 0일 때
        if observation[0] == 0:
            print("Crashed to the wall, Env2 reset will called")
            observation = self.reset()
            return observation, -10, False, {"result": "crashed to the wall"}
        # 역주행할 때
        if observation[3] == 1:
            print("Reverse Racing! Env2 reset will called")
            observation = self.reset()
            return observation, -20, False, {"result" : "Reverse racing"}

        # 이전 속도와 지금 속도를 비교함
        reward = self.calculate_reward(
            observation[0],     # speed
            observation[2]     # middle_diff
        )
        self.pre_speed = observation[0]

        # 보통의 경우, 보상을 주지 않고, 완주했을 때만 보상을 줌
        print("env2 action called, action : ", action, "  reward : ", reward)

        return observation, reward, False, {"result": "Env1 one frame passed"}

    def calculate_reward(self, speed, middle_diff):
        # 프레임당 점수를 깎을 수 있으나, 비효율적일 것임

        # reward값 설정
        reward = 0

        # 플레이어가 맵 밖으로 나갔는지 측정
        out_of_track = True if middle_diff * 80 * 2 > self.way_width else False

        # 속도 달라짐 정도 측정
        speed_diff = speed - self.pre_speed

        # 미니맵의 길에서 유저가 벗어났을 때
        reward += 1 if not out_of_track else -5

        # 속도 비교해서 증가하거나 그대로면 +1, 아니면 0점
        reward += 1 if speed_diff >= 0.0 else 0

        # 전진만 하는 걸 막는 부분. 벽에 부딛히면 속도가 떨어지는 점을 이용해, 100 이하는 -를 준다.
        reward -= 4 if speed < 0.4 else 0

        return reward





