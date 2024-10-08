import streamlit as st
import pandas as pd
import numpy as np
from io import StringIO
import requests as rq
import bs4
import plotly.express as px

url = 'https://en.wikipedia.org/wiki/List_of_countries_by_GDP_(nominal)'
page = rq.get(url)

bs4page = bs4.BeautifulSoup(page.text, 'html.parser')
for tag in bs4page.find_all(class_="reference"):
        tag.decompose()

tables = bs4page.find_all('table',{'class':"wikitable"})

gdp = pd.read_html(StringIO(str(tables[0])))[0]
gdp = gdp.dropna()

gdp.columns = ['Country/Territory', 'IMF Forecast', 'IMF Year', 'World Bank Estimate', 'World Bank Year', 'United Nations Estimate', 'United Nations Year']
gdp = gdp.drop(index=0)

st.set_page_config(layout="wide")

st.write("""
# GDP Bar Chart per IMF, World Bank, and United Nations
"""
)

st.header("Please choose which category to plot")

rb = st.radio(
    "Category",
    ('IMF', 'World Bank', 'United Nations'))

countries_continent_df = pd.read_csv('list-of-countries-by-continent-2024.csv')
countries_continent_df = countries_continent_df.drop(columns='unMember')
countries_continent_df.columns = ['Country/Territory', 'Continent']

merged_df = pd.merge(gdp, countries_continent_df, on="Country/Territory")
merged_df = merged_df.dropna()

if rb == 'IMF':
    IMF_df = merged_df[["Country/Territory", "IMF Forecast", "Continent"]]
    fig = px.bar(IMF_df, x = "Continent", y = "IMF Forecast", color = "Country/Territory")
    fig.update_layout(barmode='stack', xaxis_title='Continent (Region)', yaxis_title='GDP Forecast', title='Stacked Barchart of Country GDP')
    st.plotly_chart(fig, use_container_width=True)
elif rb == 'World Bank':
    WB_df = merged_df[["Country/Territory", "World Bank Estimate", "Continent"]]
    fig = px.bar(WB_df, x = "Continent", y = "World Bank Estimate", color = "Country/Territory")
    fig.update_layout(barmode='stack', xaxis_title='Continent (Region)', yaxis_title='GDP Estimate', title='Stacked Barchart of Country GDP')
    st.plotly_chart(fig, use_container_width=True)
else:
    UN_df = merged_df[["Country/Territory", "United Nations Estimate", "Continent"]]
    fig = px.bar(merged_df, x = "Continent", y = "United Nations Estimate", color = "Country/Territory")
    fig.update_layout(barmode='stack', xaxis_title='Continent (Region)', yaxis_title='GDP Estimate', title='Stacked Barchart of Country GDP')
    st.plotly_chart(fig, use_container_width=True)

if rb == 'IMF':
        st.dataframe(merged_df[["Country/Territory", "IMF Forecast", "IMF Year"]], hide_index=True, use_container_width=True)
elif rb == 'World Bank':
        st.dataframe(merged_df[["Country/Territory", "World Bank Estimate", "World Bank Year"]], hide_index=True, use_container_width=True)
else:
        st.dataframe(merged_df[["Country/Territory", "United Nations Estimate", "United Nations Year"]], hide_index=True, use_container_width=True)