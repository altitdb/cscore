import pandas as pd

df_database = pd.read_csv('./datafiles/teams.csv')
print(f"[BEFORE] Total de times: {len(df_database)}")
df_aux = df_database['betfair'].dropna()
print(f"Missing teams {len(df_database) - len(df_aux)}")
df = pd.read_csv('./datafiles/cscore.com.br.csv')
df_teams = pd.DataFrame()
df_teams['cscore'] = pd.concat([df['Home'], df['Away']], join='inner').drop_duplicates()

new_itens = []
for row in df_teams.iterrows():
    is_new = len(df_database[df_database['cscore'] == row[1]['cscore']]) == 0
    if is_new:
        new_itens.append({row[1]['cscore']})

df_database = pd.concat([df_database, pd.DataFrame(new_itens, columns=['cscore'])])
df_database = df_database.sort_values('cscore')
print(f"[AFTER] Total de times: {len(df_database)}")
df_database.to_csv('./datafiles/teams.csv', index=False)
