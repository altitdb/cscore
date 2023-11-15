import pandas as pd
import os
import numpy as np
import matplotlib.pyplot as plt
from datetime import datetime, timedelta

desired_width=4080
pd.set_option('display.width', desired_width)
np.set_printoptions(linewidth=desired_width)
pd.set_option('display.max_columns', 100)
pd.set_option('display.max_rows', None)
pd.options.display.float_format = '{:,.2f}'.format

STAKE = 50

dfs = []
for root, dirs, files in os.walk(r'./datafiles'):
    for name in sorted(files):
        if name.startswith('cscore.com.br-'):
            filename = f'./datafiles/{name}'
            print(f'Reading file {filename}')
            df = pd.read_csv(filename)
            dfs.append(df)

df = pd.concat(dfs, ignore_index=True)

print('Removendo jogos sem resultados concluídos')
df = df.dropna()
df = df.astype({'ScoreHome': int, 'ScoreAway': int})

df['Scoreboard'] = df['ScoreHome'].astype(str) + 'x' + df['ScoreAway'].astype(str)
df.loc[((df['ScoreHome'] > 3) & (df['ScoreHome'] > df['ScoreAway'])), 'Scoreboard'] = 'AOHW'
df.loc[((df['ScoreAway'] > 3) & (df['ScoreAway'] > df['ScoreHome'])), 'Scoreboard'] = 'AOAW'
df.loc[((df['ScoreHome'] > 3) & (df['ScoreAway'] > 3) & (df['ScoreHome'] == df['ScoreAway'])), 'Scoreboard'] = 'AOD'


def calculate_position_win(row):
    results = []
    results.append({'name': '0x0', 'value': row['0x0']})
    results.append({'name': '0x1', 'value': row['0x1']})
    results.append({'name': '0x2', 'value': row['0x2']})
    results.append({'name': '0x3', 'value': row['0x3']})
    results.append({'name': '1x0', 'value': row['1x0']})
    results.append({'name': '1x1', 'value': row['1x1']})
    results.append({'name': '1x2', 'value': row['1x2']})
    results.append({'name': '1x3', 'value': row['1x3']})
    results.append({'name': '2x0', 'value': row['2x0']})
    results.append({'name': '2x1', 'value': row['2x1']})
    results.append({'name': '2x2', 'value': row['2x2']})
    results.append({'name': '2x3', 'value': row['2x3']})
    results.append({'name': '3x0', 'value': row['3x0']})
    results.append({'name': '3x1', 'value': row['3x1']})
    results.append({'name': '3x2', 'value': row['3x2']})
    results.append({'name': '3x3', 'value': row['3x3']})
    results.append({'name': 'AOAW', 'value': row['AOAW']})
    results.append({'name': 'AOD', 'value': row['AOD']})
    results.append({'name': 'AOHW', 'value': row['AOHW']})
    sorted_results = sorted(results, key=lambda x: x['value'], reverse=True)

    for index, result in enumerate(sorted_results):
        if row['Scoreboard'] == result['name']:
            return index + 1
    raise Exception(row)


def calculate_probability_position(limit, row):
    results = []
    results.append({'name': '0x0', 'value': row['0x0']})
    results.append({'name': '0x1', 'value': row['0x1']})
    results.append({'name': '0x2', 'value': row['0x2']})
    results.append({'name': '0x3', 'value': row['0x3']})
    results.append({'name': '1x0', 'value': row['1x0']})
    results.append({'name': '1x1', 'value': row['1x1']})
    results.append({'name': '1x2', 'value': row['1x2']})
    results.append({'name': '1x3', 'value': row['1x3']})
    results.append({'name': '2x0', 'value': row['2x0']})
    results.append({'name': '2x1', 'value': row['2x1']})
    results.append({'name': '2x2', 'value': row['2x2']})
    results.append({'name': '2x3', 'value': row['2x3']})
    results.append({'name': '3x0', 'value': row['3x0']})
    results.append({'name': '3x1', 'value': row['3x1']})
    results.append({'name': '3x2', 'value': row['3x2']})
    results.append({'name': '3x3', 'value': row['3x3']})
    results.append({'name': 'AOAW', 'value': row['AOAW']})
    results.append({'name': 'AOD', 'value': row['AOD']})
    results.append({'name': 'AOHW', 'value': row['AOHW']})
    sorted_results = sorted(results, key=lambda x: x['value'], reverse=True)

    probability_total = 0
    for index, result in enumerate(sorted_results):
        probability_total += result['value']
        if (index + 1) == limit:
            return round(probability_total, 0)
    raise Exception(row)


