import pandas as pd

# Đọc tệp CSV với header đa tầng
df = pd.read_csv('results.csv', header=[0, 1, 2])

# Duyệt qua từng cột bắt đầu từ cột thứ 6 (chỉ số 5)
for col_index in range(4, df.shape[1]):  # Bắt đầu từ cột thứ 6
    column_name = df.columns[col_index]  # Lấy tên cột

    # Xóa dấu phẩy và chuyển đổi cột thành kiểu số (nếu chưa)
    df[column_name] = df[column_name].astype(str).str.replace(',', '', regex=False).astype(float)

    # Kiểm tra nếu cột có kiểu số trước khi sử dụng nlargest
    if df[column_name].notna().any():  # Kiểm tra nếu có giá trị số hợp lệ
        # Lấy 3 cầu thủ có chỉ số cao nhất
        top3 = df.nlargest(3, column_name)

        # In tên cầu thủ có chỉ số cao nhất
        print(f"\n3 cầu thủ có chỉ số cao nhất của cột '{' | '.join(column_name)}' là:")
        for index, row in top3.iterrows():
            player_name = row[('Unnamed: 0_level_0', 'Unnamed: 0_level_1', 'Player')]
            print(player_name)

        # Lấy 3 cầu thủ có chỉ số thấp nhất
        bottom3 = df.nsmallest(3, column_name)

        # In tên cầu thủ có chỉ số thấp nhất
        print(f"\n3 cầu thủ có chỉ số thấp nhất của cột '{' | '.join(column_name)}' là:")
        for index, row in bottom3.iterrows():
            player_name = row[('Unnamed: 0_level_0', 'Unnamed: 0_level_1', 'Player')]
            print(player_name)
    else:
        print(f"Cột '{column_name}' không có giá trị số hợp lệ. Bỏ qua.")
