# -*- coding: utf-8 -*-
'''
Author       : ZakiuC
Date         : 2024-01-04 14:00:59
LastEditors  : ZakiuC z2337070680@163.com
LastEditTime : 2024-01-11 16:04:51
FilePath     : \yys\loadModel.py
Description  : 目标图片加载，用于模板匹配，附带键盘/鼠标模拟输入
Copyright (c) 2024 by ZakiuC z2337070680@163.com, All Rights Reserved. 
'''
import cv2
import os
from ctypes import windll, byref
from ctypes.wintypes import HWND, POINT, RECT
import string
import time
import random
import numpy as np


# 获取当前文件的绝对路径
current_file_path = os.path.abspath(__file__)
# 获取当前文件所在目录的路径
current_dir = os.path.dirname(current_file_path)
# 构建到 static/images/ 的路径
path_to_images = os.path.join(current_dir, "static", "images")


def map_to_original(click_pos_x, click_pos_y, origin_width, origin_height):
    """
    将点击位置映射到原始窗口
    click_pos_x: 点击位置的横坐标
    click_pos_y: 点击位置的纵坐标
    origin_width: 原始窗口宽度
    origin_height: 原始窗口高度
    return 原始窗口中的点击位置
    """
    # 新窗口分辨率
    new_width, new_height = 640, 361

    # 计算宽度和高度的缩放比例
    scale_x = origin_width / new_width
    scale_y = origin_height / new_height

    # 将点击位置映射到原始窗口
    original_click_x = int(click_pos_x * scale_x)
    original_click_y = int(click_pos_y * scale_y)

    return original_click_x, original_click_y


class TargetImage:
    def __init__(self, image_name, threshold = 0.8):
        """
        image_name: 模板图像名称
        threshold: 匹配阈值
        """
        self.image = cv2.imread(path_to_images + "/" + image_name)
        self.height, self.width = self.image.shape[:2]
        self.threshold = threshold

    def match(self, main_image, method=cv2.TM_CCOEFF_NORMED):
        """
        在图像中查找模板
        main_image: 待查找的图像
        method: 匹配方法
        return: 返回匹配结果的左上角和右下角坐标, 如果未找到返回None
        """
        result = cv2.matchTemplate(main_image, self.image, method)
        min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)
        # 判断匹配分数
        self.score = max_val
        if self.score >= self.threshold:
            top_left = max_loc  # 使用最大值位置作为左上角坐标
            bottom_right = (top_left[0] + self.width, top_left[1] + self.height)  # 计算右下角坐标
            self.pos_x = top_left[0] + self.width // 2
            self.pos_y = top_left[1] + self.height // 2

            return top_left, bottom_right
        else:
            return None
    
    def match_all(self, main_image, method=cv2.TM_CCOEFF_NORMED, threshold=None):
        """
        在图像中查找所有匹配模板的位置
        main_image: 待查找的图像
        method: 匹配方法
        threshold: 匹配分数阈值，仅返回高于此分数的匹配结果
        return: 返回所有匹配结果的左上角和右下角坐标列表，如果未找到返回空列表
        """
        result = cv2.matchTemplate(main_image, self.image, method)
        if threshold is None:
            threshold = self.threshold  # 使用对象的阈值属性

        # 获取所有匹配分数超过阈值的位置
        locations = np.where(result >= threshold)
        matches = []

        for loc in zip(*locations[::-1]):  # *locations[::-1] 转换为x,y坐标
            top_left = loc
            bottom_right = (top_left[0] + self.width, top_left[1] + self.height)
            matches.append((top_left, bottom_right))

        return matches

    def click(self, handle: HWND, offset_x=15, offset_y=15, duration=0.027, offset_duration=0.03, waitCD=0.7, offset_waitCD=0.3):
        """在指定窗口中点击模板图像的中心点

        Args:
            handle (HWND): 窗口句柄
            offset_x (int, optional): 横向偏移量. 默认为15.
            offset_y (int, optional): 纵向偏移量. 默认为15.
            duration (float, optional): 按下和放开的时间间隔. 默认为0.027.
            offset_duration (float, optional): 时间间隔的随机偏移量. 默认为0.03.
            waitCD (float, optional): 点击后等待时间. 默认为0.7.
            offset_waitCD (float, optional): 等待时间的随机偏移量. 默认为0.3.
            retrun (list): 返回点击位置的坐标
        """
        rect = RECT()
        windll.user32.GetWindowRect(handle, byref(rect))
        original_width = rect.right - rect.left
        original_height = rect.bottom - rect.top
        click_pos_x = self.pos_x + random.randint(-offset_x, offset_x)
        click_pos_y = self.pos_y + random.randint(-offset_y, offset_y)
        # 映射到原始窗口坐标
        original_click_x, original_click_y = map_to_original(click_pos_x, click_pos_y, original_width, original_height)
        press_duration = duration + random.uniform(0.0, offset_duration)
        wait_time = waitCD + random.uniform(0.0, offset_waitCD)
        left_down(handle, original_click_x, original_click_y)
        time.sleep(press_duration)
        left_up(handle, original_click_x, original_click_y)
        time.sleep(wait_time)
        return [(click_pos_x, click_pos_y), (original_click_x, original_click_y)]



