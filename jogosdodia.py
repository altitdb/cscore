import pandas as pd
import os
import numpy as np
import matplotlib.pyplot as plt
from datetime import datetime

desired_width=4080
pd.set_option('display.width', desired_width)
np.set_printoptions(linewidth=desired_width)
pd.set_option('display.max_columns', 100)
pd.set_option('display.max_rows', None)
pd.options.display.float_format = '{:,.2f}'.format

date = datetime.now().strftime('%Y%m%d')
date = '20231105'
filename = f'./datafiles/cscore.com.br-{date}.csv'
print(f'Reading file {filename}')
df = pd.read_csv(filename)
home = None # 'Farul Constanta'


def calculate_ev(limit, row):
    results = []
    results.append({'name': '0x0', 'value': row['0x0'], 'ev': row['ev_0x0']})
    results.append({'name': '0x1', 'value': row['0x1'], 'ev': row['ev_0x1']})
    results.append({'name': '0x2', 'value': row['0x2'], 'ev': row['ev_0x2']})
    results.append({'name': '0x3', 'value': row['0x3'], 'ev': row['ev_0x3']})
    results.append({'name': '1x0', 'value': row['1x0'], 'ev': row['ev_1x0']})
    results.append({'name': '1x1', 'value': row['1x1'], 'ev': row['ev_1x1']})
    results.append({'name': '1x2', 'value': row['1x2'], 'ev': row['ev_1x2']})
    results.append({'name': '1x3', 'value': row['1x3'], 'ev': row['ev_1x3']})
    results.append({'name': '2x0', 'value': row['2x0'], 'ev': row['ev_2x0']})
    results.append({'name': '2x1', 'value': row['2x1'], 'ev': row['ev_2x1']})
    results.append({'name': '2x2', 'value': row['2x2'], 'ev': row['ev_2x2']})
    results.append({'name': '2x3', 'value': row['2x3'], 'ev': row['ev_2x3']})
    results.append({'name': '3x0', 'value': row['3x0'], 'ev': row['ev_3x0']})
    results.append({'name': '3x1', 'value': row['3x1'], 'ev': row['ev_3x1']})
    results.append({'name': '3x2', 'value': row['3x2'], 'ev': row['ev_3x2']})
    results.append({'name': '3x3', 'value': row['3x3'], 'ev': row['ev_3x3']})
    results.append({'name': 'AOAW', 'value': row['AOAW'], 'ev': row['ev_AOAW']})
    results.append({'name': 'AOD', 'value': row['AOD'], 'ev': row['ev_AOD']})
    results.append({'name': 'AOHW', 'value': row['AOHW'], 'ev': row['ev_AOHW']})
    sorted_results = sorted(results, key=lambda x: x['value'], reverse=True)

    ev_total = 0
    for index, result in enumerate(sorted_results):
        ev_total += result['ev']
        if (index + 1) == limit:
            return round(ev_total, 2)
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


df['Probability_5'] = df.apply(lambda row: calculate_probability_position(5, row), axis=1)
df['Probability_6'] = df.apply(lambda row: calculate_probability_position(6, row), axis=1)
df['Probability_7'] = df.apply(lambda row: calculate_probability_position(7, row), axis=1)
df['Probability_8'] = df.apply(lambda row: calculate_probability_position(8, row), axis=1)

df['Probability_5_gte80'] = df.apply(lambda row: calculate_probability_gte80(5, row), axis=1)
df['Probability_6_gte80'] = df.apply(lambda row: calculate_probability_gte80(6, row), axis=1)
df['Probability_7_gte80'] = df.apply(lambda row: calculate_probability_gte80(7, row), axis=1)
df['Probability_8_gte80'] = df.apply(lambda row: calculate_probability_gte80(8, row), axis=1)

placar = 6
df = df[(df[f'Probability_{placar}_gte80'] == 1)]
df = df.sort_values(by=['Hour'])
df.to_csv('estudo_gte80.csv', index=False)
if home:
    df = df[df['Home'] == home]
print('################################# ALL GAMES #################################')
print(df)


def change_team(df_teams, value):
    values = df_teams.loc[df_teams['betfair'] == value, 'cscore'].values
    if len(values) == 1:
        return values[0]
    return value


df_teams = pd.read_csv('./datafiles/teams.csv')
df_betfair = pd.read_csv(f'/work/automation/betfair/database/{date}.csv')
df_betfair['Home'] = df_betfair['Home'].apply(lambda row: change_team(df_teams, row))
df_betfair['Away'] = df_betfair['Away'].apply(lambda row: change_team(df_teams, row))
df = df.merge(df_betfair, how='left', on=['Home', 'Away'])
df = df.astype({'marketId': str})
print('############################ ALL GAMES WITH ODDS ############################')
print(df)

df['ev_0x0'] = df['0x0'] - (100 / df['odds_0x0'])
df['ev_0x1'] = df['0x1'] - (100 / df['odds_0x1'])
df['ev_0x2'] = df['0x2'] - (100 / df['odds_0x2'])
df['ev_0x3'] = df['0x3'] - (100 / df['odds_0x3'])
df['ev_1x0'] = df['1x0'] - (100 / df['odds_1x0'])
df['ev_1x1'] = df['1x1'] - (100 / df['odds_1x1'])
df['ev_1x2'] = df['1x2'] - (100 / df['odds_1x2'])
df['ev_1x3'] = df['1x3'] - (100 / df['odds_1x3'])
df['ev_2x0'] = df['2x0'] - (100 / df['odds_2x0'])
df['ev_2x1'] = df['2x1'] - (100 / df['odds_2x1'])
df['ev_2x2'] = df['2x2'] - (100 / df['odds_2x2'])
df['ev_2x3'] = df['2x3'] - (100 / df['odds_2x3'])
df['ev_3x0'] = df['3x0'] - (100 / df['odds_3x0'])
df['ev_3x1'] = df['3x1'] - (100 / df['odds_3x1'])
df['ev_3x2'] = df['3x2'] - (100 / df['odds_3x2'])
df['ev_3x3'] = df['3x3'] - (100 / df['odds_3x3'])
df['ev_AOAW'] = df['AOAW'] - (100 / df['odds_AOAW'])
df['ev_AOD'] = df['AOD'] - (100 / df['odds_AOD'])
df['ev_AOHW'] = df['AOHW'] - (100 / df['odds_AOHW'])

df['ev_5'] = df.apply(lambda row: calculate_ev(5, row), axis=1)
df['ev_6'] = df.apply(lambda row: calculate_ev(6, row), axis=1)
df['ev_7'] = df.apply(lambda row: calculate_ev(7, row), axis=1)
df['ev_8'] = df.apply(lambda row: calculate_ev(8, row), axis=1)
print('############################## ALL GAMES WITH EV ##############################')
print(df)
print('############################## ALL GAMES CLEANUP ##############################')
df = df[['Date', 'Hour', 'Country', 'League', 'Home', 'Away', 'Probability_5', 'ev_5', 'Probability_6', 'ev_6', 'Probability_7', 'ev_7', 'Probability_8', 'ev_8']]
df = df.sort_values(by=['Hour'])
df = df.reset_index(drop=True)
print(df)

