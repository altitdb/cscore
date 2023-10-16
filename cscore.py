import pandas as pd
import os

dfs = []
for root, dirs, files in os.walk(r'./datafiles'):
    for name in sorted(files):
        if name != 'cscore.com.br.csv':
            filename = f'./datafiles/{name}'
            print(f'Reading file {filename}')
            df = pd.read_csv(filename)
            dfs.append(df)

df = pd.concat(dfs, ignore_index=True)

df['Scoreboard'] = df['ScoreHome'].astype(str) + 'x' + df['ScoreAway'].astype(str)
df.loc[((df['ScoreHome'] > 3) & (df['ScoreHome'] > df['ScoreAway'])), 'Scoreboard'] = 'AOHW'
df.loc[((df['ScoreAway'] > 3) & (df['ScoreAway'] > df['ScoreHome'])), 'Scoreboard'] = 'AOAW'
df.loc[((df['ScoreHome'] > 3) & (df['ScoreAway'] > 3) & (df['ScoreHome'] == df['ScoreAway'])), 'Scoreboard'] = 'AOD'


def calculate_position(row):
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


df['Position'] = df.apply(lambda row: calculate_position(row), axis=1)
df['Probability_5'] = df.apply(lambda row: calculate_probability_position(5, row), axis=1)
df['Probability_6'] = df.apply(lambda row: calculate_probability_position(6, row), axis=1)
df['Probability_7'] = df.apply(lambda row: calculate_probability_position(7, row), axis=1)
df['Probability_8'] = df.apply(lambda row: calculate_probability_position(8, row), axis=1)
df['Probability_9'] = df.apply(lambda row: calculate_probability_position(9, row), axis=1)
df['Probability_10'] = df.apply(lambda row: calculate_probability_position(10, row), axis=1)
df.to_csv('./datafiles/cscore.com.br.csv')