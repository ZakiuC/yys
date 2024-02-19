# -*- coding: utf-8 -*-
'''
Author       : ZakiuC
Date         : 2024-01-11 08:38:16
LastEditors  : ZakiuC z2337070680@163.com
LastEditTime : 2024-02-16 19:47:24
FilePath     : \script.py
Description  : 
Copyright (c) 2024 by ZakiuC z2337070680@163.com, All Rights Reserved. 
'''
import cv2
import re
import numpy as np
import pytesseract
import appPush
import json
from datetime import datetime
import os
from loadModel import test, home_top_ui_jinbi, home_top_ui_gouyu, home_top_ui_tili, not_enough_challenges, battle_end_tag, lineup_locked, lineup_unlocked, \
    activitie_start, lacking_in_strength, home_exploratory, exploratory_goblin_tag, exploratory_bottom_menu_obj3, Boundary_breakthrough_title, \
    Boundary_breakthrough_record_defense_tag, Boundary_breakthrough_records_broken_tag, Boundary_breakthrough_lao_unselected, Boundary_breakthrough_lao_failure_flag, \
    Boundary_breakthrough_lao_info_attack, ready_button, avatar, battle_mvp, battle_start, battle_ready, battle_manual, battle_auto, battle_victory, battle_defeat, \
    battle_bp_no_auto, divine_spirit_lineup_locked, divine_spirit_lineup_unlocked, divine_spirit_start, scroll_small, scroll_small_info, pvp_score, seal_quest_tag,\
    seal_quest_soul_jades, seal_quest_agree, seal_quest_refuse, key_down, key_up, click


# 突发事件监控与处理
hook_state = 0
def event_monitor(img, handle):
    global hook_state
    # 悬赏封印监控与处理
    result = [None] * 4
    battle_stages = [seal_quest_tag, seal_quest_soul_jades, seal_quest_agree, seal_quest_refuse]
    button_texts = ["tag[seal quest]", "icon[soul jades]", "button[agree]", "button[refuse]"]

    hook_deal = False
    for i, stage in enumerate(battle_stages):
        result[i] = stage.match(img)
        if result[i] is not None:
            hook_deal = True  
            top_left, bottom_right = result[i]
            cv2.rectangle(img, top_left, bottom_right, (0, 255, 0), 1)
            cv2.putText(img, button_texts[i], top_left, cv2.FONT_HERSHEY_SIMPLEX, 0.3, (0, 255, 0), 1)
            if i == 0:
                hook_state = 1
            elif i == 1:
                if hook_state == 1:
                    hook_state = 2
            elif i == 2:
                if hook_state == 2:
                    battle_stages[i].click(handle)
            elif i == 3:
                # 不是勾协，拒绝
                if hook_state == 1:
                    battle_stages[i].click(handle)
            else:
                pass
    if hook_deal == False:
        if hook_state == 1:
            print("拒绝了悬赏封印")
            hook_state = 0
        elif hook_state == 2:
            print("接受了勾协")
            hook_state = 0
        else:
            pass


def script(img, handle, state):
    # result = script_1800(img, handle, state)
    result = script_wrestling(img, handle, state) # 斗技
    # result = divine_spirit_grinding_scrolls(img, handle, state)
    return result

def scene_prompt(state):
    # result = scene_1800(state)
    result = scene_wrestling(state)    # 斗技
    # result = scene_divine_spirit(state)
    return result

# 爬塔1800
def script_1800(img, handle, state):
    initial_state = state  # 记录初始state
    result = [None] * 8
    battle_stages = [not_enough_challenges, lacking_in_strength, lineup_unlocked, activitie_start, lineup_locked, battle_manual, battle_auto, battle_end_tag]
    button_texts = ["tag[not enough challenges]", "tag[lacking in strength]", "button[lineup unlocked]", "button[activitie start]", "button[lineup locked]", \
                    "button[battle manual]", "button[battle auto]", "tag[battle end]"]
    
    if 0 <= state <= 8:
        for i, stage in enumerate(battle_stages):
            result[i] = stage.match(img)
            if result[i] is not None:
                top_left, bottom_right = result[i]
                cv2.rectangle(img, top_left, bottom_right, (0, 255, 0), 1)
                cv2.putText(img, button_texts[i], top_left, cv2.FONT_HERSHEY_SIMPLEX, 0.3, (0, 255, 0), 1)
                if i != 6 and i != 0 and i != 1 and i != 4:
                    battle_stages[i].click(handle)
                    state =  (i + 1)
                elif i == 0:
                    state = 99
                elif i == 1:
                    state = 99
                elif i == 4:
                    state =  (i + 1)
                elif i == 6:
                    state =  (i + 1)
                else:
                    pass
                
                break

    # 检查 state 是否发生变化，并相应地打印信息
    if initial_state != state:
        if state == 99:
            print("挑战次数不足或体力不足,停止运行")
        elif state in [3, 4, 6, 8]:
            print(f"点击了{button_texts[state-1]}")
        elif state == 5:
            print("阵容已锁定")
        elif state == 7:
            print("自动战斗中")
        else:
            print(f"未知错误, state: {state}")

    return state

