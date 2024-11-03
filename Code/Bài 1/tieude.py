import pandas as pd
import os

# Đường dẫn đến file result.csv
file_path = 'results.csv'

# Tiêu đề cột với MultiIndex
column_titles = pd.MultiIndex.from_tuples([
    ('', '', 'Player'), ('', '', 'Nation'), ('', '', 'Team'), ('', '', 'Pos'), ('', '', 'Age'),
    ('', '', 'MP'),
    ('', 'Playing Time', 'Starts'), ('', 'Playing Time', 'Min'), ('', 'Playing Time', '90s'),
    ('', 'Performance', 'G-PK'), ('', 'Performance', 'PKatt'), ('', 'Performance', 'CrdY'), ('', 'Performance', 'CrdR'),
    ('', 'Expected', 'xG'), ('', 'Expected', 'npxG'), ('', 'Expected', 'xAG'),
    ('', 'Progression', 'PrgC'), ('', 'Progression', 'PrgP'), ('', 'Progression', 'PrgR'),
    ('', 'Per 90 minutes', 'Gls'), ('', 'Per 90 minutes', 'Ast'), ('', 'Per 90 minutes', 'G+A'),
    ('', 'Per 90 minutes', 'G-PK'), ('', 'Per 90 minutes', 'G+A-PK'), ('', 'Per 90 minutes', 'xG'),
    ('', 'Per 90 minutes', 'xAG'), ('', 'Per 90 minutes', 'xG+AG'), ('', 'Per 90 minutes', 'npxG'),
    ('Goalkeeping', 'Performance', 'GA'), ('Goalkeeping', 'Performance', 'GA90'),
    ('Goalkeeping', 'Performance', 'SoTA'), ('Goalkeeping', 'Performance', 'Saves'),
    ('Goalkeeping', 'Performance', 'Save%'), ('Goalkeeping', 'Performance', 'W'),
    ('Goalkeeping', 'Performance', 'D'), ('Goalkeeping', 'Performance', 'L'),
    ('Goalkeeping', 'Performance', 'CS'), ('Goalkeeping', 'Performance', 'CS%'),
    ('Goalkeeping', 'Penalty Kick', 'PKatt'), ('Goalkeeping', 'Penalty Kick', 'PKA'),
    ('Goalkeeping', 'Penalty Kick', 'PKsv'), ('Goalkeeping', 'Penalty Kick', 'PKm'),
    ('Goalkeeping', 'Penalty Kick', 'Save%'),
    ('Shooting', 'Standard', 'Gls'), ('Shooting', 'Standard', 'Sh'), ('Shooting', 'Standard', 'SoT'),
    ('Shooting', 'Standard', 'SoT%'), ('Shooting', 'Standard', 'Sh/90'), ('Shooting', 'Standard', 'SoT/90'),
    ('Shooting', 'Standard', 'G/Sh'), ('Shooting', 'Standard', 'G/SoT'), ('Shooting', 'Standard', 'Dist'),
    ('Shooting', 'Standard', 'FK'), ('Shooting', 'Standard', 'PK'), ('Shooting', 'Standard', 'PKatt'),
    ('Shooting', 'Expected', 'xG'), ('Shooting', 'Expected', 'npxG'), ('Shooting', 'Expected', 'npxG/Sh'),
    ('Shooting', 'Expected', 'G-xG'), ('Shooting', 'Expected', 'np:G-xG'),
    ('Passing', 'Total', 'Cmp'), ('Passing', 'Total', 'Att'), ('Passing', 'Total', 'Cmp%'),
    ('Passing', 'Total', 'TotDist'), ('Passing', 'Total', 'PrgDist'),
    ('Passing', 'Short', 'Cmp'), ('Passing', 'Short', 'Att'), ('Passing', 'Short', 'Cmp%'),
    ('Passing', 'Medium', 'Cmp'), ('Passing', 'Medium', 'Att'), ('Passing', 'Medium', 'Cmp%'),
    ('Passing', 'Long', 'Cmp'), ('Passing', 'Long', 'Att'), ('Passing', 'Long', 'Cmp%'),
    ('Passing', 'Expected', 'Ast'), ('Passing', 'Expected', 'xAG'), ('Passing', 'Expected', 'xA'),
    ('Passing', 'Expected', 'A-xAG'), ('Passing', 'Expected', 'KP'), ('Passing', 'Expected', '"1/3"'),
    ('Passing', 'Expected', 'PPA'), ('Passing', 'Expected', 'CrsPA'), ('Passing', 'Expected', 'PrgP'),
    ('Pass Types', 'Pass Types', 'Live'), ('Pass Types', 'Pass Types', 'Dead'), ('Pass Types', 'Pass Types', 'FK'),
    ('Pass Types', 'Pass Types', 'TB'), ('Pass Types', 'Pass Types', 'Sw'), ('Pass Types', 'Pass Types', 'Crs'),
    ('Pass Types', 'Pass Types', 'TI'), ('Pass Types', 'Pass Types', 'CK'),
    ('Pass Types', 'Corner Kicks', 'In'), ('Pass Types', 'Corner Kicks', 'Out'), ('Pass Types', 'Corner Kicks', 'Str'),
    ('Pass Types', 'Outcomes', 'Cmp'), ('Pass Types', 'Outcomes', 'Off'), ('Pass Types', 'Outcomes', 'Blocks'),
    ('Goal and Shot Creation', 'SCA', 'SCA'), ('Goal and Shot Creation', 'SCA', 'SCA90'),
    ('Goal and Shot Creation', 'SCA Types', 'PassLive'), ('Goal and Shot Creation', 'SCA Types', 'PassDead'),
    ('Goal and Shot Creation', 'SCA Types', 'TO'), ('Goal and Shot Creation', 'SCA Types', 'Sh'),
    ('Goal and Shot Creation', 'SCA Types', 'Fld'), ('Goal and Shot Creation', 'SCA Types', 'Def'),
    ('Goal and Shot Creation', 'GCA', 'GCA'), ('Goal and Shot Creation', 'GCA', 'GCA90'),
    ('Goal and Shot Creation', 'GCA Types', 'PassLive'), ('Goal and Shot Creation', 'GCA Types', 'PassDead'),
    ('Goal and Shot Creation', 'GCA Types', 'TO'), ('Goal and Shot Creation', 'GCA Types', 'Sh'),
    ('Goal and Shot Creation', 'GCA Types', 'Fld'), ('Goal and Shot Creation', 'GCA Types', 'Def'),
    ('Defensive Actions', 'Tackles', 'Tkl'), ('Defensive Actions', 'Tackles', 'TklW'),
    ('Defensive Actions', 'Tackles', 'Def 3rd'),
    ('Defensive Actions', 'Tackles', 'Mid 3rd'), ('Defensive Actions', 'Tackles', 'Att 3rd'),
    ('Defensive Actions', 'Challenges', 'Tkl'), ('Defensive Actions', 'Challenges', 'Att'),
    ('Defensive Actions', 'Challenges', 'Tkl%'), ('Defensive Actions', 'Challenges', 'Lost'),
    ('Defensive Actions', 'Blocks', 'Blocks'), ('Defensive Actions', 'Blocks', 'Sh'),
    ('Defensive Actions', 'Blocks', 'Pass'), ('Defensive Actions', 'Blocks', 'Int'),
    ('Defensive Actions', 'Blocks', 'Tkl+Int'), ('Defensive Actions', 'Blocks', 'Clr'),
    ('Defensive Actions', 'Blocks', 'Err'),
    ('Possession', 'Touches', 'Touches'), ('Possession', 'Touches', 'Def Pen'), ('Possession', 'Touches', 'Def 3rd'),
    ('Possession', 'Touches', 'Mid 3rd'), ('Possession', 'Touches', 'Att 3rd'), ('Possession', 'Touches', 'Att Pen'),
    ('Possession', 'Touches', 'Live'),
    ('Possession', 'Take-Ons', 'Att'), ('Possession', 'Take-Ons', 'Succ'), ('Possession', 'Take-Ons', 'Succ%'),
    ('Possession', 'Take-Ons', 'Tkld'), ('Possession', 'Take-Ons', 'Tkld%'),
    ('Possession', 'Carries', 'Carries'), ('Possession', 'Carries', 'TotDist'), ('Possession', 'Carries', 'PrgDist'),
    ('Possession', 'Carries', 'PrgC'), ('Possession', 'Carries', '"1/3'), ('Possession', 'Carries', 'CPA'),
    ('Possession', 'Carries', 'Mis'), ('Possession', 'Carries', 'Dis'),
    ('Possession', 'Receiving', 'ReC'), ('Possession', 'Receiving', 'PrgR'),
    ('Playing Time', 'Starts', 'Starts'), ('Playing Time', 'Starts', 'Mn/Start'), ('Playing Time', 'Starts', 'Compl'),
    ('Playing Time', 'Starts', 'Subs'), ('Playing Time', 'Starts', 'Mn/Sub'), ('Playing Time', 'Starts', 'unSub'),
    ('Playing Time', 'Team Success', 'PPM'), ('Playing Time', 'Team Success', 'onG'),
    ('Playing Time', 'Team Success', 'onGA'),
    ('Playing Time', 'Team Success(xG)', 'onxG'), ('Playing Time', 'Team Success(xG)', 'onxGA'),
    ('Miscellaneous Stats', 'Performance', 'Fls'), ('Miscellaneous Stats', 'Performance', 'Fld'),
    ('Miscellaneous Stats', 'Performance', 'Off'), ('Miscellaneous Stats', 'Performance', 'Crs'),
    ('Miscellaneous Stats', 'Performance', 'OG'), ('Miscellaneous Stats', 'Performance', 'Recov'),
    ('Miscellaneous Stats', 'Aerial Duels', 'Won'), ('Miscellaneous Stats', 'Aerial Duels', 'Lost'),
    ('Miscellaneous Stats', 'Aerial Duels', 'Won%'),
])

# Kiểm tra xem file có tồn tại không
if os.path.exists(file_path):
    # Xóa nội dung trong file
    open(file_path, 'w').close()

# Tạo DataFrame với tiêu đề cột
df_empty = pd.DataFrame(columns=column_titles)

# Ghi tiêu đề vào file
df_empty.to_csv(file_path, index=False)

print(f"File {file_path} đã được tạo lại với tiêu đề.")
