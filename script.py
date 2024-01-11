# -*- coding: utf-8 -*-
'''
Author       : ZakiuC
Date         : 2024-01-11 08:38:16
LastEditors  : ZakiuC z2337070680@163.com
LastEditTime : 2024-01-11 17:23:52
FilePath     : \yys\script.py
Description  : 
Copyright (c) 2024 by ZakiuC z2337070680@163.com, All Rights Reserved. 
'''
import cv2
import re
import pytesseract
from loadModel import test, home_top_ui_jinbi, home_top_ui_gouyu, home_top_ui_tili, not_enough_challenges, battle_end_tag, lineup_locked, lineup_unlocked, \
    activitie_start, lacking_in_strength, home_exploratory, exploratory_goblin_tag, exploratory_bottom_menu_obj3, Boundary_breakthrough_title, \
    Boundary_breakthrough_record_defense_tag, Boundary_breakthrough_records_broken_tag, Boundary_breakthrough_lao_unselected, Boundary_breakthrough_lao_failure_flag, \
    Boundary_breakthrough_lao_info_attack, ready_button, avatar, battle_mvp, battle_start, battle_ready, battle_manual, battle_auto, battle_victory, battle_defeat, \
    battle_bp_no_auto, divine_spirit_lineup_locked, divine_spirit_lineup_unlocked, divine_spirit_start, scroll_small, scroll_small_info, key_down, key_up, click


def script(img, handle, state):
    # result = script_1800(img, handle, state)
    # result = script_wrestling(img, handle, state)
    result = divine_spirit_grinding_scrolls(img, handle, state)
    return result

def scene_prompt(state):
    # result = scene_wrestling(state)
    result = scene_divine_spirit(state)
    return result

# 爬塔1800
def script_1800(img, handle, state):
    result = not_enough_challenges.match(img)
    if result is not None:
        top_left, bottom_right = result
        cv2.rectangle(img, top_left, bottom_right, (0, 255, 0), 1)
        cv2.putText(img, "tag[not_enough_challenges]", top_left, cv2.FONT_HERSHEY_SIMPLEX, 0.3, (0, 255, 0), 1)
        state = 100
        print("挑战次数不足")
    result = lacking_in_strength.match(img)
    if result is not None:
        top_left, bottom_right = result
        cv2.rectangle(img, top_left, bottom_right, (0, 255, 0), 1)
        cv2.putText(img, "tag[lacking_in_strength]", top_left, cv2.FONT_HERSHEY_SIMPLEX, 0.3, (0, 255, 0), 1)
        state = 100
        print("体力不足")
    if state == 0:
        locked_result = lineup_locked.match(img)
        unlocked_result = lineup_unlocked.match(img)
        if locked_result is not None and unlocked_result is None:
            top_left, bottom_right = locked_result
            cv2.rectangle(img, top_left, bottom_right, (0, 255, 0), 1)
            cv2.putText(img, "icon[locked]", top_left, cv2.FONT_HERSHEY_SIMPLEX, 0.3, (0, 255, 0), 1)
            state = 1
        elif locked_result is None and unlocked_result is not None:
            top_left, bottom_right = unlocked_result
            cv2.rectangle(img, top_left, bottom_right, (0, 255, 0), 1)
            cv2.putText(img, "icon[unlocked]", top_left, cv2.FONT_HERSHEY_SIMPLEX, 0.3, (0, 255, 0), 1)
            lineup_unlocked.click(handle)
        elif locked_result is not None and unlocked_result is not None:
            if lineup_locked.score > lineup_unlocked.score:
                top_left, bottom_right = locked_result
                cv2.rectangle(img, top_left, bottom_right, (0, 255, 0), 1)
                cv2.putText(img, "icon[locked]", top_left, cv2.FONT_HERSHEY_SIMPLEX, 0.3, (0, 255, 0), 1)
                state = 1
            else:
                top_left, bottom_right = unlocked_result
                cv2.rectangle(img, top_left, bottom_right, (0, 255, 0), 1)
                cv2.putText(img, "icon[unlocked]", top_left, cv2.FONT_HERSHEY_SIMPLEX, 0.3, (0, 255, 0), 1)
                lineup_unlocked.click(handle)
    elif state == 1:
        print("已锁定阵容")
        result = activitie_start.match(img)
        if result is not None:
            top_left, bottom_right = result
            cv2.rectangle(img, top_left, bottom_right, (0, 255, 0), 1)
            cv2.putText(img, "button[start]", top_left, cv2.FONT_HERSHEY_SIMPLEX, 0.3, (0, 255, 0), 1)
            activitie_start.click(handle)
            print("点击了开始按钮")
        else:
            print("已开始战斗")
            state = 2
    elif state == 2:
        result = battle_end_tag.match(img)
        if result is not None:
            top_left, bottom_right = result
            cv2.rectangle(img, top_left, bottom_right, (0, 255, 0), 1)
            cv2.putText(img, "tag[battle end]", top_left, cv2.FONT_HERSHEY_SIMPLEX, 0.3, (0, 255, 0), 1)
            battle_end_tag.click(handle)
            print("点击了战斗结束标签")
            state = 3
        else:
            print("战斗中")
    elif state == 3:
        result = battle_end_tag.match(img)
        if result is not None:
            top_left, bottom_right = result
            cv2.rectangle(img, top_left, bottom_right, (0, 255, 0), 1)
            cv2.putText(img, "tag[battle end]", top_left, cv2.FONT_HERSHEY_SIMPLEX, 0.3, (0, 255, 0), 1)
            battle_end_tag.click(handle)
            print("点击了战斗结束标签")
        else:
            print("战斗结束")
            state = 0
    else:
        print("停止运行")
    
    return state