# 加载图像和模板
# 庭院底部菜单未展开
home_bottom_menu_close = TargetImage("home_bottom_menu_close.png")
# 庭院底部菜单已展开
home_bottom_menu_open = TargetImage("home_bottom_menu_open.png")
# 庭院底部菜单 - 式神录
home_bottom_menu_shishenlu = TargetImage("home_bottom_menu_obj1.png")
# 庭院底部菜单 - 阴阳术
home_bottom_menu_yinyangshu = TargetImage("home_bottom_menu_obj2.png")
# 庭院底部菜单 - 好友
home_bottom_menu_haoyou = TargetImage("home_bottom_menu_obj3.png")
# 庭院底部菜单 - 花合战
home_bottom_menu_huahz = TargetImage("home_bottom_menu_obj4.png")
# 庭院底部菜单 - 商店
home_bottom_menu_shangdian = TargetImage("home_bottom_menu_obj5.png")
# 庭院底部菜单 - 阴阳寮
home_bottom_menu_yinyangliao = TargetImage("home_bottom_menu_obj6.png")
# 庭院底部菜单 - 组队
home_bottom_menu_zudui = TargetImage("home_bottom_menu_obj7.png")
# 庭院底部菜单 - 同心队
home_bottom_menu_tongxindui = TargetImage("home_bottom_menu_obj8.png")
# 庭院底部菜单 - 珍旅居
home_bottom_menu_zhenlvju = TargetImage("home_bottom_menu_obj9.png")
# 庭院底部菜单 - 图鉴
home_bottom_menu_tujian = TargetImage("home_bottom_menu_obj10.png")
# 庭院顶部UI - 金币
home_top_ui_jinbi = TargetImage("home_up_ui_money.png")
# 庭院顶部UI - 勾玉
home_top_ui_gouyu = TargetImage("home_up_ui_magatama.png")
# 庭院顶部UI - 体力
home_top_ui_tili = TargetImage("home_up_ui_stamina.png")
# 庭院中部町中图标
home_machinaka = TargetImage("Machinaka.png")
# 庭院中部探索图标
home_exploratory = TargetImage("home_exploratory.png")
# 探索 - [妖]图标
exploratory_goblin_tag = TargetImage("exploratory_goblin_tag.png")
# 探索底部菜单 - 觉醒材料
exploratory_bottom_menu_obj1 = TargetImage("exploratory_bottom_menu_obj1.png")
# 探索底部菜单 - 御魂
exploratory_bottom_menu_obj2 = TargetImage("exploratory_bottom_menu_obj2.png")
# 探索底部菜单 - 结界突破
exploratory_bottom_menu_obj3 = TargetImage("exploratory_bottom_menu_obj3.png")
# 探索底部菜单 - 御灵
exploratory_bottom_menu_obj4 = TargetImage("exploratory_bottom_menu_obj4.png")
# 探索底部菜单 - 式神委派
exploratory_bottom_menu_obj5 = TargetImage("exploratory_bottom_menu_obj5.png")
# 探索底部菜单 - 秘闻副本
exploratory_bottom_menu_obj6 = TargetImage("exploratory_bottom_menu_obj6.png")
# 探索底部菜单 - 地域鬼王
exploratory_bottom_menu_obj7 = TargetImage("exploratory_bottom_menu_obj7.png")
# 探索底部菜单 - 平安奇谭
exploratory_bottom_menu_obj8 = TargetImage("exploratory_bottom_menu_obj8.png")
# 探索底部菜单 - 六道之门
exploratory_bottom_menu_obj9 = TargetImage("exploratory_bottom_menu_obj9.png")
# 探索底部菜单 - 契灵之境
exploratory_bottom_menu_obj10 = TargetImage("exploratory_bottom_menu_obj10.png")
# 结界突破标题
Boundary_breakthrough_title = TargetImage("Boundary_breakthrough_title.png")
# 结界突破 - 个人突破 - 防守记录图标
Boundary_breakthrough_record_defense_tag = TargetImage("Boundary_breakthrough_record_defense_tag.png")
# 结界突破 - 寮突破 - 突破记录图标
Boundary_breakthrough_records_broken_tag = TargetImage("Boundary_breakthrough_records_broken_tag.png")
# 结界突破 - 个人 - 选中
Boundary_breakthrough_personal_selected = TargetImage("Boundary_breakthrough_personal_selected.png")
# 结界突破 - 个人 - 未选中
Boundary_breakthrough_personal_unselected = TargetImage("Boundary_breakthrough_personal_unselected.png")
# 结界突破 - 寮 - 选中
Boundary_breakthrough_lao_selected = TargetImage("Boundary_breakthrough_lao_selected.png")
# 结界突破 - 寮 - 未选中
Boundary_breakthrough_lao_unselected = TargetImage("Boundary_breakthrough_lao_unselected.png")
# 结界突破 - 寮 - 突破失败标记
Boundary_breakthrough_lao_failure_flag = TargetImage("Boundary_breakthrough_lao_failure_flag.png")
# 结界突破 - 寮 - 结界进攻按钮
Boundary_breakthrough_lao_info_attack = TargetImage("Boundary_breakthrough_lao_info_attack.png")
# 道馆突破 - 准备按钮
ready_button = TargetImage("ready.png")
# 头像
avatar = TargetImage("user_image.png")
# 测试
test = TargetImage("test.png")
# 活动 - 挑战按钮
activitie_start = TargetImage("activitie_start.png")
# 阵容 - 已锁定
lineup_locked = TargetImage("lineup_locked.png")
# 阵容 - 未锁定
lineup_unlocked = TargetImage("lineup_unlocked.png") 
# 副本 - 结束标记
battle_end_tag = TargetImage("battle_end_tag.png")
# 副本 - 挑战次数不足
not_enough_challenges = TargetImage("not_enough_challenges.png")
# 副本 - 冒险干粮不足
lacking_in_strength = TargetImage("lacking_in_strength.png")
# 斗技 - 开始匹配
battle_start = TargetImage("battle_start.png")
# 斗技 - 准备
battle_ready = TargetImage("battle_ready.png")
# 斗技 - 胜利
battle_victory = TargetImage("battle_victory.png")
# 斗技 - 失败
battle_defeat = TargetImage("battle_defeat.png")
# 斗技 - 拔得头筹
battle_mvp = TargetImage("battle_mvp.png")
# 斗技 - BP手动
battle_bp_no_auto = TargetImage("battle_bp_no_auto.png")
# 战斗 - 手动
battle_manual = TargetImage("battle_manual.png")
# 战斗 - 自动
battle_auto = TargetImage("battle_auto.png")
# 御灵 - 阵容锁定
divine_spirit_lineup_locked = TargetImage("divine_spirit_lineup_locked.png")
# 御灵 - 阵容未锁定
divine_spirit_lineup_unlocked = TargetImage("divine_spirit_lineup_unlocked.png")
# 御灵 - 开始挑战
divine_spirit_start = TargetImage("divine_spirit_start.png")
# 绘卷 - 小绘卷
scroll_small = TargetImage("scroll_small.png")
# 绘卷 - 小绘卷数量
scroll_small_info = TargetImage("scroll_small_info.png")


