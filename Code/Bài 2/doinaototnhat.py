import pandas as pd

# Đọc tệp CSV với header đa tầng
df = pd.read_csv('results.csv', header=[0, 1, 2])

# Loại bỏ 3 cột đầu tiên ('Player', 'Nation', 'Team')
df_stats = df.iloc[:, 4:]  # Chỉ giữ các cột từ cột thứ 4 trở đi (các chỉ số)

# Chuyển đổi các giá trị trong cột số 7 thành số thực, bỏ dấu phẩy
df_stats.iloc[:, 3] = df_stats.iloc[:, 3].replace(',', '', regex=True).astype(float)

# Nhóm các cầu thủ theo 'Team' và tính toán trung bình chỉ số của từng đội
df_team_stats = df_stats.groupby(df[('Unnamed: 2_level_0', 'Unnamed: 2_level_1', 'Team')]).mean()

# Tìm đội có chỉ số cao nhất cho từng chỉ số
highest_stats_teams = df_team_stats.idxmax(axis=0)
highest_stats_values = df_team_stats.max(axis=0)

# Tạo từ điển để đếm số chỉ số cao nhất cho từng đội
team_score_count = {}

# Đếm số chỉ số cao nhất cho từng đội
for stat in highest_stats_teams.index:
    team = highest_stats_teams[stat]

    # Tăng số chỉ số cao nhất của đội lên 1
    if team in team_score_count:
        team_score_count[team] += 1
    else:
        team_score_count[team] = 1

# Tìm đội có nhiều chỉ số cao nhất
best_team = max(team_score_count, key=team_score_count.get)
best_team_count = team_score_count[best_team]

# In ra kết quả
for stat in highest_stats_teams.index:
    team = highest_stats_teams[stat]
    value = highest_stats_values[stat]

    # Lấy tên bậc thứ 3 từ chỉ số
    stat_name = stat[2]  # Lấy tên bậc thứ 3 trong tuple stat
    print(f'Đội bóng có chỉ số điểm cao nhất ở chỉ số {stat_name} là: {team} với giá trị = {value:.2f}')

print(f'\nĐội bóng có phong độ tốt nhất giải ngoại Hạng Anh mùa 2023-2024 là: '
      f'{best_team} với {best_team_count} chỉ số cao nhất.')
