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
filename = f'./datafiles/cscore.com.br-{date}.csv'
print(f'Reading file {filename}')
df = pd.read_csv(filename)

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
df['Probability_9'] = df.apply(lambda row: calculate_probability_position(9, row), axis=1)
df['Probability_10'] = df.apply(lambda row: calculate_probability_position(10, row), axis=1)

df['Probability_5_gte80'] = df.apply(lambda row: calculate_probability_gte80(5, row), axis=1)
df['Probability_6_gte80'] = df.apply(lambda row: calculate_probability_gte80(6, row), axis=1)
df['Probability_7_gte80'] = df.apply(lambda row: calculate_probability_gte80(7, row), axis=1)
df['Probability_8_gte80'] = df.apply(lambda row: calculate_probability_gte80(8, row), axis=1)
df['Probability_9_gte80'] = df.apply(lambda row: calculate_probability_gte80(9, row), axis=1)
df['Probability_10_gte80'] = df.apply(lambda row: calculate_probability_gte80(10, row), axis=1)

placar = 6
df = df[(df[f'Probability_{placar}_gte80'] == 1)]
df = df.sort_values(by=['Hour'])
df = df.reset_index(drop=True)
print(df)

