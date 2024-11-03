import requests
import pandas as pd
from bs4 import BeautifulSoup as bs
import time
import os
# Danh sách các URL
urls = [
    'https://fbref.com/en/squads/822bd0ba/2023-2024/Liverpool-Stats',
    'https://fbref.com/en/squads/b8fd03ef/2023-2024/Manchester-City-Stats',
    'https://fbref.com/en/squads/18bb7c10/2023-2024/Arsenal-Stats',
    'https://fbref.com/en/squads/cff3d9bb/2023-2024/Chelsea-Stats',
    'https://fbref.com/en/squads/8602292d/2023-2024/Aston-Villa-Stats',
    'https://fbref.com/en/squads/d07537b9/2023-2024/Brighton-and-Hove-Albion-Stats',
    'https://fbref.com/en/squads/b2b47a98/2023-2024/Newcastle-United-Stats',
    'https://fbref.com/en/squads/fd962109/2023-2024/Fulham-Stats',
    'https://fbref.com/en/squads/361ca564/2023-2024/Tottenham-Hotspur-Stats',
    'https://fbref.com/en/squads/e4a775cb/2023-2024/Nottingham-Forest-Stats',
    'https://fbref.com/en/squads/cd051869/2023-2024/Brentford-Stats',
    'https://fbref.com/en/squads/7c21e445/2023-2024/West-Ham-United-Stats',
    'https://fbref.com/en/squads/4ba7cbea/2023-2024/Bournemouth-Stats',
    'https://fbref.com/en/squads/19538871/2023-2024/Manchester-United-Stats',
    'https://fbref.com/en/squads/a2d435b3/2023-2024/Leicester-City-Stats',
    'https://fbref.com/en/squads/d3fd31cc/2023-2024/Everton-Stats',
    'https://fbref.com/en/squads/b74092de/2023-2024/Ipswich-Town-Stats',
    'https://fbref.com/en/squads/47c64c55/2023-2024/Crystal-Palace-Stats',
    'https://fbref.com/en/squads/33c895d4/2023-2024/Southampton-Stats',
    'https://fbref.com/en/squads/8cec06e1/2023-2024/Wolverhampton-Wanderers-Stats',
    # Thêm các URL khác vào đây
]


def scrape_player_data(url):
    r = requests.get(url)
    soup = bs(r.content, 'html.parser')
    player_data = []
    table = soup.find('table', attrs={'id': 'stats_standard_9'})
    if table:
        rows = table.find_all('tr')
        for row in rows[1:]:
            cols = row.find_all('td')
            if len(cols) > 0:
                player_name = row.find('th').text.strip()
                if player_name in ['Squad Total', 'Opponent Total']:
                    continue
                nation = cols[0].text.strip()
                team = url.split("/")[7].replace('-Stats', '')
                pos = cols[1].text.strip()
                age = cols[2].text.strip()
                mp = cols[3].text.strip()
                starts = cols[4].text.strip()
                min = cols[5].text.strip()
                s90 = cols[6].text.strip()
                g_pk = cols[10].text.strip()
                pkatt = cols[12].text.strip()
                crdy = cols[13].text.strip()
                crdr = cols[14].text.strip()
                xg = cols[15].text.strip()
                npxg = cols[16].text.strip()
                xag = cols[17].text.strip()
                prgc = cols[19].text.strip()
                prgp = cols[20].text.strip()
                prgr = cols[21].text.strip()
                gls = cols[22].text.strip()
                ast = cols[23].text.strip()
                g_a = cols[24].text.strip()
                gpk = cols[25].text.strip()
                gapk = cols[26].text.strip()
                x_g = cols[27].text.strip()
                x_ag = cols[28].text.strip()
                xg_xag = cols[29].text.strip()
                npx_g = cols[30].text.strip()
                try:
                    minutes_played = int(min.replace(',', ''))
                except ValueError:
                    minutes_played = 0

                if minutes_played > 90:
                    player_data.append(
                        [player_name, nation, team, pos, age, mp, starts, min, s90, g_pk, pkatt, crdy, crdr, xg,
                            npxg, xag, prgc, prgp, prgr, gls, ast, g_a, gpk, gapk, x_g, x_ag, xg_xag, npx_g])
    return player_data


