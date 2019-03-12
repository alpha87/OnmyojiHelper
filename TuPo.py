#!/usr/bin/env python
# -*- coding: utf-8 -*-
import time
import random

from DmBase import DmBase
from config import beat_path, win_path


class TuPo(object):

    __doc__ = "结界突破"

    def __init__(self):
        self.dm = DmBase()

    def app_location(self):
        """
        获取前台坐标，并把窗口改为默认大小
        """
        hwnd = self.dm.find_windows("阴阳师-网易游戏")
        self.dm.set_window_size(hwnd)
        return self.dm.get_client_rect(hwnd)

    @property
    def rest(self):
        """
        返回剩余结界券
        """
        windows_location = self.app_location()
        left = windows_location[1]
        top = windows_location[2]
        num = self.dm.ocr(left + 317, top + 530, left + 430, top + 570, "3B3833-3C3833")
        return int(num.split("/")[0])

    def get_pic(self, path, location):
        """
        找图
        """
        kwargs = {
            "left": location[1],
            "top": location[2],
            "right": location[3],
            "down": location[4],
            "pic_path": path,
            "sim": 0.5,
            "dir": 0
        }
        pic_path = self.dm.find_pic_e(**kwargs)
        x, y = pic_path.split("|")[1:]
        return x, y

    def beat_one(self, peo):
        rx = random.randint(-50, 20)
        ry = random.randint(10, 25)
        print("正在选择挑战目标...")
        self.dm.move_to(peo[0], peo[1], x=rx, y=ry)
        time.sleep(1)
        self.dm.left_click()
        print("寻找进攻按钮...")
        time.sleep(random.randint(1, 4))
        windows_location = self.app_location()

        while True:
            x, y = self.get_pic(path=beat_path, location=windows_location)
            if x != "-1" and y != "-1":
                self.dm.move_to(x, y, x=random.randint(1, 10), y=random.randint(1, 5))
                self.dm.left_click()
                print("已找到！")
                break
            time.sleep(3)

        while True:
            print("等待结果...")
            flag = self.find_win_button(windows_location)
            if flag:
                break
            time.sleep(8)

    def find_win_button(self, windows_location):
        x, y = self.get_pic(path=win_path, location=windows_location)
        if x != "-1" and y != "-1":
            print("已胜利！")
            self.dm.move_to(x, y, x=random.randint(1, 5), y=random.randint(1, 5))
            self.dm.left_click()
            time.sleep(5)
            return True
        return False

    def run_app(self):
        windows_location = self.app_location()
        left = windows_location[1]
        top = windows_location[2]

        # 九个挑战目标
        peo1 = left + 279, top + 152
        peo2 = left + 590, top + 136
        peo3 = left + 982, top + 134
        peo4 = left + 360, top + 245
        peo5 = left + 679, top + 251
        peo6 = left + 942, top + 260
        peo7 = left + 384, top + 382
        peo8 = left + 647, top + 373
        peo9 = left + 952, top + 382

        peoples = [peo1, peo2, peo3,
                   peo4, peo5, peo6,
                   peo7, peo8, peo9]

        used = list()
        while len(used) != 9:
            item = random.choice(peoples)
            if item not in used:
                self.beat_one(item)
                used.append(item)
                print(f"攻破记录：{len(used)}")
                print(f"结界挑战券剩余：{self.rest}")

                if self.rest <= 0:
                    print("挑战券不足")
                    break

                # TODO 可能不生效
                if len(used) % 3 == 0:
                    print("攻破记录奖励")
                    self.find_win_button(windows_location)
        print(f"一轮结束，结界挑战券剩余：{self.rest}")

    def main(self):
        if self.rest > 0:
            self.run_app()
        else:
            print(f"挑战券不足，剩余{self.rest}张")


if __name__ == '__main__':
    t = TuPo()
    t.main()