def calculate_probability_gte80(limit, row):
    if row[f'Probability_{limit}'] >= 80:
        return 1
    return 0


def calculate_position_win_by_limit(row, limit):
    if row['Position_Win'] <= limit:
        return 1
    elif row['Position_Win'] > limit:
        return 0
    raise Exception(row)


def calculate_profit(row, position, gain_percent):
    if row[f'Position_{position}_win'] == 0:
        return STAKE * row['Total'] * -1
    return STAKE * row['Total'] * gain_percent


def calculate_position_probability_gte(row):
    results = []
    results.append({'name': '0x0', 'value': row['0x0']})
    results.append({'name': '0x1', 'value': row['0x1']})
    results.append({'name': '0x2', 'value': row['0x2']})
    results.append({'name': '0x3', 'value': row['0x3']})
    results.append({'name': '1x0', 'value': row['1x0']})
    results.append({'name': '1x1', 'value': row['1x1']})
    results.append({'name': '1x2', 'value': row['1x2']})
    results.append({'name': '1x3', 'value': row['1x3']})
    results.append({'name': '2x0', 'value': row['2x0']})
    results.append({'name': '2x1', 'value': row['2x1']})
    results.append({'name': '2x2', 'value': row['2x2']})
    results.append({'name': '2x3', 'value': row['2x3']})
    results.append({'name': '3x0', 'value': row['3x0']})
    results.append({'name': '3x1', 'value': row['3x1']})
    results.append({'name': '3x2', 'value': row['3x2']})
    results.append({'name': '3x3', 'value': row['3x3']})
    results.append({'name': 'AOAW', 'value': row['AOAW']})
    results.append({'name': 'AOD', 'value': row['AOD']})
    results.append({'name': 'AOHW', 'value': row['AOHW']})
    sorted_results = sorted(results, key=lambda x: x['value'], reverse=True)

    probability_total = 0
    for index, result in enumerate(sorted_results):
        probability_total += result['value']
        if probability_total >= 80:
            return index + 1
    raise Exception(row)


def calculate_position_probability_gte_win(row):
    if row['Position_Win'] <= row['Position_Probability_gte80']:
        return 1
    return 0


df['Position_Win'] = df.apply(lambda row: calculate_position_win(row), axis=1)
df['Position_Probability_gte80'] = df.apply(lambda row: calculate_position_probability_gte(row), axis=1)
df['Position_Probability_gte80_Win'] = df.apply(lambda row: calculate_position_probability_gte_win(row), axis=1)

df['Probability_5'] = df.apply(lambda row: calculate_probability_position(5, row), axis=1)
df['Probability_6'] = df.apply(lambda row: calculate_probability_position(6, row), axis=1)
df['Probability_7'] = df.apply(lambda row: calculate_probability_position(7, row), axis=1)
df['Probability_8'] = df.apply(lambda row: calculate_probability_position(8, row), axis=1)

df['Probability_5_gte80'] = df.apply(lambda row: calculate_probability_gte80(5, row), axis=1)
df['Probability_6_gte80'] = df.apply(lambda row: calculate_probability_gte80(6, row), axis=1)
df['Probability_7_gte80'] = df.apply(lambda row: calculate_probability_gte80(7, row), axis=1)
df['Probability_8_gte80'] = df.apply(lambda row: calculate_probability_gte80(8, row), axis=1)

df['Position_5_win'] = df.apply(lambda row: calculate_position_win_by_limit(row, 5), axis=1)
df['Position_6_win'] = df.apply(lambda row: calculate_position_win_by_limit(row, 6), axis=1)
df['Position_7_win'] = df.apply(lambda row: calculate_position_win_by_limit(row, 7), axis=1)
df['Position_8_win'] = df.apply(lambda row: calculate_position_win_by_limit(row, 8), axis=1)