PostMessageW = windll.user32.PostMessageW
MapVirtualKeyW = windll.user32.MapVirtualKeyW
VkKeyScanA = windll.user32.VkKeyScanA
ClientToScreen = windll.user32.ClientToScreen

# MOUSE
WM_MOUSEMOVE = 0x0200
WM_LBUTTONDOWN = 0x0201
WM_LBUTTONUP = 0x202
WM_MOUSEWHEEL = 0x020A
WHEEL_DELTA = 120

# KEYBOARD
WM_KEYDOWN = 0x100
WM_KEYUP = 0x101

VkCode = {
    "back":  0x08,
    "tab":  0x09,
    "return":  0x0D,
    "shift":  0x10,
    "control":  0x11,
    "menu":  0x12,
    "pause":  0x13,
    "capital":  0x14,
    "escape":  0x1B,
    "space":  0x20,
    "end":  0x23,
    "home":  0x24,
    "left":  0x25,
    "up":  0x26,
    "right":  0x27,
    "down":  0x28,
    "print":  0x2A,
    "snapshot":  0x2C,
    "insert":  0x2D,
    "delete":  0x2E,
    "lwin":  0x5B,
    "rwin":  0x5C,
    "numpad0":  0x60,
    "numpad1":  0x61,
    "numpad2":  0x62,
    "numpad3":  0x63,
    "numpad4":  0x64,
    "numpad5":  0x65,
    "numpad6":  0x66,
    "numpad7":  0x67,
    "numpad8":  0x68,
    "numpad9":  0x69,
    "multiply":  0x6A,
    "add":  0x6B,
    "separator":  0x6C,
    "subtract":  0x6D,
    "decimal":  0x6E,
    "divide":  0x6F,
    "f1":  0x70,
    "f2":  0x71,
    "f3":  0x72,
    "f4":  0x73,
    "f5":  0x74,
    "f6":  0x75,
    "f7":  0x76,
    "f8":  0x77,
    "f9":  0x78,
    "f10":  0x79,
    "f11":  0x7A,
    "f12":  0x7B,
    "numlock":  0x90,
    "scroll":  0x91,
    "lshift":  0xA0,
    "rshift":  0xA1,
    "lcontrol":  0xA2,
    "rcontrol":  0xA3,
    "lmenu":  0xA4,
    "rmenu":  0XA5
}


