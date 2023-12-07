import pandas as pd
from datetime import datetime, timedelta

def convert_case(value):
    if isinstance(value, str):
        return str(value).upper()
    return None


df_database = pd.read_csv('./datafiles/teams.csv')
df_database['CSCORE'] = df_database['CSCORE'].apply(lambda value: convert_case(value))
df_database['BETFAIR'] = df_database['BETFAIR'].apply(lambda value: convert_case(value))
print(f"[BEFORE] Total de times: {len(df_database)}")
df_aux = df_database['BETFAIR'].dropna()
print(f"Missing teams {len(df_database) - len(df_aux)}")
print(f"Missing teams: {df_database[df_database['BETFAIR'].isna()]}")
df_cscore = pd.read_csv('./datafiles/cscore.com.br.csv')
today = datetime.now().strftime('%Y%m%d')
tomorrow = (datetime.now() + timedelta(days=1)).strftime('%Y%m%d')
df_today = pd.read_csv(f'./datafiles/cscore.com.br-{today}.csv')
df_tomorrow = pd.read_csv(f'./datafiles/cscore.com.br-{tomorrow}.csv')
df = pd.concat([df_cscore, df_today, df_tomorrow])
df['Home'] = df['Home'].apply(lambda x: str(x).upper())
df['Away'] = df['Away'].apply(lambda x: str(x).upper())
df_teams = pd.DataFrame()
df_teams['CSCORE'] = pd.concat([df['Home'], df['Away']], join='inner')
df_teams = df_teams.drop_duplicates()

new_itens = []
for row in df_teams.iterrows():
    is_new = len(df_database[df_database['CSCORE'] == row[1]['CSCORE']]) == 0
    if is_new:
        new_itens.append({row[1]['CSCORE']})

df_database = pd.concat([df_database, pd.DataFrame(new_itens, columns=['CSCORE'])])
df_database = df_database.sort_values('CSCORE')
print(f"[AFTER] Total de times: {len(df_database)}")
df_database.to_csv('./datafiles/teams.csv', index=False)