print(f'Saving {len(df)} results')
df.to_csv('./datafiles/cscore.com.br.csv', index=False)

start_date = datetime(2023, 10, 1)
today = datetime.today()
difference_days = today - start_date
dates = []
for single_date in (start_date + timedelta(days=n) for n in range(difference_days.days + 1)):
    dates.append({
        'Date': single_date.strftime('%Y-%m-%d')
    })
df_x = pd.DataFrame(dates)
print(df_x)

win = []
available_results = range(5, 9)
for x in available_results:
    probability_total_win = df[(df[f'Probability_{x}_gte80'] == 1) & (df[f'Position_{x}_win'] == 1)].count()[f"Position_{x}_win"]
    probability_total_loss = df[(df[f'Probability_{x}_gte80'] == 1) & (df[f'Position_{x}_win'] == 0)].count()[f"Position_{x}_win"]
    win.append([probability_total_win, probability_total_loss])
df_summary = pd.DataFrame(win, index=available_results, columns=['Win', 'Loss'])
df_summary['Percent'] = df_summary['Loss'] / df_summary['Win']
df_summary['Min_Profit'] = df_summary['Percent'] * 1.065
print(df_summary)

for index, summary in df_summary.iterrows():
    df_analytics = df.copy()
    df_analytics.drop(['Hour', 'Country', 'League', 'Home', 'Away', 'ScoreHome', 'ScoreAway',
                       '0x0', '0x1', '0x2', '0x3', '1x0', '1x1', '1x2', '1x3', '2x0', '2x1', '2x2',
                       '2x3', '3x0', '3x1', '3x2', '3x3', 'AOAW', 'AOD', 'AOHW', 'Scoreboard',
                       'Score', 'Position_Win', 'Probability_5', 'Probability_6',
                       'Probability_7', 'Probability_8'],
                      inplace=True, axis=1)
    df_analytics['Total'] = 0
    flt = df_analytics[f'Probability_{index}_gte80'] == 1
    group_by = ['Date', f'Probability_{index}_gte80', f'Position_{index}_win']
    df_analytics = df_analytics[flt].groupby(group_by, as_index=False)['Total'].count()
    gain_percent = summary['Min_Profit']
    df_analytics['Profit'] = df_analytics.apply(lambda row: calculate_profit(row, index, gain_percent), axis=1)
    df_analytics['Accumulate'] = df_analytics['Profit'].cumsum()
    df_analytics['Max'] = df_analytics['Accumulate'].max()
    df_analytics['Min'] = df_analytics['Accumulate'].min()

    print(f'# Resultados analiticos - Probabilidade com {index} placares')
    print(df_analytics)

    df_analytics.plot(x='Date', y='Accumulate', style='-o')
    plt.title(f'Probabilidade com {index} placares')
    plt.axhline(0, color='b')
    plt.savefig(f'graphs/probability-until-80-with-{index}-scores.png')

win = []
for x in available_results:
    probability_total_win = df[(df[f'Position_{x}_win'] == 1)].count()[f"Position_{x}_win"]
    probability_total_loss = df[(df[f'Position_{x}_win'] == 0)].count()[f"Position_{x}_win"]
    win.append([probability_total_win, probability_total_loss])
df_summary = pd.DataFrame(win, index=available_results, columns=['Win', 'Loss'])
df_summary['Percent'] = df_summary['Loss'] / df_summary['Win']
df_summary['Min_Profit'] = df_summary['Percent'] * 1.065
print(df_summary)