def scrape_keeper_data(url):
    r = requests.get(url)
    soup = bs(r.content, 'html.parser')
    player_data = []
    table = soup.find('table', attrs={'id': 'stats_keeper_9'})
    if table:
        rows = table.find_all('tr')
        for row in rows[1:]:  # Bỏ qua hàng tiêu đề
            cols = row.find_all('td')
            if len(cols) > 0:  # Bỏ qua các hàng trống
                player_name = row.find('th').text.strip()
                if player_name in ['Squad Total', 'Opponent Total']:
                    continue
                ga = cols[7].text.strip()
                ga90 = cols[8].text.strip()
                sota = cols[9].text.strip()
                save = cols[10].text.strip()
                save5 = cols[11].text.strip()
                w = cols[12].text.strip()
                d = cols[13].text.strip()
                l = cols[14].text.strip()
                cs = cols[15].text.strip()
                cs5 = cols[16].text.strip()
                pkatt = cols[17].text.strip()
                pka = cols[18].text.strip()
                pksv = cols[19].text.strip()
                pkm = cols[20].text.strip()
                save_5 = cols[21].text.strip()
                player_data.append([player_name, ga, ga90, sota, save, save5, w, d, l, cs, cs5,
                                    pkatt, pka, pksv, pkm, save_5])
    return player_data


def scrape_shooting_data(url):
    r = requests.get(url)
    soup = bs(r.content, 'html.parser')
    player_data = []
    table = soup.find('table', attrs={'id': 'stats_shooting_9'})
    if table:
        rows = table.find_all('tr')
        for row in rows[1:]:  # Bỏ qua hàng tiêu đề
            cols = row.find_all('td')
            if len(cols) > 0:  # Bỏ qua các hàng trống
                player_name = row.find('th').text.strip()  # Lấy tên cầu thủ từ thẻ <th>
                # Bỏ qua các cầu thủ có tên "Squad Total" hoặc "Opponent Total"
                if player_name in ['Squad Total', 'Opponent Total']:
                    continue
                gls = cols[4].text.strip()
                sh = cols[5].text.strip()
                sot = cols[6].text.strip()
                sot5 = cols[7].text.strip()
                sh90 = cols[8].text.strip()
                sot90 = cols[9].text.strip()
                gsh = cols[10].text.strip()
                gsot = cols[11].text.strip()
                dist = cols[12].text.strip()
                fk = cols[13].text.strip()
                pk = cols[14].text.strip()
                pkatt = cols[15].text.strip()
                xg = cols[16].text.strip()
                npxg = cols[17].text.strip()
                npxgsh = cols[18].text.strip()
                gxg = cols[19].text.strip()
                npgxg = cols[20].text.strip()
                player_data.append([player_name, gls, sh, sot, sot5, sh90, sot90, gsh, gsot, dist, fk,
                                    pk, pkatt, xg, npxg, npxgsh, gxg, npgxg])
    return player_data


