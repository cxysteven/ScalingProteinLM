import re
import pandas as pd
results = []

with open("./bj-cce-share-cpu0007-1003.log", 'r') as file:
    for line in file:
        # 使用正则表达式匹配所需的值
        if (match := re.search(r'iteration (\d+) \| lm loss value: ([\d\.E\+\-]+)', line)):
            iteration_number = int(match.group(1))
            lm_loss_value = float(match.group(2))
            # 计算Step值
            step_value = iteration_number * 6 * 1024 * 1024
            # 将结果添加到列表中
            results.append({"Wall time": 0, "Step": step_value, "Value": lm_loss_value})

df_results = pd.DataFrame(results)
df_results.to_csv('lm_loss.csv', index=False)
