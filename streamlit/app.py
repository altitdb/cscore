import pandas as pd
import streamlit as st
from awesome_table import AwesomeTable
from awesome_table.column import Column

st.set_page_config(page_title='AwesomeTable by @caiofaar', page_icon='📊', layout='wide')
st.title('Soccer Betfair Analytics')

data = pd.read_csv('https://github.com/altitdb/cscore/blob/main/datafiles/cscore.com.br.csv?raw=true')

AwesomeTable(data, columns=[
    Column(name='Home', label='Home'),
    Column(name='Away', label='Away'),
])