def scrape_passing_data(url):
    r = requests.get(url)
    soup = bs(r.content, 'html.parser')
    player_data = []
    table = soup.find('table', attrs={'id': 'stats_passing_9'})
    if table:
        rows = table.find_all('tr')
        for row in rows[1:]:  # Bỏ qua hàng tiêu đề
            cols = row.find_all('td')
            if len(cols) > 0:  # Bỏ qua các hàng trống
                player_name = row.find('th').text.strip()  # Lấy tên cầu thủ từ thẻ <th>
                # Bỏ qua các cầu thủ có tên "Squad Total" hoặc "Opponent Total"
                if player_name in ['Squad Total', 'Opponent Total']:
                    continue
                tcmp = cols[4].text.strip()
                tatt = cols[5].text.strip()
                tcmp5 = cols[6].text.strip()
                totdist = cols[7].text.strip()
                prgdist = cols[8].text.strip()
                scmp = cols[9].text.strip()
                satt = cols[10].text.strip()
                scmp5 = cols[11].text.strip()
                mcmp = cols[12].text.strip()
                matt = cols[13].text.strip()
                mcmp5 = cols[14].text.strip()
                lcmp = cols[15].text.strip()
                latt = cols[16].text.strip()
                lcmp5 = cols[17].text.strip()
                ast = cols[18].text.strip()
                xag = cols[19].text.strip()
                xa = cols[20].text.strip()
                axag = cols[21].text.strip()
                kp = cols[22].text.strip()
                e13 = cols[23].text.strip()
                ppa = cols[24].text.strip()
                crspa = cols[25].text.strip()
                prgp = cols[26].text.strip()
                player_data.append([player_name, tcmp, tatt, tcmp5, totdist, prgdist, scmp, satt, scmp5, mcmp, matt,
                                    mcmp5, lcmp, latt, lcmp5, ast, xag, xa, axag, kp, e13, ppa, crspa, prgp])
    return player_data


def scrape_passtypes_data(url):
    r = requests.get(url)
    soup = bs(r.content, 'html.parser')
    player_data = []
    table = soup.find('table', attrs={'id': 'stats_passing_types_9'})
    if table:
        rows = table.find_all('tr')
        for row in rows[1:]:  # Bỏ qua hàng tiêu đề
            cols = row.find_all('td')
            if len(cols) > 0:  # Bỏ qua các hàng trống
                player_name = row.find('th').text.strip()  # Lấy tên cầu thủ từ thẻ <th>
                # Bỏ qua các cầu thủ có tên "Squad Total" hoặc "Opponent Total"
                if player_name in ['Squad Total', 'Opponent Total']:
                    continue
                live = cols[5].text.strip()
                dead = cols[6].text.strip()
                fk = cols[7].text.strip()
                tb = cols[8].text.strip()
                sw = cols[9].text.strip()
                crs = cols[10].text.strip()
                ti = cols[11].text.strip()
                ck = cols[12].text.strip()
                ptin = cols[13].text.strip()
                ptout = cols[14].text.strip()
                ptstr = cols[15].text.strip()
                cmp = cols[16].text.strip()
                off = cols[17].text.strip()
                blocks = cols[18].text.strip()
                player_data.append([player_name, live, dead, fk, tb, sw, crs, ti, ck, ptin, ptout, ptstr, cmp, off,
                                    blocks])
    return player_data


def scrape_gca_data(url):
    r = requests.get(url)
    soup = bs(r.content, 'html.parser')
    player_data = []
    table = soup.find('table', attrs={'id': 'stats_gca_9'})
    if table:
        rows = table.find_all('tr')
        for row in rows[1:]:  # Bỏ qua hàng tiêu đề
            cols = row.find_all('td')
            if len(cols) > 0:  # Bỏ qua các hàng trống
                player_name = row.find('th').text.strip()  # Lấy tên cầu thủ từ thẻ <th>
                # Bỏ qua các cầu thủ có tên "Squad Total" hoặc "Opponent Total"
                if player_name in ['Squad Total', 'Opponent Total']:
                    continue
                sca = cols[4].text.strip()
                sca90 = cols[5].text.strip()
                passlive = cols[6].text.strip()
                passdead = cols[7].text.strip()
                to = cols[8].text.strip()
                sh = cols[9].text.strip()
                fld = cols[10].text.strip()
                stdef = cols[11].text.strip()
                gca = cols[12].text.strip()
                gca90 = cols[13].text.strip()
                gtpasslive = cols[14].text.strip()
                gtpassdead = cols[15].text.strip()
                gtto = cols[16].text.strip()
                gtsh = cols[17].text.strip()
                gtfld = cols[18].text.strip()
                gtdef = cols[19].text.strip()
                player_data.append([player_name, sca, sca90, passlive, passdead, to, sh, fld,
                                   stdef, gca, gca90, gtpasslive, gtpassdead, gtto, gtsh, gtfld, gtdef])
    return player_data


