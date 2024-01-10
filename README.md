[English](./README.EN.md) | 简体中文
# 项目
> 阴阳师监控脚本 
# 版本
> V1.0.2 - 


# 结构
> - [static](./static/) - 静态文件
> - [static/images](./static/images/) - 用于模板匹配的图片
> - [grabscreen.py](./grabscreen.py) - windows窗口内容截取
> - [loadModel.py](./loadModel.py) - 目标图片加载，用于模板匹配，附带键盘/鼠标模拟输入
> - [test.py](./test.py) - 测试脚本


# 更新记录
## 活动刷1800体用
> ### 新增
> - [test.py](./test.py#L307-L364)新增新活动副本1800体的脚本，详细：
> 在活动界面识别阵容锁定图标，未锁定则点击锁定，锁定完阵容后寻找[挑战]按钮点击开始战斗，战斗结束后循环第一步。（具体流程可自己更改）

## V1.0.2 - 2024年1月9日
> ### 新增
> - 类[TargetImage](./loadModel.py#L52)新增[match_all](./loadModel.py#L83-L104)方法，返回匹配到的所有目标
> - [loadModel.py](./loadModel.py)新增[click](./loadModel.py#L425-L454)方法，点击指定坐标
> - [test.py](./test.py#L309-L329)新增当前场景的提示在hook窗口的右上角
> - [test.py](./test.py#L182-L306)新增结界突破的处理，从庭院自动到寮突破的界面，点击突破失败的下一位
> ### 修改
> - 类[TargetImage](./loadModel.py#L52)的[click](./loadModel.py#L106-L133)方法添加位置和时间的随机偏移以对抗自动化检测
> ### 修复
> - 添加了[map_to_original](./loadModel.py#L29)方法以解决监控窗口和原始窗口分辨率不一致导致点击位置不准确的问题


## V1.0.1 - 2024年1月8日
> ### 新增
> - [检查脚本运行权限](./test.py#L205-L208)
> - [添加了键盘/鼠标输入的模拟](./loadModel.py#L114-L318)
> - 类[TargetImage](./loadModel.py#L28-L70)中添加[click](./loadModel.py#L59-L70)方法