# 爬塔1800 - 场景提示
def scene_1800(state):
    """
    1800爬塔场景提示文本切换

    Args:
        state (int): 状态
    
    Returns:
        scene_text (str): 场景提示文本
    """
    if state == 0:
        scene_text = "stop"
    elif state == 1:
        scene_text = "1800 scene"
    elif state == 2:
        scene_text = "1800 scene"
    elif state == 3:
        scene_text = "1800 scene"
    elif state == 4:
        scene_text = "1800 scene"
    elif state == 5:
        scene_text = "1800 scene"
    elif state == 6:
        scene_text = "battles"
    elif state == 7:
        scene_text = "battles"
    elif state == 8:
        scene_text = "battle victory"
    else:
        scene_text = "unknown"
    return scene_text


pvp_my_score = 0
score_count = 0
temp_score = None
max_pvp_my_score = 0
def extract_new_score(img_original, bottom_right, scale_factor=6):
    x, y = bottom_right
    x += 50  # 根据实际情况调整，以确保截取到分数区域
    y -= 23
    info_img = img_original[y:y + 23, x - 56:x]  # 调整裁剪范围以覆盖分数区域

    # 将图片等比放大,以提高识别准确率
    info_img = cv2.resize(info_img, None, fx=scale_factor, fy=scale_factor, interpolation=cv2.INTER_CUBIC)

    # 将图片转换到 HSV 颜色空间
    imgHSV = cv2.cvtColor(info_img, cv2.COLOR_BGR2HSV)
    # 定义 HSV 颜色范围的上下限
    lower = np.array([9, 71, 114])
    upper = np.array([19, 97, 255])
    # 创建蒙版
    mask = cv2.inRange(imgHSV, lower, upper)
    # 应用蒙版
    imgResult = cv2.bitwise_and(info_img, info_img, mask=mask)
    gray_info_img = cv2.cvtColor(imgResult, cv2.COLOR_BGR2GRAY)
    # cv2.imshow("info_img", info_img)
    # cv2.imshow("gray_info_img", gray_info_img)
    # 识别
    text = pytesseract.image_to_string(gray_info_img, config='outputbase digits', lang='eng')
    new_score = re.findall(r'\d+', text)
    # print(f'text:{text}, new_score: {new_score}')
    if new_score:
        new_score = int(new_score[0])
        # 如果识别出的分数与上一次的分数相差500以上，则认为识别错误(可能引起误判的bug)
        if pvp_my_score > 0:
            if abs(new_score - pvp_my_score) > 500:  
                return None
            else:
                return new_score
        else:
            return new_score
    else:
        return None



def update_scores_to_file(pvp_my_score, max_pvp_my_score, filename='pvp_scores.txt'):
    """
    将分数更新至本地文件并向app推送

    Args:
        pvp_my_score (int): pvp的分数
        max_pvp_my_score (int): pvp的最高分数
        filename (str): 文件名
    """
    with open(filename, 'a') as f:
        now = datetime.now()  # 获取当前时间
        timestamp = now.strftime("%Y-%m-%d %H:%M:%S")  # 格式化时间戳
        f.write(f'当前分数: {pvp_my_score}\t历史最高分: {max_pvp_my_score} ---- {timestamp}\n')
        # 获取当前文件夹下的.env文件中的SENDKEY
        data = {}
        with open(os.path.join(os.path.dirname(__file__), '.env'), 'r') as f:
            for line in f:
                key, value = line.strip().split('=')
                data[key] = value
        key = data['SENDKEY']
        ret = appPush.sc_send(f'更新斗技分数: {pvp_my_score}/{max_pvp_my_score}',desp = f'当前分数: {pvp_my_score}\t历史最高分: {max_pvp_my_score} ---- {timestamp}', channel=98, key=key)
        ret_dict = json.loads(ret)  # 将 ret 的内容解析为字典
        # 检查 'error' 字段是否等于 "SUCCESS"
        if ret_dict['data']['error'] != 'SUCCESS':
            print(f"推送失败：{ret_dict['data']['error']}")
        else:
            print(f"推送成功")
        print(f"分数已更新至文件: {pvp_my_score}/{max_pvp_my_score}")



