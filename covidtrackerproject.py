import streamlit as st
import pandas as pd
import plotly.graph_objs as go
import requests
from pandas.io.json import json_normalize
st.title('COVID-19 TRACKER DATA APP')
st.sidebar.header('Covid-19 Tracker')
url = "https://api.covid19api.com/countries"
r = requests.get(url)
df1 = json_normalize(r.json())
#st.write(df1.head(5))
#df1 = pd.read_json(url, encoding="ISO-8859-1")
case_type = st.sidebar.selectbox('Cases type', ('confirmed', 'deaths', 'recovered'))
country = st.sidebar.selectbox('Country', df1.Country)
col1, col2 = st.columns(2)

if st.sidebar.checkbox('View Data'):
    if country != '':
        url = 'https://api.covid19api.com/total/dayone/country/' +country+ '/status/' +case_type
        r = requests.get(url)
        df = json_normalize(r.json())
        #df = pd.read_json(url, encoding="ISO-8859-1")
        st.write(
            """# Total Cumulative """ + case_type + """ cases in """ + country + """ are: """ + str(r.json()[-1].get("Cases")))
        st.write(country+'\'s '+case_type+' cases Tabular View of Data')
        st.dataframe(df.head(10))
        with col1:
            fig = go.Figure()
            layout = go.Layout(
              title=country + '\'s ' + case_type + ' cases Graphical Data View',
              xaxis=dict(title='Date'),
              yaxis=dict(title='Number of cases'), )
            fig.update_layout(dict1=layout, plot_bgcolor='rgba(2,2,2,2)')
            fig.add_trace(go.Scatter(x=df.Date, y=df.Cases, mode='lines', name=country,
                                     marker = {'color' : 'green'}))
        st.plotly_chart(fig, use_container_width=True)

