import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans
from sklearn.decomposition import PCA
import matplotlib.pyplot as plt

# 1. Đọc dữ liệu từ file CSV
df = pd.read_csv('results.csv', header=[0, 1, 2])

# 2. Chuyển cột 'Playing Time - Min' sang kiểu số
df[('Unnamed: 7_level_0', 'Playing Time', 'Min')] = df[('Unnamed: 7_level_0', 'Playing Time', 'Min')].replace({',': ''}, regex=True).astype(float)

# 3. Chọn các chỉ số cần thiết cho phân cụm
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


# 4. Xóa các hàng có giá trị NaN và lưu lại chỉ số ban đầu
features = features.dropna()
original_indices = features.index

# 5. Chuẩn hóa dữ liệu
scaler = StandardScaler()
scaled_features = scaler.fit_transform(features)

# 6. Áp dụng K-means với số cụm tối ưu
kmeans = KMeans(n_clusters=3, random_state=42)
kmeans.fit(scaled_features)

# 7. Thêm nhãn phân cụm vào DataFrame `features`
features['Cluster'] = kmeans.labels_

# 8. Gán nhãn phân cụm vào DataFrame ban đầu `df` theo chỉ số
df['Cluster'] = np.nan  # Khởi tạo cột Cluster với NaN
df.loc[original_indices, 'Cluster'] = kmeans.labels_  # Gán nhãn theo chỉ số ban đầu

# 9. Giảm chiều dữ liệu xuống 2D bằng PCA để trực quan hóa
pca = PCA(n_components=2)
pca_features = pca.fit_transform(scaled_features)

# 10. Trực quan hóa các cụm
plt.scatter(pca_features[:, 0], pca_features[:, 1], c=kmeans.labels_, cmap='viridis', s=20)
plt.xlabel('PC 1')
plt.ylabel('PC 2')
plt.title('Phân cụm cầu thủ bằng K-means (giảm chiều với PCA)')
plt.colorbar(label='Cluster')
plt.show()