def get_virtual_keycode(key: str):
    """根据按键名获取虚拟按键码

    Args:
        key (str): 按键名

    Returns:
        int: 虚拟按键码
    """
    if len(key) == 1 and key in string.printable:
        # https://docs.microsoft.com/en-us/windows/win32/api/winuser/nf-winuser-vkkeyscana
        return VkKeyScanA(ord(key)) & 0xff
    else:
        return VkCode[key]


def key_down(handle: HWND, key: str):
    """按下指定按键

    Args:
        handle (HWND): 窗口句柄
        key (str): 按键名
    """
    vk_code = get_virtual_keycode(key)
    scan_code = MapVirtualKeyW(vk_code, 0)
    # https://docs.microsoft.com/en-us/windows/win32/inputdev/wm-keydown
    wparam = vk_code
    lparam = (scan_code << 16) | 1
    PostMessageW(handle, WM_KEYDOWN, wparam, lparam)


def key_up(handle: HWND, key: str):
    """放开指定按键

    Args:
        handle (HWND): 窗口句柄
        key (str): 按键名
    """
    vk_code = get_virtual_keycode(key)
    scan_code = MapVirtualKeyW(vk_code, 0)
    # https://docs.microsoft.com/en-us/windows/win32/inputdev/wm-keyup
    wparam = vk_code
    lparam = (scan_code << 16) | 0XC0000001
    PostMessageW(handle, WM_KEYUP, wparam, lparam)



