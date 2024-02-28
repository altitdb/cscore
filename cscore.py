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
            filename = f'{root}/{name}'
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


def format_hour(value):
    values = value.split(':')
    if len(values) == 2:
        return value
    return f'{values[0]}:{values[1]}'


df['Hour'] = df['Hour'].apply(lambda value: format_hour(value))


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


def calculate_score_order(limit, row):
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
        if probability_total >= 80 or index == 18:
            return index + 1
    raise Exception(row)


def calculate_position_probability_gte_win(row):
    if row['Position_Win'] <= row['Position_Probability_gte80']:
        return 1
    return 0


def calculate_position_order(row, position):
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
    return sorted_results[position - 1]['name']


def calculate_score_position(row, score):
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
    for index, value in enumerate(sorted_results):
        if value['name'] == score:
            return index + 1


df['Position_Win'] = df.apply(lambda row: calculate_position_win(row), axis=1)
df['Position_Probability_gte80'] = df.apply(lambda row: calculate_position_probability_gte(row), axis=1)
df['Position_Probability_gte80_Win'] = df.apply(lambda row: calculate_position_probability_gte_win(row), axis=1)

df['Probability_5'] = df.apply(lambda row: calculate_score_order(5, row), axis=1)
df['Probability_6'] = df.apply(lambda row: calculate_score_order(6, row), axis=1)
df['Probability_7'] = df.apply(lambda row: calculate_score_order(7, row), axis=1)
df['Probability_8'] = df.apply(lambda row: calculate_score_order(8, row), axis=1)

df['Probability_5_gte80'] = df.apply(lambda row: calculate_probability_gte80(5, row), axis=1)
df['Probability_6_gte80'] = df.apply(lambda row: calculate_probability_gte80(6, row), axis=1)
df['Probability_7_gte80'] = df.apply(lambda row: calculate_probability_gte80(7, row), axis=1)
df['Probability_8_gte80'] = df.apply(lambda row: calculate_probability_gte80(8, row), axis=1)

df['Position_5_win'] = df.apply(lambda row: calculate_position_win_by_limit(row, 5), axis=1)
df['Position_6_win'] = df.apply(lambda row: calculate_position_win_by_limit(row, 6), axis=1)
df['Position_7_win'] = df.apply(lambda row: calculate_position_win_by_limit(row, 7), axis=1)
df['Position_8_win'] = df.apply(lambda row: calculate_position_win_by_limit(row, 8), axis=1)

scores = ['0x0', '0x1', '0x2', '0x3', '1x0', '1x1', '1x2', '1x3', '2x0', '2x1', '2x2',
                       '2x3', '3x0', '3x1', '3x2', '3x3', 'AOAW', 'AOD', 'AOHW']

for score in scores:
    df[f'Position_Score_{score}'] = df.apply(lambda row: calculate_score_position(row, score), axis=1)

df['Score_Order_1'] = df.apply(lambda row: calculate_position_order(row, 1), axis=1)
df['Score_Order_2'] = df.apply(lambda row: calculate_position_order(row, 2), axis=1)
df['Score_Order_3'] = df.apply(lambda row: calculate_position_order(row, 3), axis=1)
df['Score_Order_4'] = df.apply(lambda row: calculate_position_order(row, 4), axis=1)
df['Score_Order_5'] = df.apply(lambda row: calculate_position_order(row, 5), axis=1)
df['Score_Order_6'] = df.apply(lambda row: calculate_position_order(row, 6), axis=1)
df['Score_Order_7'] = df.apply(lambda row: calculate_position_order(row, 7), axis=1)
df['Score_Order_8'] = df.apply(lambda row: calculate_position_order(row, 8), axis=1)
df['Score_Order_9'] = df.apply(lambda row: calculate_position_order(row, 9), axis=1)
df['Score_Order_10'] = df.apply(lambda row: calculate_position_order(row, 10), axis=1)
df['Score_Order_11'] = df.apply(lambda row: calculate_position_order(row, 11), axis=1)
df['Score_Order_12'] = df.apply(lambda row: calculate_position_order(row, 12), axis=1)
df['Score_Order_13'] = df.apply(lambda row: calculate_position_order(row, 13), axis=1)
df['Score_Order_14'] = df.apply(lambda row: calculate_position_order(row, 14), axis=1)
df['Score_Order_15'] = df.apply(lambda row: calculate_position_order(row, 15), axis=1)
df['Score_Order_16'] = df.apply(lambda row: calculate_position_order(row, 16), axis=1)
df['Score_Order_17'] = df.apply(lambda row: calculate_position_order(row, 17), axis=1)
df['Score_Order_18'] = df.apply(lambda row: calculate_position_order(row, 18), axis=1)
df['Score_Order_19'] = df.apply(lambda row: calculate_position_order(row, 19), axis=1)

