# -*- coding: utf-8 -*-
'''
Author       : ZakiuC
Date         : 2024-01-04 14:00:59
LastEditors  : ZakiuC z2337070680@163.com
LastEditTime : 2024-01-05 09:05:16
FilePath     : \yys\loadModel.py
Description  : 
Copyright (c) 2024 by ZakiuC z2337070680@163.com, All Rights Reserved. 
'''
import cv2
import os


# 获取当前文件的绝对路径
current_file_path = os.path.abspath(__file__)
# 获取当前文件所在目录的路径
current_dir = os.path.dirname(current_file_path)
# 构建到 static/images/ 的路径
path_to_images = os.path.join(current_dir, "static", "images")


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
        if max_val >= self.threshold:
            top_left = max_loc  # 使用最大值位置作为左上角坐标
            bottom_right = (top_left[0] + self.width, top_left[1] + self.height)  # 计算右下角坐标
            self.pos_x = top_left[0] + self.width // 2
            self.pos_y = top_left[1] + self.height // 2

            return top_left, bottom_right
        else:
            return None






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

