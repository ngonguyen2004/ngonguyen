import pandas as pd
# Đọc file CSV với header đa tầng
df_players = pd.read_csv('results.csv', header=[0, 1])
# Lưu lại hàng đầu tiên (giữ nguyên hàng này)
first_row = df_players.iloc[0:1].copy()
# Lấy dữ liệu từ hàng thứ 1 trở đi
df_data = df_players.iloc[1:].copy()
# Chuyển cột 'Age' sang kiểu số nguyên
df_data.loc[:, ('Unnamed: 4_level_0', 'Unnamed: 4_level_1')] = (
    pd.to_numeric(df_data[('Unnamed: 4_level_0', 'Unnamed: 4_level_1')], errors='coerce'))
# Sắp xếp theo tên cầu thủ và tuổi, giữ nguyên các giá trị N/A
df_data = df_data.sort_values(
    by=[('Unnamed: 0_level_0', 'Unnamed: 0_level_1'), ('Unnamed: 4_level_0', 'Unnamed: 4_level_1')],
    ascending=[True, True],
    na_position='last'  # Đặt N/A ở cuối, nếu muốn ở đầu, dùng 'first'
)
# Đặt lại chỉ số để giữ cho cột số thứ tự chính xác
df_data.reset_index(drop=True, inplace=True)
# Kết hợp lại với hàng đầu tiên
df_sorted = pd.concat([first_row, df_data], ignore_index=True)
# Ghi đè DataFrame đã sắp xếp vào file CSV với giá trị rỗng được thay thế bằng 'N/A'
df_sorted.to_csv('results.csv', index=False, na_rep='N/A')
print(df_sorted)
print("Sắp xếp và đổi tên cột thành công, file results.csv đã được cập nhật!")
