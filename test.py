# -*- coding: utf-8 -*-
'''
Author       : ZakiuC
Date         : 2024-01-04 10:59:14
LastEditors  : ZakiuC z2337070680@163.com
LastEditTime : 2024-01-12 17:04:56
FilePath     : \yys\test.py
Description  : 测试脚本
Copyright (c) 2024 by ZakiuC z2337070680@163.com, All Rights Reserved. 
'''
import cv2
import numpy as np
import win32gui
import win32con
import time
import threading
import queue
import pytesseract
import os
from ctypes import windll
import sys

from grabscreen import grab_window
from loadModel import divine_spirit_start, not_enough_challenges, battle_end_tag, lineup_locked, lineup_unlocked, activitie_start, home_exploratory, exploratory_goblin_tag, exploratory_bottom_menu_obj3, Boundary_breakthrough_title, Boundary_breakthrough_record_defense_tag, Boundary_breakthrough_records_broken_tag, Boundary_breakthrough_lao_unselected, Boundary_breakthrough_lao_failure_flag, Boundary_breakthrough_lao_info_attack, ready_button, avatar, key_down, key_up, click
from script import script, scene_prompt, event_monitor


def create_error_image(width, height, message):
    """
    创建一个显示错误信息的图像
    width: 图像宽度
    height: 图像高度
    message: 错误信息
    """
    img = np.zeros((height, width, 3), np.uint8)
    font = cv2.FONT_HERSHEY_SIMPLEX
    font_scale = 1
    font_color = (0, 0, 255)
    font_thickness = 2

    # 获取文本大小
    text_size = cv2.getTextSize(message, font, font_scale, font_thickness)[0]

    # 计算文本在图像中的位置（居中）
    text_x = (width - text_size[0]) // 2
    text_y = (height + text_size[1]) // 2

    # 将文本放置在图像中央
    cv2.putText(img, message, (text_x, text_y), font, font_scale, font_color, font_thickness)
    return img

def stackImages(scale, imgArray):
    """
    将图像堆叠在一起以便于显示
    scale: 缩放因子
    imgArray: 图像列表

    return: 堆叠后的图像
    """
    rows = len(imgArray)
    cols = len(imgArray[0])
    rowsAvailable = isinstance(imgArray[0], list)

    # 在这里，我们需要确定合适的尺寸以调整图像
    width = imgArray[0][0].shape[1] * scale
    height = imgArray[0][0].shape[0] * scale
    dim = (int(width), int(height))

    if rowsAvailable:
        for x in range(0, rows):
            for y in range(0, cols):
                # 调整图像尺寸
                imgArray[x][y] = cv2.resize(imgArray[x][y], dim, interpolation=cv2.INTER_AREA)
                if len(imgArray[x][y].shape) == 2:
                    imgArray[x][y] = cv2.cvtColor(imgArray[x][y], cv2.COLOR_GRAY2BGR)
        # 堆叠处理
        hor = [np.hstack(imgArray[x]) for x in range(0, rows)]
        ver = np.vstack(hor)
    else:
        for x in range(0, rows):
            imgArray[x] = cv2.resize(imgArray[x], dim, interpolation=cv2.INTER_AREA)
            if len(imgArray[x].shape) == 2:
                imgArray[x] = cv2.cvtColor(imgArray[x], cv2.COLOR_GRAY2BGR)
        ver = np.hstack(imgArray)

    return ver

def parse_chinese_number(text):
    try:
        # 移除非数字和非中文单位的字符（除了小数点）
        num_str = ''.join(filter(lambda x: x.isdigit() or x in ['亿', '万', '.', '/'], text))

        # 处理可能的空字符串
        if not num_str:
            return 0

        # 处理带有分隔符（如 14万/100）的情况
        if '/' in num_str:
            num_str = num_str.split('/')[0]

        # 处理带有小数点的数字
        if '.' in num_str:
            num_str = num_str.replace('.', '.')

        # 转换中文单位
        if '亿' in num_str:
            return int(float(num_str.replace('亿', '')) * 1e8)
        elif '万' in num_str:
            return int(float(num_str.replace('万', '')) * 1e4)
        else:
            return int(float(num_str))
    except ValueError:
        # 在转换过程中出现错误时返回0或者适当的错误处理
        print(f"Error parsing number from text: {text}")
        return 0


myMoney = None
myGouyu = None
myTili = None
click_flag = False
state = 99