# 斗技
def script_wrestling(img, handle, state):
    """
    斗技脚本
    
    Args:
        img (np.ndarray): 图像
        handle (int): 窗口句柄
        state (int): 状态

    Returns:
        state (int): 状态
    """
    global pvp_my_score, score_count, temp_score, max_pvp_my_score
    initial_state = state  # 记录初始state
    result = [None] * 9
    battle_stages = [pvp_score, battle_start, battle_ready, battle_manual, battle_auto, battle_victory, battle_defeat, battle_mvp, battle_bp_no_auto]
    button_texts = ["tag[score]", "button[battle start]", "button[battle ready]", "button[battle manual]", "button[battle auto]", "tag[battle victory]", \
                    "tag[battle defeat]", "tag[battle mvp]", "button[bp auto]"]
    img_original = img.copy()
    
    # 重置计数器
    if state != 1 and state != 2:
        if score_count != 0:
            score_count = 0
            print("重置分数读取计数器")
    # 如果max_pvp_my_score无值或者值为零，从文件中读取max_pvp_my_score
    if not max_pvp_my_score:
        if os.path.exists("pvp_scores.txt"):
            with open("pvp_scores.txt", 'r') as f:
                lines = f.readlines()
                if lines:  # 检查是否有行
                    last_line = lines[-1]  # 获取最后一行
                    if '历史最高分' in last_line:
                        max_pvp_my_score = int(last_line.split('\t')[1].split(':')[1].split(' ')[1])  # 再次按照 ' ' 分割，然后选择数字部分
        else:
            print("分数记录文件不存在")

    if 0 <= state <= 9:
        for i, stage in enumerate(battle_stages):
            result[i] = stage.match(img_original)
            if result[i] is not None:
                top_left, bottom_right = result[i]
                cv2.rectangle(img, top_left, bottom_right, (0, 255, 0), 1)
                cv2.putText(img, button_texts[i], top_left, cv2.FONT_HERSHEY_SIMPLEX, 0.3, (0, 255, 0), 1)
                if i != 4 and i != 0:  # 自动战斗，不需要点击
                    battle_stages[i].click(handle)
                    print(f"点击了{button_texts[i]}")
                    state =  (i + 1)
                    break
                elif i == 0:
                    new_score = extract_new_score(img_original, result[0][1])
                    if new_score is not None:
                        if temp_score is not None and new_score == temp_score:
                            if score_count >= 15:  # 连续15次相同分数
                                pvp_my_score = new_score
                                # 不return，继续检测下一个场景
                                if pvp_my_score > max_pvp_my_score:
                                    max_pvp_my_score = pvp_my_score
                                # 更新分数到文件
                                update_scores_to_file(pvp_my_score, max_pvp_my_score)  
                                if pvp_my_score >= 2590:
                                    state = 99
                                    break       
                            else:
                                score_count += 1
                                state =  (i + 1)
                                break
                        else:
                            temp_score = new_score
                            score_count = 1
                            state =  (i + 1)
                            break
                    else:
                        state =  (i + 1)
                        break
                else:
                    state =  (i + 1)
                    break
        
    # 检查 state 是否发生变化，并相应地打印信息
    if initial_state != state:
        if state == 99:
            print("分数达到目标，停止运行脚本")
        elif state in [4, 6, 7, 8, 9]:
            print(f"点击了{button_texts[state-1]}")
        elif state == 1:
            print("更新斗技分数中...")
        elif state == 2:
            print(f"斗技分数更新完毕: {pvp_my_score}")
        elif state == 3:
            print("准备阶段")
        elif state == 5:
            print("自动战斗中...")
        else:
            print(f"未知错误, state: {state}")

    return state


# 斗技 - 场景提示
def scene_wrestling(state):
    """
    场景提示文本切换

    Args:
        state (int): 状态
    
    Returns:
        scene_text (str): 场景提示文本
    """
    # 根据state更新场景显示文本
    if state == 0:
        scene_text = f"stop[now:{pvp_my_score} max:{max_pvp_my_score}]"
    elif state == 1:
        scene_text = f"battle scene[now:{pvp_my_score} max:{max_pvp_my_score}]"
    elif state == 2:
        scene_text = f"battle scene[now:{pvp_my_score} max:{max_pvp_my_score}]"
    elif state == 3:
        scene_text = f"battle ready[now:{pvp_my_score} max:{max_pvp_my_score}]"
    elif state == 4:
        scene_text = f"battles[now:{pvp_my_score} max:{max_pvp_my_score}]"
    elif state == 5:
        scene_text = f"battles[now:{pvp_my_score} max:{max_pvp_my_score}]"
    elif state == 6:
        scene_text = f"battle victory[now:{pvp_my_score} max:{max_pvp_my_score}]"
    elif state == 7:
        scene_text = f"battle defeat[now:{pvp_my_score} max:{max_pvp_my_score}]"
    elif state == 8:
        scene_text = f"battle mvp[now:{pvp_my_score} max:{max_pvp_my_score}]"
    elif state == 9:
        scene_text = f"bp[now:{pvp_my_score} max:{max_pvp_my_score}]"
    else:
        scene_text = f"unknown[now:{pvp_my_score} max:{max_pvp_my_score}]"
    return scene_text