def scrape_defense_data(url):
    r = requests.get(url)
    soup = bs(r.content, 'html.parser')
    player_data = []
    table = soup.find('table', attrs={'id': 'stats_defense_9'})
    if table:
        rows = table.find_all('tr')
        for row in rows[1:]:  # Bỏ qua hàng tiêu đề
            cols = row.find_all('td')
            if len(cols) > 0:  # Bỏ qua các hàng trống
                player_name = row.find('th').text.strip()  # Lấy tên cầu thủ từ thẻ <th>
                # Bỏ qua các cầu thủ có tên "Squad Total" hoặc "Opponent Total"
                if player_name in ['Squad Total', 'Opponent Total']:
                    continue
                tkl = cols[4].text.strip()
                tklw = cols[5].text.strip()
                def3rd = cols[6].text.strip()
                mid3rd = cols[7].text.strip()
                att3rd = cols[8].text.strip()
                tklch = cols[9].text.strip()
                att = cols[10].text.strip()
                tkl5 = cols[11].text.strip()
                lost = cols[12].text.strip()
                blocks = cols[13].text.strip()
                sh = cols[14].text.strip()
                passbl = cols[15].text.strip()
                int = cols[16].text.strip()
                tklint = cols[17].text.strip()
                clr = cols[18].text.strip()
                err = cols[19].text.strip()
                player_data.append([player_name, tkl, tklw, def3rd, mid3rd, att3rd, tklch, att,
                                   tkl5, lost, blocks, sh, passbl, int, tklint, clr, err])
    return player_data


def scrape_possession_data(url):
    r = requests.get(url)
    soup = bs(r.content, 'html.parser')
    player_data = []
    table = soup.find('table', attrs={'id': 'stats_possession_9'})
    if table:
        rows = table.find_all('tr')
        for row in rows[1:]:  # Bỏ qua hàng tiêu đề
            cols = row.find_all('td')
            if len(cols) > 0:  # Bỏ qua các hàng trống
                player_name = row.find('th').text.strip()  # Lấy tên cầu thủ từ thẻ <th>
                # Bỏ qua các cầu thủ có tên "Squad Total" hoặc "Opponent Total"
                if player_name in ['Squad Total', 'Opponent Total']:
                    continue
                touches = cols[4].text.strip()
                defpen = cols[5].text.strip()
                def3rd = cols[6].text.strip()
                mid3rd = cols[7].text.strip()
                att3rd = cols[8].text.strip()
                attpen = cols[9].text.strip()
                live = cols[10].text.strip()
                att = cols[11].text.strip()
                succ = cols[12].text.strip()
                succ5 = cols[13].text.strip()
                tkld = cols[14].text.strip()
                tkld5 = cols[15].text.strip()
                carries = cols[16].text.strip()
                totdist = cols[17].text.strip()
                prgdist = cols[18].text.strip()
                prgcs = cols[19].text.strip()
                c13 = cols[20].text.strip()
                cpa = cols[21].text.strip()
                mis = cols[22].text.strip()
                dis = cols[23].text.strip()
                rec = cols[24].text.strip()
                prgr = cols[25].text.strip()
                player_data.append([player_name, touches, defpen, def3rd, mid3rd, att3rd, attpen, live,
                                   att, succ, succ5, tkld, tkld5, carries, totdist, prgdist, prgcs, c13,
                                    cpa, mis, dis, rec, prgr])
    return player_data


