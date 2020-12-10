# Autonomous-Kartrider
건국대 2020 2학기 드림학기제 자율주행 카트라이더

**강화학습: 17학번 이관석** 

**영상처리: 17학번 윤동근**

### 주의사항 및 실행방법
- 게임 내 설정 -> 그래픽 -> 그래픽 설정 -> 창모드 ON, 그외 모두 OFF
- 게임 내에서 Tab 키를 눌러 미니맵을 가장 왼쪽 위치로 이동시켜 주세요
- **Python을 관리자 권한으로 실행시켜 주세요(어드민 아닐시 Keyinput.py 사용 불가)**
- 맵 로드 직전 창에서 "고스트 사용" 해제
- 모니터의 해상도를 1920x1080 (FHD) 로 설정해주세요
- 현재 지원하는 맵은 "사막 버려진 오아시스" 하나입니다. 다른 맵에서는 동작하지 않습니다.

모든 설정이 완료되면, 프로젝트 최상위 폴더의 main.py를 실행시켜 주세요.
main.py 안의 agent, env 변수 (`if __name__ == "__main__"` 블록 밑에 있음) 를 변경해 환경과 에이전트를 바꿀 수 있습니다.

### 설치 필요 라이브러리

1. OpenCV(cv2) https://pypi.org/project/opencv-python/
2. mss(화면 영상 추출) https://pypi.org/project/mss/
3. pywin32(키보드 입력)
4. pyautoit(마우스 입력)
5. tensorflow(1.14 버전, 강화학습 에이전트 의존성 때문)
6. stable-baselines(강화학습 베이스라인 코드)
7. numpy(1.19.2 버전으로 설치)

아래 명령어로 한번에 설치할 수 있습니다.
```bash
pip install opencv-python mss pywin32 pyautoit tensorflow==1.14 stable-baselines numpy==1.19.2
```


**영상처리 현재 구현사항**
1. 카트라이더 프로그램 윈도우 좌표 파악 및 영상 획득
2. 레이스 시작 카운트 다운 숫자 인식 및 출발 부스터 타이밍에 맞춰 출발
3. 미니맵을 통한 앞으로의 진행 path, 사용자 현재 위치 등 획득
4. 현재 속도 획득
5. 역주행 중인지 판별

&nbsp;





---
Keyinput.py 사용법 

    from Keyinput import PressKey, ReleaseKey, FORWARD
    
    PressKey(FORWARD)
    time.sleep(1)
    ReleaseKey(FORWARD)

    #전진에 해당하는 키가 1초 동안 입력
    #FORWARD 외에도 다른 필요 키의 Scan Code가 Keyinput에 정의되어 있음