def imgAnalysis(img):
    """
    图像分析
    具体分析内容：
    1. 模板匹配并返回匹配结果

    img: 待分析的图像
    """
    global click_flag, state
    # global myMoney, myGouyu, myTili

    # if myMoney is None or myMoney == 0:
    #     result = home_top_ui_jinbi.match(img)
    #     if result is not None:
    #         top_left, bottom_right = result
    #         cv2.rectangle(img, top_left, bottom_right, (0, 255, 0), 1)
    #         cv2.putText(img, "money", top_left, cv2.FONT_HERSHEY_SIMPLEX, 0.3, (0, 255, 0), 1)
    #         top_left = (top_left[0] + home_top_ui_jinbi.width, top_left[1])
    #         bottom_right = (bottom_right[0] + 50, bottom_right[1])
    #         roi = img[top_left[1]:bottom_right[1], top_left[0]:bottom_right[0]]
    #         text = pytesseract.image_to_string(roi, lang='chi_sim')
    #         myMoney = parse_chinese_number(text)
    #         print(f'moneyText: {text}, data: {myMoney}')

    # if myGouyu is None or myGouyu == 0:
    #     result = home_top_ui_gouyu.match(img)
    #     if result is not None:
    #         top_left, bottom_right = result
    #         cv2.rectangle(img, top_left, bottom_right, (0, 255, 0), 1)
    #         cv2.putText(img, "gouyu", top_left, cv2.FONT_HERSHEY_SIMPLEX, 0.3, (0, 255, 0), 1)
    #         top_left = (top_left[0] + home_top_ui_gouyu.width, top_left[1])
    #         bottom_right = (bottom_right[0] + 50, bottom_right[1])
    #         roi = img[top_left[1]:bottom_right[1], top_left[0]:bottom_right[0]]
    #         text = pytesseract.image_to_string(roi, lang='chi_sim')
    #         myGouyu = parse_chinese_number(text)
    #         print(f'gouyuText: {text}, data: {myGouyu}')

    # if myTili is None or myTili == 0:
    #     result = home_top_ui_tili.match(img)
    #     if result is not None:
    #         top_left, bottom_right = result
    #         cv2.rectangle(img, top_left, bottom_right, (0, 255, 0), 1)
    #         cv2.putText(img, "tili", top_left, cv2.FONT_HERSHEY_SIMPLEX, 0.3, (0, 255, 0), 1)
    #         top_left = (top_left[0] + home_top_ui_tili.width, top_left[1])
    #         bottom_right = (bottom_right[0] + 80, bottom_right[1])
    #         roi = img[top_left[1]:bottom_right[1], top_left[0]:bottom_right[0]]
    #         text = pytesseract.image_to_string(roi, lang='chi_sim')
    #         myTili = parse_chinese_number(text)
    #         print(f'tiliText: {text}, data: {myTili}')
    # # 道馆 - 突破
    # result = ready_button.match(img)
    # if result is not None:
    #     top_left, bottom_right = result
    #     cv2.rectangle(img, top_left, bottom_right, (0, 255, 0), 1)
    #     cv2.putText(img, "button[ready]", top_left, cv2.FONT_HERSHEY_SIMPLEX, 0.3, (0, 255, 0), 1)
    #     print(f"x: {ready_button.pos_x}, y: {ready_button.pos_y}")
    #     # if click_flag == False:
    #     #     click_flag = True
    #     ready_button.click(handle, duration=0.03)
    # # 结界突破 - 寮突
    # if state == 0:
    #     # 在庭院，找到探索按钮
    #     result = home_exploratory.match(img)
    #     if result is not None:
    #         top_left, bottom_right = result
    #         cv2.rectangle(img, top_left, bottom_right, (0, 255, 0), 1)
    #         cv2.putText(img, "button[exploratory]", top_left, cv2.FONT_HERSHEY_SIMPLEX, 0.3, (0, 255, 0), 1)
    #         print(f"click button[exploratory]")
    #         home_exploratory.click(handle)
    #     else:
    #         result = exploratory_goblin_tag.match(img)
    #         if result is not None:
    #             top_left, bottom_right = result
    #             cv2.rectangle(img, top_left, bottom_right, (0, 255, 0), 1)
    #             cv2.putText(img, "tag[goblin]", top_left, cv2.FONT_HERSHEY_SIMPLEX, 0.3, (0, 255, 0), 1)
    #             print(f"Leave the courtyard and come to the exploration scene.")
    #             state = 1

    # if state == 1:
    #     # 在探索场景，找到结界突破按钮
    #     result = exploratory_bottom_menu_obj3.match(img)
    #     if result is not None:
    #         top_left, bottom_right = result
    #         cv2.rectangle(img, top_left, bottom_right, (0, 255, 0), 1)
    #         cv2.putText(img, "button[obj3]", top_left, cv2.FONT_HERSHEY_SIMPLEX, 0.3, (0, 255, 0), 1)
    #         print(f"click button[obj3]")
    #         click_pos = exploratory_bottom_menu_obj3.click(handle)
    #         cv2.circle(img, click_pos[0], 5, (0, 0, 255), 1, shift=0)
    #     else:
    #         result = Boundary_breakthrough_title.match(img)
    #         if result is not None:
    #             top_left, bottom_right = result
    #             cv2.rectangle(img, top_left, bottom_right, (0, 255, 0), 1)
    #             cv2.putText(img, "title[Boundary_breakthrough]", top_left, cv2.FONT_HERSHEY_SIMPLEX, 0.3, (0, 255, 0), 1)
    #             print(f"Leave the exploration scene and come to the boundary breakthrough scene.")
    #             state = 2

    # if state == 2:
    #     # 在结界突破场景，切换到寮突破
    #     result = Boundary_breakthrough_record_defense_tag.match(img)
    #     if result is not None:
    #         top_left, bottom_right = result
    #         cv2.rectangle(img, top_left, bottom_right, (0, 255, 0), 1)
    #         cv2.putText(img, "icon[record_defense]", top_left, cv2.FONT_HERSHEY_SIMPLEX, 0.3, (0, 255, 0), 1)
    #         print(f"Onto the knot-breaking-personal-breaking scenario.")
    #         result = Boundary_breakthrough_lao_unselected.match(img)
    #         if result is not None:
    #             top_left, bottom_right = result
    #             cv2.rectangle(img, top_left, bottom_right, (0, 255, 0), 1)
    #             cv2.putText(img, "button[lao_unselected]", top_left, cv2.FONT_HERSHEY_SIMPLEX, 0.3, (0, 255, 0), 1)
    #             print(f"click button[lao_unselected]")
    #             Boundary_breakthrough_lao_unselected.click(handle)
    #     result = Boundary_breakthrough_records_broken_tag.match(img)
    #     if result is not None:
    #         top_left, bottom_right = result
    #         cv2.rectangle(img, top_left, bottom_right, (0, 255, 0), 1)
    #         cv2.putText(img, "icon[records_broken]", top_left, cv2.FONT_HERSHEY_SIMPLEX, 0.3, (0, 255, 0), 1)
    #         print(f"To the knot-breaking-squatter-breaking scene.")
    #         state = 3
                
    
    # if state == 3:
    #     # 定位特定区域
    #     top_left = (205, 65)
    #     bottom_right = (551, 331)
    #     # 将图片转换到 HSV 颜色空间
    #     imgHSV = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    #     # 定义HSV颜色范围的上下限
    #     lower = np.array([10, 32, 197])
    #     upper = np.array([18, 51, 249])
    #     # 创建蒙版
    #     mask = cv2.inRange(imgHSV, lower, upper)
    #     # 应用蒙版
    #     imgResult = cv2.bitwise_and(img, img, mask=mask)
    #     roi = imgResult[top_left[1]:bottom_right[1], top_left[0]:bottom_right[0]]
    #     # 在ROI中找矩形
    #     imgGray = cv2.cvtColor(roi, cv2.COLOR_BGR2GRAY)
    #     imgBlur = cv2.GaussianBlur(imgGray, (7,7), 1)
    #     imgCanny = cv2.Canny(imgBlur, 50, 50)
    #     _, thresh = cv2.threshold(imgCanny, 150, 255, cv2.THRESH_BINARY)
    #     contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    #     # 对轮廓进行排序，从左到右，从上到下
    #     contours_sorted = sorted(contours, key=lambda ctr: (cv2.boundingRect(ctr)[1], cv2.boundingRect(ctr)[0]))
    #     cv2.rectangle(img, top_left, bottom_right, (0, 255, 0), 1)
    #     id = 0
    #     # 计算失败标志
    #     results = Boundary_breakthrough_lao_failure_flag.match_all(img)
    #     for result in results:
    #         rx, ry, rw, rh = result[0][0], result[0][1], result[1][0] - result[0][0], result[1][1] - result[0][1]
    #         print("Result coordinates:", rx, ry, rw, rh)
    #         flag_top_left, flag_bottom_right = result
    #         cv2.rectangle(img, flag_top_left, flag_bottom_right, (0, 255, 0), 1)
    #         cv2.putText(img, "flag[fail]", flag_top_left, cv2.FONT_HERSHEY_SIMPLEX, 0.3, (0, 0, 255), 1)

    #     click_pos_x = click_pos_y = 0
    #     for contour in contours_sorted:
    #         # 获取轮廓的边界框
    #         x, y, w, h = cv2.boundingRect(contour)
    #         # 计算面积
    #         area = w * h

    #         overlap = False
    #         # 只有当result不为None时才进行重叠检测
    #         # 遍历每个匹配结果进行重叠检测
    #         for rx, ry, rw, rh in [(res[0][0], res[0][1], res[1][0] - res[0][0], res[1][1] - res[0][1]) for res in results]:
    #             if ((x + top_left[0]) < rx + rw and (x + top_left[0]) + w > rx and (y + top_left[1]) < ry + rh and (y + top_left[1]) + h > ry):
    #                 overlap = True
    #                 print("Overlap detected")
    #                 break  # 一旦检测到重叠，就跳出内循环

    #         if area > 9000 and area < 12000 and not overlap:
    #             # 打印轮廓的坐标和面积
    #             print(f"[{id}] coordinates and area:", x, y, w, h, area)
    #             # 在原图上绘制矩形
    #             cv2.rectangle(img, (top_left[0] + x, top_left[1] + y), (top_left[0] + x + w, top_left[1] + y + h), (0, 255, 0), 1)
    #             cv2.putText(img, f"[{id}]", (top_left[0] + x, top_left[1] + y), cv2.FONT_HERSHEY_SIMPLEX, 0.3, (0, 0, 255), 1)
    #             id += 1
    #             click_pos_x = top_left[0] + x + w // 2
    #             click_pos_y = top_left[1] + y + h // 2
    #             break
    #     if click_pos_x != 0 and click_pos_y != 0:
    #         click(handle=handle, x=click_pos_x, y=click_pos_y)
    #         print(f"Click the [{id}] button.")
    #         state = 4
    # result = not_enough_challenges.match(img)
    # if result is not None:
    #     top_left, bottom_right = result
    #     cv2.rectangle(img, top_left, bottom_right, (0, 255, 0), 1)
    #     cv2.putText(img, "tag[not_enough_challenges]", top_left, cv2.FONT_HERSHEY_SIMPLEX, 0.3, (0, 255, 0), 1)
    #     print(f"Click the [not_enough_challenges] button.")
    #     state = 100
    #     print("挑战次数不足")
    # if state == 0:
    #     locked_result = lineup_locked.match(img)
    #     unlocked_result = lineup_unlocked.match(img)
    #     if locked_result is not None and unlocked_result is None:
    #         top_left, bottom_right = locked_result
    #         cv2.rectangle(img, top_left, bottom_right, (0, 255, 0), 1)
    #         cv2.putText(img, "icon[locked]", top_left, cv2.FONT_HERSHEY_SIMPLEX, 0.3, (0, 255, 0), 1)
    #         state = 1
    #     elif locked_result is None and unlocked_result is not None:
    #         top_left, bottom_right = unlocked_result
    #         cv2.rectangle(img, top_left, bottom_right, (0, 255, 0), 1)
    #         cv2.putText(img, "icon[unlocked]", top_left, cv2.FONT_HERSHEY_SIMPLEX, 0.3, (0, 255, 0), 1)
    #         lineup_unlocked.click(handle)
    #     elif locked_result is not None and unlocked_result is not None:
    #         if lineup_locked.score > lineup_unlocked.score:
    #             top_left, bottom_right = locked_result
    #             cv2.rectangle(img, top_left, bottom_right, (0, 255, 0), 1)
    #             cv2.putText(img, "icon[locked]", top_left, cv2.FONT_HERSHEY_SIMPLEX, 0.3, (0, 255, 0), 1)
    #             state = 1
    #         else:
    #             top_left, bottom_right = unlocked_result
    #             cv2.rectangle(img, top_left, bottom_right, (0, 255, 0), 1)
    #             cv2.putText(img, "icon[unlocked]", top_left, cv2.FONT_HERSHEY_SIMPLEX, 0.3, (0, 255, 0), 1)
    #             lineup_unlocked.click(handle)
    # elif state == 1:
    #     print("已锁定阵容")
    #     result = activitie_start.match(img)
    #     if result is not None:
    #         top_left, bottom_right = result
    #         cv2.rectangle(img, top_left, bottom_right, (0, 255, 0), 1)
    #         cv2.putText(img, "button[start]", top_left, cv2.FONT_HERSHEY_SIMPLEX, 0.3, (0, 255, 0), 1)
    #         activitie_start.click(handle)
    #         print("点击了开始按钮")
    #     else:
    #         print("已开始战斗")
    #         state = 2
    # elif state == 2:
    #     result = battle_end_tag.match(img)
    #     if result is not None:
    #         top_left, bottom_right = result
    #         cv2.rectangle(img, top_left, bottom_right, (0, 255, 0), 1)
    #         cv2.putText(img, "tag[battle end]", top_left, cv2.FONT_HERSHEY_SIMPLEX, 0.3, (0, 255, 0), 1)
    #         battle_end_tag.click(handle)
    #         print("点击了战斗结束标签")
    #         state = 3
    #     else:
    #         print("战斗中")
    # elif state == 3:
    #     result = battle_end_tag.match(img)
    #     if result is not None:
    #         top_left, bottom_right = result
    #         cv2.rectangle(img, top_left, bottom_right, (0, 255, 0), 1)
    #         cv2.putText(img, "tag[battle end]", top_left, cv2.FONT_HERSHEY_SIMPLEX, 0.3, (0, 255, 0), 1)
    #         battle_end_tag.click(handle)
    #         print("点击了战斗结束标签")
    #     else:
    #         print("战斗结束")
    #         state = 0

        