def scrape_playingtime_data(url):
    r = requests.get(url)
    soup = bs(r.content, 'html.parser')
    player_data = []
    table = soup.find('table', attrs={'id': 'stats_playing_time_9'})
    if table:
        rows = table.find_all('tr')
        for row in rows[1:]:  # Bỏ qua hàng tiêu đề
            cols = row.find_all('td')
            if len(cols) > 0:  # Bỏ qua các hàng trống
                player_name = row.find('th').text.strip()  # Lấy tên cầu thủ từ thẻ <th>
                # Bỏ qua các cầu thủ có tên "Squad Total" hoặc "Opponent Total"
                if player_name in ['Squad Total', 'Opponent Total']:
                    continue
                starts = cols[8].text.strip()
                mnstart = cols[9].text.strip()
                compl = cols[10].text.strip()
                subs = cols[11].text.strip()
                mnsub = cols[12].text.strip()
                unsub = cols[13].text.strip()
                ppm = cols[14].text.strip()
                ong = cols[15].text.strip()
                onga = cols[16].text.strip()
                onxg = cols[20].text.strip()
                onxga = cols[21].text.strip()
                player_data.append([player_name, starts, mnstart, compl, subs, mnsub, unsub, ppm,
                                   ong, onga, onxg, onxga])
    return player_data


def scrape_ms_data(url):
    r = requests.get(url)
    soup = bs(r.content, 'html.parser')
    player_data = []
    table = soup.find('table', attrs={'id': 'stats_misc_9'})
    if table:
        rows = table.find_all('tr')
        for row in rows[1:]:  # Bỏ qua hàng tiêu đề
            cols = row.find_all('td')
            if len(cols) > 0:  # Bỏ qua các hàng trống
                player_name = row.find('th').text.strip()  # Lấy tên cầu thủ từ thẻ <th>
                # Bỏ qua các cầu thủ có tên "Squad Total" hoặc "Opponent Total"
                if player_name in ['Squad Total', 'Opponent Total']:
                    continue
                fls = cols[7].text.strip()
                fld = cols[8].text.strip()
                off = cols[9].text.strip()
                crs = cols[10].text.strip()
                og = cols[15].text.strip()
                recov = cols[16].text.strip()
                won = cols[17].text.strip()
                lost = cols[18].text.strip()
                won5 = cols[19].text.strip()
                player_data.append([player_name, fls, fld, off, crs, og, recov, won,
                                   lost, won5])
    return player_data


# Kiểm tra xem file CSV có tồn tại không
file_exists = os.path.isfile('result.csv')

# Tạo tiêu đề cột với MultiIndex chỉ một lần
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


for url in urls:
    player_list = scrape_player_data(url)
    time.sleep(5)
    keeper_list = scrape_keeper_data(url)
    time.sleep(5)
    shooting_list = scrape_shooting_data(url)
    time.sleep(5)
    passing_list = scrape_passing_data(url)
    time.sleep(5)
    passtypes_list = scrape_passtypes_data(url)
    time.sleep(5)

    gca_list = scrape_gca_data(url)
    time.sleep(5)

    defense_list = scrape_defense_data(url)
    time.sleep(5)
    possession_list = scrape_possession_data(url)
    time.sleep(5)

    playingtime_list = scrape_playingtime_data(url)
    time.sleep(5)
    ms_list = scrape_ms_data(url)
    time.sleep(5)

    time.sleep(5)  # Nghỉ 3 giây giữa các URL
