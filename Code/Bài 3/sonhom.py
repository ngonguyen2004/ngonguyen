import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans

# 1. Đọc dữ liệu từ file CSV
df = pd.read_csv('results.csv', header=[0, 1, 2])
df[('Unnamed: 7_level_0', 'Playing Time', 'Min')] = df[('Unnamed: 7_level_0', 'Playing Time', 'Min')].replace({',': ''}, regex=True).astype(float)

# 2. Chọn các chỉ số cần thiết cho phân cụm
features = df[[  # Chọn các cột chỉ số mà bạn muốn sử dụng
    ('Unnamed: 7_level_0', 'Playing Time', 'Min'), # Thời gian thi đấu tổng cộng (phút)
    ('Unnamed: 9_level_0', 'Performance', 'G-PK'), # Số bàn thắng (không tính penalty)
    ('Unnamed: 20_level_0', 'Per 90 minutes', 'Ast'), # Số đường chuyền kiến tạo
    ('Shooting', 'Standard', 'Gls'), # Tổng số bàn thắng
    ('Defensive Actions', 'Blocks', 'Blocks'), # số lần cầu thủ chặn được các cú sút, đường chuyền
    ('Possession', 'Touches', 'Touches'), # Số lần chạm bóng
    ('Passing', 'Total.2', 'Cmp%'), # Tỉ lệ chuyền thành công
    ('Shooting', 'Expected', 'xG'), # Bàn thắng dự kiến
    ('Passing', 'Expected.1', 'xAG'), # Dự đoán số kiến tạo
    ('Miscellaneous Stats', 'Performance.5', 'Recov') # Số lần thu hồi bóng
]]

# 3. Xóa các hàng có giá trị NaN
features = features.dropna()

# 4. Chuẩn hóa dữ liệu
scaler = StandardScaler()
scaled_features = scaler.fit_transform(features)

# 5. Áp dụng K-means
kmeans = KMeans(n_clusters=3, random_state=0).fit(scaled_features)

# 6. Thêm nhãn phân cụm vào DataFrame `features`
features['Cluster'] = kmeans.labels_ + 1  # Bắt đầu đánh số từ 1

# 7. Sắp xếp DataFrame trước khi nhóm
features = features.sort_index(level=0, axis=1)

# 8. Tính toán trung bình cho mỗi nhóm
grouped = features.groupby('Cluster').mean()

# 9. Nhận xét dựa trên trung bình
for cluster in grouped.index:
    print(f"\nNhóm {int(cluster)}:")  # Đảm bảo in số nhóm nguyên
    for stat in grouped.columns:
        # Lấy tên của tầng cuối cùng
        stat_name = stat[-1] if isinstance(stat, tuple) else stat
        print(f"  Trung bình {stat_name}: {grouped.loc[cluster, stat]:.2f}")

    # Nhận xét cụ thể
    if grouped.loc[cluster, ('Unnamed: 7_level_0', 'Playing Time', 'Min')] > 1000:
        print("  Nhóm này có thời gian thi đấu cao, có thể là cầu thủ chủ chốt trong đội.")
    else:
        print("  Nhóm này có thể là cầu thủ dự bị hoặc ít thi đấu.")

    if grouped.loc[cluster, ('Unnamed: 9_level_0', 'Performance', 'G-PK')] > 10:
        print("  Nhóm này có hiệu suất ghi bàn cao.")
    else:
        print("  Nhóm này cần cải thiện khả năng ghi bàn.")

    if grouped.loc[cluster, ('Miscellaneous Stats', 'Performance.5', 'Recov')] > 20:
        print("  Nhóm này có khả năng thu hồi bóng tốt.")
    else:
        print("  Nhóm này có thể cần cải thiện khả năng thu hồi bóng.")