def update_scene():
    """
    更新场景
    """
    global state, scene_text
    while running:
        try:
            scene_text = scene_prompt(state)
            time.sleep(0.1)
        except:
            continue

def calculate_fps():
    """
    fps计算
    """
    global fps_text, running, frame_timestamps
    last_frame_time = None
    while running:
        try:
            # 从队列中获取时间戳，最多等待一定时间
            current_frame_time = frame_timestamps.get(timeout=0.1)
            if last_frame_time is not None:
                time_difference = current_frame_time - last_frame_time
                if time_difference != 0:
                    fps = 1 / time_difference
                    fps_text = f'FPS: {fps:.2f}'
            last_frame_time = current_frame_time
        except queue.Empty:
            continue


if __name__ == "__main__":
    if not windll.shell32.IsUserAnAdmin():
        # 不是管理员就提权
        windll.shell32.ShellExecuteW(None, "runas", sys.executable, __file__, None, 1)
        sys.exit(0)  # 退出当前实例
    # 目标窗口标题
    window_title = "阴阳师-网易游戏"
    # 新窗口标题
    hook_window_title = "hook"
    # 定义新窗口的分辨率
    new_width, new_height = 640, 361
    # 当前显示的图像索引
    current_index = 0
    # 截图保存路径
    # 获取当前文件的绝对路径
    current_file_path = os.path.abspath(__file__)
    # 获取当前文件所在目录的路径
    current_dir = os.path.dirname(current_file_path)
    # 构建到 static/images/ 的路径
    path_to_images = os.path.join(current_dir, "static", "images")
    save_path = path_to_images
    # 初始化帧率相关的变量
    fps = 0
    frame_time = time.time()
    fps_text = f'FPS: {fps}'
    running = True
    # 初始化场景显示的变量
    scene_text = "unknown"

    # 创建一个线程安全的队列
    frame_timestamps = queue.Queue()

    # 创建并启动 FPS 计算线程
    fps_thread = threading.Thread(target=calculate_fps)
    fps_thread.start()

    # 创建并启动场景更新线程
    scene_thread = threading.Thread(target=update_scene)
    scene_thread.start()

    # 加载OCR核心
    pytesseract.pytesseract.tesseract_cmd = r'D:\Tools\Tesseract-OCR\tesseract.exe'

    # 获取窗口句柄
    handle = windll.user32.FindWindowW(None, "阴阳师-网易游戏")

    while True:
        # 捕获屏幕图像
        imgOrigin = grab_window(window_title)

        # 如果找不到窗口，则显示错误信息
        if imgOrigin is None:
            imgOrigin = create_error_image(new_width, new_height, 'WINDOW NOT FOUND')
        else:
            # 调整图像大小以适应新的分辨率
            imgOrigin = cv2.resize(imgOrigin, (new_width, new_height))

        # 调整图像大小以适应新的分辨率
        imgResize = cv2.resize(imgOrigin, (new_width, new_height))

        # 图像处理
        # 灰度图
        imgGray = cv2.cvtColor(imgResize, cv2.COLOR_BGR2GRAY)
        # 高斯模糊
        imgBlur = cv2.GaussianBlur(imgGray, (7,7), 1)
        # Canny边缘检测
        imgCanny = cv2.Canny(imgBlur, 50, 50)
        # 空白填充图像
        imgBlank = np.zeros_like(imgResize)
        # 原图
        imgContour = imgResize.copy()
        # 轮廓检测
        contours, hierarchy = cv2.findContours(imgCanny, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
        for cnt in contours:
            area = cv2.contourArea(cnt)
            cv2.drawContours(imgContour, cnt, -1, (0,255,0), 1)
        # 堆叠图像
        imgStack = stackImages(0.6, ([imgResize, imgGray, imgBlur],
                                    [imgCanny, imgContour, imgBlank]))

        
        imgShow = [imgResize, imgGray, imgBlur, imgCanny, imgContour, imgStack]

        # # 图像分析
        # imgAnalysis(imgResize)

        # 突发事件监控
        event_monitor(imgResize, handle)
        # 脚本
        state = script(imgResize, handle, state)

        # 添加帧率信息
        cv2.putText(imgShow[current_index], fps_text, (5, 20), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 1)
        # 添加场景信息
        # 右边距
        right_margin = 10
        # 获取文本大小
        (text_width, text_height), baseline = cv2.getTextSize(scene_text, cv2.FONT_HERSHEY_SIMPLEX, 0.5, 1)
        # 计算文本的起始 x 坐标
        start_x = imgShow[current_index].shape[1] - text_width - right_margin
        # 确保 start_x 不是负值846
        start_x = max(0, start_x)
        # 在图片上绘制文本
        cv2.putText(imgShow[current_index], scene_text, (start_x, 20), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 1)

        # 创建并显示窗口，使用新的分辨率
        cv2.namedWindow(hook_window_title, cv2.WINDOW_NORMAL)
        cv2.resizeWindow(hook_window_title, new_width, new_height)
        cv2.imshow(hook_window_title, imgShow[current_index])

        # 图片刷新后，向队列发送当前时间戳
        frame_timestamps.put(time.time())

        # 查找窗口并设置窗口位置
        hwnd = win32gui.FindWindow(None, hook_window_title)
        win32gui.SetWindowPos(hwnd, win32con.HWND_TOPMOST, 0, 0, 0, 0, win32con.SWP_NOMOVE | win32con.SWP_NOSIZE)

        # 设置 WS_EX_LAYERED 扩展样式
        exStyle = win32gui.GetWindowLong(hwnd, win32con.GWL_EXSTYLE)
        win32gui.SetWindowLong(hwnd, win32con.GWL_EXSTYLE, exStyle | win32con.WS_EX_LAYERED)

        # 设置窗口透明度
        # 透明度范围是 0(完全透明) 到 255(完全不透明)
        transparency = 75
        win32gui.SetLayeredWindowAttributes(hwnd, 0, transparency, win32con.LWA_ALPHA)


        # 获取一次键盘输入
        key = cv2.waitKey(1) & 0xFF

        # 根据键盘输入更新当前显示的图像索引
        if key == ord('a') or key == ord('A'):
            current_index = (current_index - 1) % len(imgShow)  # 循环显示
        elif key == ord('d') or key == ord('D'):
            current_index = (current_index + 1) % len(imgShow)  # 循环显示
        elif key == ord('j') or key == ord('J'):
            # 保存当前显示的图像
            cv2.imwrite(save_path + "/image.png", imgShow[current_index])
            print(f"Image saved at {save_path}")
        elif key == ord('s') or key == ord('S'):
            if state != 99:
                state = 99
                print("Stop script.")
            else:
                state = 0
                print("Start script.")
        elif key == ord('q') or key == ord('Q'):
            running = False
            print("Exiting...")
            break
            
        if state == 100:
            running = False
            print("Exiting...")
            break
        
    # 线程和窗口清理
    fps_thread.join()
    scene_thread.join()
    cv2.destroyAllWindows()