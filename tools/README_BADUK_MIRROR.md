# Baduk Mirror (좌측 -> 우측 자동 착수)

## 1) 설치
```bash
python3 -m pip install --user pyautogui pynput
```

## 2) 실행
```bash
python3 tools/baduk_mirror.py
```

## 3) 사용법
1. 실행하면 캘리브레이션이 시작됩니다.
2. 안내에 따라 마우스를 위치시키고 Enter를 눌러:
   - LEFT 바둑판 좌상단
   - LEFT 바둑판 우하단
   - RIGHT 바둑판 좌상단
   - RIGHT 바둑판 우하단
3. 이후 좌측 보드 클릭 시 우측에 같은 상대좌표로 자동 클릭됩니다.

## 4) 단축키
- `F8`: ON/OFF 토글
- `F9`: 캘리브레이션 다시
- `ESC`: 종료

## 5) macOS 권한
- 시스템 설정 → 개인정보 보호 및 보안
  - 손쉬운 사용(Accessibility) 허용
  - 입력 모니터링(Input Monitoring) 허용

권한 변경 후 터미널/앱 재실행이 필요할 수 있습니다.
