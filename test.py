# -*- coding: utf-8 -*-
'''
Author       : ZakiuC
Date         : 2024-01-04 10:59:14
LastEditors  : ZakiuC z2337070680@163.com
LastEditTime : 2024-01-05 09:18:59
FilePath     : \yys\test.py
Description  : 
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

from grabscreen import grab_window
from loadModel import home_top_ui_jinbi, home_top_ui_gouyu, home_top_ui_tili


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
        # 移除非数字和非中文单位的字符
        num_str = ''.join(filter(lambda x: x.isdigit() or x in ['亿', '万', '点'], text))

        # 处理可能的空字符串
        if not num_str:
            return 0

        # 转换中文单位
        if '亿' in num_str:
            return int(float(num_str.replace('亿', '')) * 1e8)
        elif '万' in num_str:
            return int(float(num_str.replace('万', '')) * 1e4)
        else:
            # 处理带有小数点的数字
            if '点' in num_str:
                num_str = num_str.replace('点', '.')
            return int(float(num_str))
    except ValueError:
        # 在转换过程中出现错误时返回0或者适当的错误处理
        print(f"Error parsing number from text: {text}")
        return 0
myMoney = None
myGouyu = None
myTili = None

def imgAnalysis(img):
    """
    图像分析
    具体分析内容：
    1. 模板匹配并返回匹配结果

    img: 待分析的图像
    """
    global myMoney, myGouyu, myTili

    if myMoney is None:
        result = home_top_ui_jinbi.match(img)
        if result is not None:
            top_left, bottom_right = result
            cv2.rectangle(img, top_left, bottom_right, (0, 255, 0), 1)
            cv2.putText(img, "money", top_left, cv2.FONT_HERSHEY_SIMPLEX, 0.3, (0, 255, 0), 1)
            top_left = (top_left[0] + home_top_ui_jinbi.width, top_left[1])
            bottom_right = (bottom_right[0] + 50, bottom_right[1])
            roi = img[top_left[1]:bottom_right[1], top_left[0]:bottom_right[0]]
            text = pytesseract.image_to_string(roi, lang='chi_sim')
            myMoney = parse_chinese_number(text)
            print(f'moneyText: {text}, data: {myMoney}')

    if myGouyu is None:
        result = home_top_ui_gouyu.match(img)
        if result is not None:
            top_left, bottom_right = result
            cv2.rectangle(img, top_left, bottom_right, (0, 255, 0), 1)
            cv2.putText(img, "gouyu", top_left, cv2.FONT_HERSHEY_SIMPLEX, 0.3, (0, 255, 0), 1)
            top_left = (top_left[0] + home_top_ui_gouyu.width, top_left[1])
            bottom_right = (bottom_right[0] + 50, bottom_right[1])
            roi = img[top_left[1]:bottom_right[1], top_left[0]:bottom_right[0]]
            text = pytesseract.image_to_string(roi, lang='chi_sim')
            myGouyu = parse_chinese_number(text)
            print(f'gouyuText: {text}, data: {myGouyu}')

    if myTili is None:
        result = home_top_ui_tili.match(img)
        if result is not None:
            top_left, bottom_right = result
            cv2.rectangle(img, top_left, bottom_right, (0, 255, 0), 1)
            cv2.putText(img, "tili", top_left, cv2.FONT_HERSHEY_SIMPLEX, 0.3, (0, 255, 0), 1)
            top_left = (top_left[0] + home_top_ui_tili.width, top_left[1])
            bottom_right = (bottom_right[0] + 70, bottom_right[1])
            roi = img[top_left[1]:bottom_right[1], top_left[0]:bottom_right[0]]
            text = pytesseract.image_to_string(roi, lang='chi_sim')
            myTili = parse_chinese_number(text)
            print(f'tiliText: {text}, data: {myTili}')
    






def calculate_fps():
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

    # 创建一个线程安全的队列
    frame_timestamps = queue.Queue()

    # 创建并启动 FPS 计算线程
    fps_thread = threading.Thread(target=calculate_fps)
    fps_thread.start()

    # 加载OCR核心
    pytesseract.pytesseract.tesseract_cmd = r'D:\Tools\Tesseract-OCR\tesseract.exe'
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

        # 图像分析
        imgAnalysis(imgResize)

        # 添加帧率信息
        cv2.putText(imgShow[current_index], fps_text, (5, 20), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 1)

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
        if key == ord('a'):
            current_index = (current_index - 1) % len(imgShow)  # 循环显示
        elif key == ord('d'):
            current_index = (current_index + 1) % len(imgShow)  # 循环显示
        elif key == ord('j'):
            # 保存当前显示的图像
            cv2.imwrite(save_path, imgShow[current_index])
            print(f"Image saved at {save_path}")
        elif key == ord('q'):
            running = False
            print("Exiting...")
            break
        
    # 线程和窗口清理
    fps_thread.join()
    cv2.destroyAllWindows()