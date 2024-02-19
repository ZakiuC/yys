import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from datetime import datetime

# 解析文本文件中的数据
timestamps = []
current_scores = []
max_scores = []

with open('pvp_scores.txt', 'r') as f:
    for line in f:
        parts = line.split('----')
        scores = parts[0].split('\t')
        timestamp = datetime.strptime(parts[1].strip(), "%Y-%m-%d %H:%M:%S")
        
        current_score = int(scores[0].split(':')[1])
        max_score = int(scores[1].split(':')[1].split(' ')[1])
        
        timestamps.append(timestamp)
        current_scores.append(current_score)
        max_scores.append(max_score)


# 绘制折线图
plt.figure(figsize=(10, 5))
plt.plot(timestamps, current_scores, 'o-', label='CurrentScore')
plt.plot(timestamps, max_scores, 'o-', label='HighestScore')

# 添加 x 轴和 y 轴的标签
for i in range(len(timestamps)):
    plt.text(timestamps[i], current_scores[i], f'{current_scores[i]}', fontsize=5)

# 设置图形的格式
plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d %H:%M:%S'))
plt.gca().xaxis.set_major_locator(mdates.DayLocator())
plt.gcf().autofmt_xdate()

plt.legend()
plt.grid(True)
plt.title('PVP SCORE')
plt.xlabel('TIME')
plt.ylabel('SCORE')

now = datetime.now()  # 获取当前时间
timestamp = now.strftime("%Y-%m-%d[%H-%M]")  # 替换冒号为下划线
# 保存图形
plt.savefig(f'static/analyzData/pvp_score_{timestamp}.png')