def parse_acquired_max(input_str):
    """
    从字符串中解析出当前获取小绘卷的数量和最大数量
    """
    match = re.search(r'(\d+)/(\d+)', input_str)
    if match:
        acquired = int(match.group(1))
        max = int(match.group(2))
        return acquired, max
    else:
        return None, None



# 御灵 刷绘卷
def divine_spirit_grinding_scrolls(img, handle, state):
    """
    御灵 刷绘卷脚本

    Args:
        img (np.ndarray): 图像
        handle (int): 窗口句柄
        state (int): 状态
    
    Returns:
        state (int): 状态
    """
    global acquired, max
    initial_state = state  # 记录初始state
    result = [None] * 9
    battle_stages = [divine_spirit_lineup_unlocked, divine_spirit_start, divine_spirit_lineup_locked , battle_manual, battle_auto, scroll_small_info, scroll_small, \
                     battle_defeat, battle_end_tag]
    button_texts = ["button[lineup unlocked]", "button[divine spirit start]", "button[lineup locked]" , "button[battle manual]", "button[battle auto]", "tag[scroll small info]", \
                    "icon[scroll small]", "tag[battle defeat]", "tag[battle victory]"]
    
    if 0 <= state <= 9:
        for i, stage in enumerate(battle_stages):
            result[i] = stage.match(img)
            if result[i] is not None:
                top_left, bottom_right = result[i]
                # cv2.rectangle(img, top_left, bottom_right, (0, 255, 0), 1)
                # cv2.putText(img, button_texts[i], top_left, cv2.FONT_HERSHEY_SIMPLEX, 0.3, (0, 255, 0), 1)
                if i != 4 and i != 2 and i != 5:
                    battle_stages[i].click(handle)
                elif i == 5:
                    # 获取绘卷数量，根据scroll_small_info的最右边的坐标来截取右边40x12的区域，再用pytesseract进行识别
                    x, y = bottom_right
                    x += 34
                    y -= 13
                    info_img = img[y:y+13, x-34:x]
                    gray_info_img = cv2.cvtColor(info_img, cv2.COLOR_BGR2GRAY)
                    # 识别
                    text = pytesseract.image_to_string(gray_info_img, lang='eng')
                    if bool(re.search(r'\d+/\d+.*', text)):
                        acquired, max = parse_acquired_max(text)
                        print(f"已获取小绘卷数量：{acquired}/{max}")
                        if acquired == max:
                            # 满了，停止刷绘卷
                            state = 100
                        else:
                            click(handle=handle, x=112, y=122, waitCD=1)
                            click(handle=handle, x=112, y=122)
                    else:
                        acquired, max = 0, 0
                state = (i + 1)
                break
    
    # 检查 state 是否发生变化，并相应地打印信息
    if initial_state != state:
        if state == 100:
            print("小绘卷已刷满，停止运行脚本")
        elif state in [1, 2, 4, 6, 7, 8, 9]:
            print(f"点击了{button_texts[state-1]}")
        elif state == 3:
            print("阵容已锁定")
        elif state == 5:
            print("自动战斗中...")
        elif state == 6 or 7:
            print(f"获取小绘卷数量中...")
        else:
            print(f"未知错误, state: {state}")
    return state


acquired, max = 0, 0
# 御灵 - 场景提示
def scene_divine_spirit(state):
    # 根据state更新场景显示文本
    if state == 0:
        scene_text = f"stop: {acquired}/{max}"
    elif state == 1:
        scene_text = f"divine spirit scene: {acquired}/{max}"
    elif state == 2:
        scene_text = f"divine spirit scene: {acquired}/{max}"
    elif state == 3:
        scene_text = f"divine spirit scene: {acquired}/{max}"
    elif state == 4:
        scene_text = f"battles: {acquired}/{max}"
    elif state == 5:
        scene_text = f"battles: {acquired}/{max}"
    elif state == 6:
        scene_text = f"battle victory: {acquired}/{max}"
    elif state == 7:
        scene_text = f"battle victory: {acquired}/{max}"
    elif state == 8:
        scene_text = f"battle defeat: {acquired}/{max}"
    elif state == 9:
        scene_text = f"battle victory: {acquired}/{max}"
    else:
        scene_text = f"unknown: {acquired}/{max}"
    return scene_text