[English](./README.EN.md) | 简体中文
# 项目
> 阴阳师监控脚本 
# 版本
> V1.0.1


# 结构
> - [static](./static/) - 静态文件
> - [static/images](./static/images/) - 用于模板匹配的图片
> - [grabscreen.py](./grabscreen.py) - windows窗口内容截取
> - [loadModel.py](./loadModel.py) - 目标图片加载，用于模板匹配
> - [test.py](./test.py) - 测试脚本


# 更新记录
## V1.0.1 - 2024年1月8日
### 新增
- [检查脚本运行权限](./test.py#L205-L208)
- [添加了键盘/鼠标输入的模拟](./loadModel.py#L114-L318)
- 类[TargetImage](./loadModel.py#L28-L70)中添加[click](./loadModel.py#L59-L70)方法
