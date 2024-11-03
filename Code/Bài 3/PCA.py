import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans
from sklearn.decomposition import PCA
import matplotlib.pyplot as plt

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

# Kiểm tra và loại bỏ bất kỳ hàng nào có giá trị NaN trong cột 'Cluster'
features = features[features['Cluster'].notna()]

# 7. Thực hiện PCA để giảm số chiều dữ liệu xuống 2
pca = PCA(n_components=2)
pca_result = pca.fit_transform(scaled_features)

# 8. Tạo DataFrame cho kết quả PCA
pca_df = pd.DataFrame(data=pca_result, columns=['PC1', 'PC2'])
pca_df['Cluster'] = features['Cluster'].values  # Chuyển giá trị Cluster vào DataFrame PCA

# 9. Vẽ hình phân cụm trên mặt 2D
plt.figure(figsize=(10, 8))
colors = plt.cm.viridis(np.linspace(0, 1, 3))  # Màu cho 3 cụm

for cluster in np.unique(pca_df['Cluster']):
    plt.scatter(pca_df[pca_df['Cluster'] == cluster]['PC1'],
                pca_df[pca_df['Cluster'] == cluster]['PC2'],
                label=f'Nhóm {int(cluster)}',
                color=colors[int(cluster)-1],
                alpha=0.7)

plt.title('K-means Clustering of Player Statistics (PCA)')
plt.xlabel('Principal Component 1')
plt.ylabel('Principal Component 2')
plt.legend()
plt.grid()
plt.show()
