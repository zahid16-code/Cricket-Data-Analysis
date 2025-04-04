import pandas as pd
import numpy as np

def converter(df):
    years = df['Player'].unique().tolist()
    years.sort()
    years.insert(0, 'Overall')

    country = np.unique(df['Country'].dropna().values).tolist()
    country.sort()
    country.insert(0, 'Overall')

    return years,country
def table_return(medal_df,year,country):
    if year == 'Overall' and country == 'Overall':
        temp_df = medal_df
    if year == 'Overall' and country != 'Overall':
        flag = 1
        temp_df = medal_df[medal_df['Country'] == country]
    if year != 'Overall' and country == 'Overall':
        temp_df = medal_df[medal_df['Player'] == year]
    if year != 'Overall' and country != 'Overall':
        temp_df = medal_df[(medal_df['Player'] == year) & (medal_df['Country'] == country)]
    return temp_df