# Tạo DataFrame từ danh sách cầu thủ và thủ môn
    df_players = pd.DataFrame(player_list,
                              columns=['Player', 'Nation', 'Team', 'Pos', 'Age', 'MP', 'Starts', 'Min', '90s',
                                       'G-PK', 'PKatt', 'CrdY', 'CrdR', 'xG', 'npxG', 'xAG', 'PrgC', 'PrgP', 'PrgR',
                                       'Gls', 'Ast', 'G+A', 'G-PK', 'G+A-PK', 'xG', 'xAG', 'xG+xAG', 'npxG'])
    df_keepers = pd.DataFrame(keeper_list,
                              columns=['Player', 'GA', 'GA90', 'SoTA', 'Save', 'Save%', 'W', 'D', 'L', 'CS', 'CS%',
                                       'PKatt', 'PKA', 'PKsv', 'PKm', 'Save%'])
    df_shooting = pd.DataFrame(shooting_list,
                               columns=['Player', 'Gls', 'Sh', 'SoT', 'SoT5', 'Sh/90', 'SoT/90', 'G/Sh',
                                        'G/SoT', 'Dist', 'FK', 'PK', 'PKatt', 'xG', 'npxG', 'npxG/Sh', 'G-xG',
                                        'np:G-xG'])
    df_passing = pd.DataFrame(passing_list,
                              columns=['Player', 'Cmp', 'Att', 'Cmp%', 'TotDist', 'PrgDist', 'Cmp', 'Att', 'Cmp%',
                                       'Cmp', 'Att', 'Cmp%', 'Cmp', 'Att', 'Cmp%', 'Ast', 'xAG', 'xA', 'A-xAG', 'KP',
                                       '1/3', 'PPA', 'CrsPA', 'PrgP'])
    df_passtypes = pd.DataFrame(passtypes_list,
                                columns=['Player', 'Live', 'Dead', 'FK', 'TB', 'Sw', 'Crs', 'TI', 'CK', 'In', 'Out',
                                         'Str','Cmp', 'Off', 'Blocks'])
    df_gca = pd.DataFrame(gca_list,
                          columns=['Player', 'SCA', 'SCA90', 'PassLive', 'PassDead', 'TO', 'Sh',
                                   'Fld', 'Def', 'GCA', 'GCA90', 'PassLive', 'PassDead', 'TO', 'Sh',
                                   'Fld', 'Def'])
    df_defense = pd.DataFrame(defense_list,
                              columns=['Player', 'Tkl', 'TklW', 'Def 3rd', 'Mid 3rd', 'Att 3rd', 'Tkl',
                                       'Att', 'Tkl%', 'Lost', 'Blocks', 'Sh', 'Pass', 'Int', 'Tkl+Int',
                                       'Clr', 'Err'])
    df_possession = pd.DataFrame(possession_list,
                                 columns=['Player', 'Touches', 'Def Pen', 'Def 3rd', 'Mid 3rd', 'Att 3rd', 'Att Pen',
                                          'Live', 'Att', 'Succ', 'Succ%', 'Tkld', 'Tkld%', 'Carries', 'TotDist',
                                          'PrgDist', 'PrgC', '1/3', 'CPA', 'Mis', 'Dis', 'Rec', 'PrgR'])
    df_playingtime = pd.DataFrame(playingtime_list,
                                  columns=['Player', 'Starts', 'Mn/Start', 'Compl', 'Subs', 'Mn/Sub', 'unSub',
                                           'PPM', 'onG', 'onGA', 'onxG', 'onxGA'])
    df_ms = pd.DataFrame(ms_list,
                         columns=['Player', 'Fls', 'Fld', 'Off', 'Crs', 'OG', 'Recov',
                                  'Won', 'Lost', 'Won%'])

    # Ghép hai bảng lại dựa trên cột 'Player'
    df_merged = pd.merge(df_players, df_keepers, on='Player', how='left')
    df_merged = pd.merge(df_merged, df_shooting, on='Player', how='left')
    df_merged = pd.merge(df_merged, df_passing, on='Player', how='left')
    df_merged = pd.merge(df_merged, df_passtypes, on='Player', how='left')
    df_merged = pd.merge(df_merged, df_gca, on='Player', how='left')
    df_merged = pd.merge(df_merged, df_defense, on='Player', how='left')
    df_merged = pd.merge(df_merged, df_possession, on='Player', how='left')
    df_merged = pd.merge(df_merged, df_playingtime, on='Player', how='left')
    df_merged = pd.merge(df_merged, df_ms, on='Player', how='left')
    df_merged.fillna('N/A', inplace=True)
    df_merged.columns = column_titles
    df_merged.to_csv('results.csv', mode='a', header=not file_exists, index=False)
    file_exists = True  # Đặt thành True sau khi ghi lần đầu tiên
    time.sleep(2)
# Lưu vào file CSV
print("Dữ liệu đã được ghi vào file 'results.csv'.")
