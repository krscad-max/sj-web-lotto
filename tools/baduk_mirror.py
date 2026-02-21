#!/usr/bin/env python3
"""
Baduk Board Mirror Clicker (macOS)

좌측 바둑판 클릭을 우측 바둑판 동일 상대좌표에 자동 클릭합니다.

Hotkeys:
- F8  : 미러 ON/OFF
- F9  : 재캘리브레이션
- ESC : 종료
"""

import sys
import time
from dataclasses import dataclass

import pyautogui
from pynput import mouse, keyboard


@dataclass
class Rect:
    left: float
    top: float
    right: float
    bottom: float

    @property
    def width(self) -> float:
        return self.right - self.left

    @property
    def height(self) -> float:
        return self.bottom - self.top

    def contains(self, x: float, y: float) -> bool:
        return self.left <= x <= self.right and self.top <= y <= self.bottom


def prompt_point(msg: str):
    print(f"\n{msg}")
    input("커서를 위치시킨 뒤 Enter...")
    p = pyautogui.position()
    print(f"  -> ({p.x}, {p.y})")
    return p.x, p.y


def calibrate() -> tuple[Rect, Rect]:
    print("\n=== 캘리브레이션 시작 ===")
    print("각 바둑판의 좌상단/우하단을 지정합니다.")

    lx1, ly1 = prompt_point("[LEFT] 좌상단")
    lx2, ly2 = prompt_point("[LEFT] 우하단")

    rx1, ry1 = prompt_point("[RIGHT] 좌상단")
    rx2, ry2 = prompt_point("[RIGHT] 우하단")

    left = Rect(min(lx1, lx2), min(ly1, ly2), max(lx1, lx2), max(ly1, ly2))
    right = Rect(min(rx1, rx2), min(ry1, ry2), max(rx1, rx2), max(ry1, ry2))

    if left.width <= 0 or left.height <= 0 or right.width <= 0 or right.height <= 0:
        raise ValueError("잘못된 영역입니다. 다시 캘리브레이션하세요.")

    print("\n[완료] LEFT:", left)
    print("[완료] RIGHT:", right)
    print("=== 캘리브레이션 종료 ===\n")
    return left, right


def map_point(x: float, y: float, src: Rect, dst: Rect) -> tuple[int, int]:
    rx = (x - src.left) / src.width
    ry = (y - src.top) / src.height
    tx = dst.left + rx * dst.width
    ty = dst.top + ry * dst.height
    return int(round(tx)), int(round(ty))


def main():
    print("Baduk Mirror 시작")
    print("※ macOS 접근성/입력 모니터링 권한 필요")

    pyautogui.FAILSAFE = False
    enabled = True

    left_rect, right_rect = calibrate()

    ignore_until = 0.0

    def on_click(x, y, button, pressed):
        nonlocal ignore_until
        if not pressed:
            return
        if time.time() < ignore_until:
            return
        if not enabled:
            return
        if button != mouse.Button.left:
            return
        if not left_rect.contains(x, y):
            return

        tx, ty = map_point(x, y, left_rect, right_rect)
        print(f"L({x:.0f},{y:.0f}) -> R({tx},{ty})")

        # 우리 클릭 이벤트 재귀 방지
        ignore_until = time.time() + 0.12

        cur = pyautogui.position()
        pyautogui.click(tx, ty, button='left')
        pyautogui.moveTo(cur.x, cur.y)

    def on_press(key):
        nonlocal enabled, left_rect, right_rect
        try:
            if key == keyboard.Key.f8:
                enabled = not enabled
                print(f"[STATE] mirror {'ON' if enabled else 'OFF'}")
            elif key == keyboard.Key.f9:
                print("[ACTION] recalibrate")
                left_rect, right_rect = calibrate()
            elif key == keyboard.Key.esc:
                print("[EXIT] 종료")
                return False
        except Exception as e:
            print("keyboard error:", e)

    ml = mouse.Listener(on_click=on_click)
    kl = keyboard.Listener(on_press=on_press)

    ml.start()
    kl.start()

    print("실행 중... (F8 토글 / F9 재설정 / ESC 종료)")
    kl.join()
    ml.stop()


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        pass
    except Exception as e:
        print("오류:", e)
        sys.exit(1)
