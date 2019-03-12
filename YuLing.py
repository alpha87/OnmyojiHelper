#!/usr/bin/env python
# -*- coding: utf-8 -*-
import time
import random

from DmBase import DmBase
from config import ko_path, win_path


class TuPo(object):

    __doc__ = "御灵之境"

    def __init__(self):
        self.dm = DmBase()
        self.window_location = self.app_location()
        self.flag = False

    def app_location(self):
        """
        获取前台坐标，并把窗口改为默认大小
        """
        hwnd = self.dm.find_windows("阴阳师-网易游戏")
        self.dm.set_window_size(hwnd)
        return self.dm.get_client_rect(hwnd)

    @property
    def weekday(self):
        """
        返回当天星期
        """
        return time.strftime("%A")

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
            "sim": 0.8,
            "dir": 0
        }
        pic_path = self.dm.find_pic_e(**kwargs)
        x, y = pic_path.split("|")[1:]
        return x, y

    def beat_one(self, peo):
        if not self.flag:
            rx = random.randint(-20, 20)
            ry = random.randint(1, 50)
            self.dm.move_to(peo[0], peo[1], x=rx, y=ry)
            time.sleep(1)
            self.dm.left_click()
        print("准备挑战...")
        time.sleep(random.randint(2, 5))
        x, y = self.get_pic(ko_path, self.window_location)

        if x != "-1" and y != "-1":
            self.dm.move_to(x, y, x=random.randint(1, 10), y=random.randint(1, 5))
            self.dm.left_click()
            print("开始")

        while True:
            print("等待结果...")
            flag = self.find_win_button(self.window_location)
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
        peo1 = left + 215, top + 355
        peo2 = left + 455, top + 360
        peo3 = left + 690, top + 370
        peo4 = left + 935, top + 365

        item = None
        if self.weekday == "Tuesday":
            item = peo1
        elif self.weekday == "Wednesday":
            item = peo2
        elif self.weekday == "Thursday":
            item = peo3
        elif self.weekday == "Friday":
            item = peo4
        elif self.weekday == "Monday":
            print("周一没得打啊！")

        i = 1
        while i < 10:
            self.beat_one(item)
            self.flag = True
            time.sleep(random.randint(3, 8))
            i += 1
        print("刷了10次了，歇歇吧")

    def main(self):
        self.run_app()


if __name__ == '__main__':
    t = TuPo()
    t.main()
