import pandas as pd

data = pd.read_csv('cscore.com.br.csv')
print(data)

import streamlit as st
from awesome_table import AwesomeTable
from awesome_table.column import Column

st.set_page_config(page_title='Soccer Betfair Analytics by @altitdb', page_icon='📊', layout='wide')
st.title('Soccer Betfair Analytics by @altitdb')

AwesomeTable(data, show_search=True, show_order=True)