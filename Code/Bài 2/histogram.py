import pandas as pd
import matplotlib.pyplot as plt
import os

# Tạo thư mục histograms nếu chưa tồn tại
if not os.path.exists('histograms'):
    os.makedirs('histograms')

# Đọc tệp CSV với header đa tầng
df = pd.read_csv('results.csv', header=[0, 1, 2])

# Loại bỏ 3 cột đầu tiên ('Player', 'Nation', 'Team')
df_stats = df.iloc[:, 4:]  # Chỉ giữ các cột từ cột thứ 4 trở đi (các chỉ số)

# Chuyển đổi các cột thành số và loại bỏ dấu phẩy
for col in df_stats.columns:
    df_stats[col] = df_stats[col].astype(str).str.replace(',', '', regex=False).astype(float)

# Vẽ histogram cho từng chỉ số của toàn bộ cầu thủ
for column in df_stats.columns:
    stat_name = column[2]  # Lấy tên bậc thứ 3 (có thể là "1/3")
    plt.figure(figsize=(10, 5))
    plt.hist(df_stats[column].dropna(), bins=30, alpha=0.7, color='blue')  # Bỏ NaN khi vẽ
    plt.title(f'HISTOGRAM: Phân bố chỉ số {stat_name} của toàn bộ cầu thủ')
    plt.xlabel('Giá trị')
    plt.ylabel('Tần suất')
    plt.grid(axis='y', alpha=0.75)

    # Thay thế các ký tự không hợp lệ trong tên tệp
    stat_name_safe = stat_name.replace("/", "_").replace('"', '')  # Thay ký tự không hợp lệ
    plt.savefig(f'histograms/histogram_all_players_{stat_name_safe}.png')
    plt.close()  # Đóng hình để không hiển thị nữa

print("Các histogram đã được lưu vào tệp trong thư mục 'histograms'.")
