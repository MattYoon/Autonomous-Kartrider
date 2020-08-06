# Autonomous-Kartrider
건국대 2020 2학기 드림학기제 자율주행 카트라이더

**강화학습: 17학번 이관석** 

**영상처리: 17학번 윤동근**

### 주의사항
- 게임 내 설정 -> 그래픽 -> 그래픽 설정 -> 창모드 ON, 그외 모두 OFF
- 게임 내에서 Tab 키를 눌러 미니맵을 가장 왼쪽 위치로 이동시켜 주세요
- **Python을 관리자 권한으로 실행시켜 주세요(어드민 아닐시 Keyinput.py 사용 불가)**

### 설치 필요 라이브러리
1. cv2 https://pypi.org/project/opencv-python/
2. mss(화면 영상 추출) https://pypi.org/project/mss/

**영상처리 현재 구현사항**
1. 카트라이더 프로그램 윈도우 좌표 파악 및 영상 획득
2. 레이스 시작 카운트 다운 숫자 인식 및 출발 부스터 타이밍에 맞춰 출발

&nbsp;





---
Keyinput.py 사용법 **[Python 관리자 권한으로 실행할 것]**

    from Keyinput import PressKey, ReleaseKey, FORWARD

    PressKey(FORWARD)

    time.sleep(1)

    ReleaseKey(FORWARD)

    #전진에 해당하는 입력이 1초 동안 입력
    #FORWARD 외에도 다른 필요 입력의 Scan Code가 Keyinput에 정의되어 있음