df_backtest = df.copy()
df_backtest = df_backtest[df_backtest['Score_Order_1'] == 'AOHW']
print(f'Total: {len(df_backtest)}')
print(f"Total first: {len(df_backtest[df_backtest['Position_Win'] == 1])}")
print(f"Total <= 5: {len(df_backtest[df_backtest['Position_Win'] <= 5])}")
print(f"Total <= 6: {len(df_backtest[df_backtest['Position_Win'] <= 6])}")
print(f"Total <= 7: {len(df_backtest[df_backtest['Position_Win'] <= 7])}")
print(f"Total <= 8: {len(df_backtest[df_backtest['Position_Win'] <= 8])}")

print(f'Saving {len(df)} results')
df.sort_values(by=['Date', 'Hour'], inplace=True)
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

data_inicial = '2024-01-01'
data_final = '2024-01-31'
for index, summary in df_summary.iterrows():
    df_analytics = df.copy()
    df_analytics = df_analytics[(df_analytics['Date'] >= data_inicial) & (df_analytics['Date'] <= data_final)]
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
    plt.title(f'Probabilidade com {index} placares - De {data_inicial} até {data_final}')
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
    df_analytics = df_analytics[(df_analytics['Date'] >= data_inicial) & (df_analytics['Date'] <= data_final)]
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
    plt.title(f'Probabilidade com {index} placares - De {data_inicial} até {data_final}')
    plt.axhline(0, color='b')
    plt.savefig(f'graphs/probability-with-{index}-scores.png')


print('Analysis by League')


def summary_by_league(index, league):
    win = []
    probability_total_win = df[(df[f'League'] == league) & (df[f'Position_{index}_win'] == 1)].count()[
        f"Position_{index}_win"]
    probability_total_loss = df[(df[f'League'] == league) & (df[f'Position_{index}_win'] == 0)].count()[
        f"Position_{index}_win"]
    win.append([probability_total_win, probability_total_loss])
    df_summary = pd.DataFrame(win, index=[index], columns=['Win', 'Loss'])
    df_summary['Percent'] = df_summary['Loss'] / df_summary['Win']
    df_summary['Min_Profit'] = df_summary['Percent'] * 1.065
    print(df_summary)
    return df_summary


for index in available_results:
    df_analytics = df.copy()
    df_dates = df_x.copy()
    df_analytics.drop(['Hour', 'Home', 'Away', 'ScoreHome', 'ScoreAway',
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
        # summary = summary_by_league(index, league)
        group_by = ['Date']
        df_country = df_analytics[df_analytics['League'] == league]
        countries = df_country['Country'].unique()

        for country in countries:
            df_analytics_league = df_analytics[(df_analytics['League'] == league) & (df_analytics['Country'] == country)]
            df_analytics_league.loc[(df_analytics_league[f'Position_{index}_win'] == 0), 'Profit'] = STAKE * -1
            df_analytics_league.loc[(df_analytics_league[f'Position_{index}_win'] == 1), 'Profit'] = STAKE * 0.38
            df_analytics_league = df_analytics_league.groupby(group_by, as_index=False)['Profit'].sum()
            df_dates = df_x.copy()
            df_dates['Profit'] = 0
            dates_without_duplicates = pd.concat([df_analytics_league, df_dates], ignore_index=True)['Date'].drop_duplicates(keep=False)
            df_dates = df_dates[(df_dates['Date'].isin(dates_without_duplicates))]
            df_analytics_league = pd.concat([df_analytics_league, df_dates], ignore_index=True)
            df_analytics_league.sort_values(by='Date', inplace=True)
            df_analytics_league.reset_index(drop=True, inplace=True)
            df_analytics_league['Accumulate'] = df_analytics_league['Profit'].cumsum()

            last_value = df_analytics_league['Accumulate'].iloc[-1]
            if last_value > -50:
                legend.append(f'{league} - {country}')
                plt.plot(df_analytics_league['Date'], df_analytics_league['Accumulate'], label=league)

    plt.legend(legend)
    plt.title(f'Probabilidade com {index} placares')
    plt.axhline(0, color='b')
    plt.savefig(f'graphs/probability-league-with-{index}-scores.png')