# 斗技
def script_wrestling(img, handle, state):
    result = [None] * 8
    battle_stages = [battle_start, battle_ready, battle_manual, battle_auto, battle_victory, battle_defeat, battle_mvp, battle_bp_no_auto]
    button_texts = ["button[battle start]", "button[battle ready]", "button[battle manual]", "button[battle auto]", "tag[battle victory]", \
                    "tag[battle defeat]", "tag[battle mvp]", "button[bp auto]"]
    
    if 0 <= state <= 8:
        for i, stage in enumerate(battle_stages):
            result[i] = stage.match(img)
            if result[i] is not None:
                top_left, bottom_right = result[i]
                cv2.rectangle(img, top_left, bottom_right, (0, 255, 0), 1)
                cv2.putText(img, button_texts[i], top_left, cv2.FONT_HERSHEY_SIMPLEX, 0.3, (0, 255, 0), 1)
                if i != 3:  # 自动战斗，不需要点击
                    battle_stages[i].click(handle)
                    print(f"点击了{button_texts[i]}")
                else:
                    print("自动战斗中")
                return (i + 1)
    else:
        print("停止运行")
        
    return state


# 斗技 - 场景提示
def scene_wrestling(state):
    # 根据state更新场景显示文本
    if state == 0:
        scene_text = "stop"
    elif state == 1:
        scene_text = "battle scene"
    elif state == 2:
        scene_text = "battle ready"
    elif state == 3:
        scene_text = "battles"
    elif state == 4:
        scene_text = "battles"
    elif state == 5:
        scene_text = "battle victory"
    elif state == 6:
        scene_text = "battle defeat"
    elif state == 7:
        scene_text = "battle mvp"
    elif state == 8:
        scene_text = "bp"
    else:
        scene_text = "unknown"
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
    global acquired, max
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
                    print(f"点击了{button_texts[i]}")
                elif i == 4:
                    print("自动战斗中")
                elif i == 2:
                    print("已锁定阵容")
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
                            print("小绘卷已满，停止运行脚本")
                            state = 100
                        else:
                            click(handle=handle, x=112, y=122, waitCD=1)
                            click(handle=handle, x=112, y=122)
                            print("点击结算")
                    else:
                        acquired, max = 0, 0
                        print("未识别到小绘卷数量")
                return (i + 1)
    else:
        print("停止运行")
        
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