for index, summary in df_summary.iterrows():
    df_analytics = df.copy()
    df_analytics.drop(['Hour', 'Country', 'League', 'Home', 'Away', 'ScoreHome', 'ScoreAway',
                       '0x0', '0x1', '0x2', '0x3', '1x0', '1x1', '1x2', '1x3', '2x0', '2x1', '2x2',
                       '2x3', '3x0', '3x1', '3x2', '3x3', 'AOAW', 'AOD', 'AOHW', 'Scoreboard',
                       'Score', 'Position_Win', 'Probability_5', 'Probability_6',
                       'Probability_7', 'Probability_8'],
                      inplace=True, axis=1)
    df_analytics['Total'] = 0
    group_by = ['Date', f'Position_{index}_win']
    df_analytics = df_analytics.groupby(group_by, as_index=False)['Total'].count()
    gain_percent = summary['Min_Profit']
    df_analytics['Profit'] = df_analytics.apply(lambda row: calculate_profit(row, index, gain_percent), axis=1)
    df_analytics['Accumulate'] = df_analytics['Profit'].cumsum()
    df_analytics['Max'] = df_analytics['Accumulate'].max()
    df_analytics['Min'] = df_analytics['Accumulate'].min()

    print(f'# Resultados analiticos - Probabilidade com {index} placares')
    print(df_analytics)

    df_analytics.plot(x='Date', y='Accumulate', style='-o')
    plt.title(f'Probabilidade com {index} placares')
    plt.axhline(0, color='b')
    plt.savefig(f'graphs/probability-with-{index}-scores.png')

print('Analysis by League')
win = []
for x in available_results:
    probability_total_win = df[(df[f'Position_{x}_win'] == 1)].count()[f"Position_{x}_win"]
    probability_total_loss = df[(df[f'Position_{x}_win'] == 0)].count()[f"Position_{x}_win"]
    win.append([probability_total_win, probability_total_loss])
df_summary = pd.DataFrame(win, index=available_results, columns=['Win', 'Loss'])
df_summary['Percent'] = df_summary['Loss'] / df_summary['Win']
df_summary['Min_Profit'] = df_summary['Percent'] * 1.065
print(df_summary)

for index, summary in df_summary.iterrows():
    df_analytics = df.copy()
    df_dates = df_x.copy()
    df_analytics.drop(['Hour', 'Country', 'Home', 'Away', 'ScoreHome', 'ScoreAway',
                       '0x0', '0x1', '0x2', '0x3', '1x0', '1x1', '1x2', '1x3', '2x0', '2x1', '2x2',
                       '2x3', '3x0', '3x1', '3x2', '3x3', 'AOAW', 'AOD', 'AOHW', 'Scoreboard',
                       'Score', 'Position_Win', 'Probability_5', 'Probability_6',
                       'Probability_7', 'Probability_8'],
                      inplace=True, axis=1)

    leagues = df_analytics['League'].unique()
    df_analytics['Total'] = 0
    legend = []

    plt.clf()
    plt.figure(figsize=(60, 15))

    for league in leagues:
        group_by = ['Date']
        df_analytics_league = df_analytics[df_analytics['League'] == league]
        df_analytics_league.loc[(df_analytics_league[f'Position_{index}_win'] == 0), 'Profit'] = STAKE * -1
        df_analytics_league.loc[(df_analytics_league[f'Position_{index}_win'] == 1), 'Profit'] = STAKE * summary['Min_Profit']
        df_analytics_league = df_analytics_league.groupby(group_by, as_index=False)['Profit'].sum()
        df_dates['Profit'] = 0
        dates_without_duplicates = pd.concat([df_analytics_league, df_dates], ignore_index=True)['Date'].drop_duplicates(keep=False)
        df_dates = df_dates[(df_dates['Date'].isin(dates_without_duplicates))]
        df_analytics_league = pd.concat([df_analytics_league, df_dates], ignore_index=True)
        df_analytics_league.sort_values(by='Date', inplace=True)
        df_analytics_league.reset_index(drop=True, inplace=True)
        df_analytics_league['Accumulate'] = df_analytics_league['Profit'].cumsum()

        last_value = df_analytics_league['Accumulate'].iloc[-1]
        if last_value > 0:
            legend.append(league)
            plt.plot(df_analytics_league['Date'], df_analytics_league['Accumulate'], label=league)

    plt.legend(legend)
    plt.title(f'Probabilidade com {index} placares')
    plt.axhline(0, color='b')
    plt.savefig(f'graphs/probability-league-with-{index}-scores.png')
