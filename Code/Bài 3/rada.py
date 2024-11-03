import matplotlib.pyplot as plt
import pandas as pd
import numpy as np

df = pd.read_csv('results.csv', header=[0, 1, 2])
df.columns = [tuple('' if 'Unnamed:' in x else x for x in col) for col in df.columns]

p1 = "Max Aarons"  # Thay tên cầu thủ
p2 = "Tyler Adams"  # Thay tên cầu thủ
attributes = [('', 'Expected','npxG'), ('Passing','Long','Cmp'), ('Pass Types','Outcomes','Cmp')]  # Thay đổi danh sách các chỉ số muốn so sánh

# Trích xuất dữ liệu
data1 = df[df[('','','Player')] == p1][attributes].values.flatten()
data2 = df[df[('','','Player')] == p2][attributes].values.flatten()

# Thiết lập biểu đồ radar
labels = np.array(attributes)
num_vars = len(attributes)

# Tạo các góc cho biểu đồ radar
angles = np.linspace(0, 2 * np.pi, num_vars, endpoint=False).tolist()
data1 = np.concatenate((data1, [data1[0]]))  # Vòng lại điểm đầu
data2 = np.concatenate((data2, [data2[0]]))  # Vòng lại điểm đầu
angles += angles[:1]

# Vẽ biểu đồ radar
fig, ax = plt.subplots(figsize=(6, 6), subplot_kw=dict(polar=True))
ax.fill(angles, data1, color='blue', alpha=0.25, label=p1)
ax.fill(angles, data2, color='red', alpha=0.25, label=p2)
ax.plot(angles, data1, color='blue', linewidth=2)
ax.plot(angles, data2, color='red', linewidth=2)

# Thiết lập các nhãn
ax.set_yticklabels([])
ax.set_xticks(angles[:-1])
ax.set_xticklabels(labels)

# Thêm tiêu đề và chú thích
plt.title(f"So sánh cầu thủ {p1} và {p2}")
plt.legend(loc='upper right', bbox_to_anchor=(0.1, 0.1))
plt.show()