def move_to(handle: HWND, x: int, y: int):
    """移动鼠标到坐标（x, y)

    Args:
        handle (HWND): 窗口句柄
        x (int): 横坐标
        y (int): 纵坐标
    """
    # https://docs.microsoft.com/en-us/windows/win32/inputdev/wm-mousemove
    wparam = 0
    lparam = y << 16 | x
    PostMessageW(handle, WM_MOUSEMOVE, wparam, lparam)


def left_down(handle: HWND, x: int, y: int):
    """在坐标(x, y)按下鼠标左键

    Args:
        handle (HWND): 窗口句柄
        x (int): 横坐标
        y (int): 纵坐标
    """
    # https://docs.microsoft.com/en-us/windows/win32/inputdev/wm-lbuttondown
    wparam = 0
    lparam = y << 16 | x
    PostMessageW(handle, WM_LBUTTONDOWN, wparam, lparam)


def left_up(handle: HWND, x: int, y: int):
    """在坐标(x, y)放开鼠标左键

    Args:
        handle (HWND): 窗口句柄
        x (int): 横坐标
        y (int): 纵坐标
    """
    # https://docs.microsoft.com/en-us/windows/win32/inputdev/wm-lbuttonup
    wparam = 0
    lparam = y << 16 | x
    PostMessageW(handle, WM_LBUTTONUP, wparam, lparam)


def scroll(handle: HWND, delta: int, x: int, y: int):
    """在坐标(x, y)滚动鼠标滚轮

    Args:
        handle (HWND): 窗口句柄
        delta (int): 为正向上滚动，为负向下滚动 
        x (int): 横坐标
        y (int): 纵坐标
    """
    move_to(handle, x, y)
    # https://docs.microsoft.com/en-us/windows/win32/inputdev/wm-mousewheel
    wparam = delta << 16
    p = POINT(x, y)
    ClientToScreen(handle, byref(p))
    lparam = p.y << 16 | p.x
    PostMessageW(handle, WM_MOUSEWHEEL, wparam, lparam)


def scroll_up(handle: HWND, x: int, y: int):
    """在坐标(x, y)向上滚动鼠标滚轮

    Args:
        handle (HWND): 窗口句柄
        x (int): 横坐标
        y (int): 纵坐标
    """
    scroll(handle, WHEEL_DELTA, x, y)


def scroll_down(handle: HWND, x: int, y: int):
    """在坐标(x, y)向下滚动鼠标滚轮

    Args:
        handle (HWND): 窗口句柄
        x (int): 横坐标
        y (int): 纵坐标
    """
    scroll(handle, -WHEEL_DELTA, x, y)


def click(handle: HWND, x, y, offset_x=15, offset_y=15, duration=0.027, offset_duration=0.03, waitCD=0.7, offset_waitCD=0.3):
        """在指定窗口中点击模板图像的中心点

        Args:
            handle (HWND): 窗口句柄
            x (int): 点击位置的横坐标
            y (int): 点击位置的纵坐标
            offset_x (int, optional): 横向偏移量. 默认为15.
            offset_y (int, optional): 纵向偏移量. 默认为15.
            duration (float, optional): 按下和放开的时间间隔. 默认为0.027.
            offset_duration (float, optional): 时间间隔的随机偏移量. 默认为0.03.
            waitCD (float, optional): 点击后等待时间. 默认为0.7.
            offset_waitCD (float, optional): 等待时间的随机偏移量. 默认为0.3.
            retrun (list): 返回点击位置的坐标
        """
        rect = RECT()
        windll.user32.GetWindowRect(handle, byref(rect))
        original_width = rect.right - rect.left
        original_height = rect.bottom - rect.top
        click_pos_x = x + random.randint(-offset_x, offset_x)
        click_pos_y = y + random.randint(-offset_y, offset_y)
        # 映射到原始窗口坐标
        original_click_x, original_click_y = map_to_original(click_pos_x, click_pos_y, original_width, original_height)
        press_duration = duration + random.uniform(0.0, offset_duration)
        wait_time = waitCD + random.uniform(0.0, offset_waitCD)
        left_down(handle, original_click_x, original_click_y)
        time.sleep(press_duration)
        left_up(handle, original_click_x, original_click_y)
        time.sleep(wait_time)
        return [(click_pos_x, click_pos_y), (original_click_x, original_click_y)]