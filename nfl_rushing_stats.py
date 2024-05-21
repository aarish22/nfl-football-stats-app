import streamlit as st
import pandas as pd
import base64
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import plotly.express as px

st.title('NFL Football Stats (Rushing) Explorer')

st.markdown("""
Welcome to the NFL Football Stats (Rushing) Explorer! This application allows you to explore NFL rushing statistics from 1990 to 2019. Use the interactive features in the sidebar to filter data by year, team, and position.

### Features
- **Interactive Data Exploration**: Filter rushing stats by year, team, and position.
- **Data Visualization**: Generate scatter plots to visualize player performance.
- **Downloadable Data**: Export the filtered data to a CSV file for offline analysis.

### How to Use
1. **Select Year**: Choose the year of interest from the dropdown menu in the sidebar.
2. **Filter by Team and Position**: Use the multiselect options to narrow down the data to specific teams and positions.
3. **Visualize Data**: Click the buttons to generate interactive scatter plots.
4. **Download Data**: Download the filtered data for further analysis.

### Data Source
All data is sourced from [Pro-Football-Reference.com](https://www.pro-football-reference.com/).

Feel free to explore and analyze NFL rushing stats with this app!
""")

st.sidebar.header('User Input Features')
selected_year = st.sidebar.selectbox('Year', list(reversed(range(1990, 2024))))

@st.cache_data
def load_data(year):
    url = f"https://www.pro-football-reference.com/years/{year}/rushing.htm"
    html = pd.read_html(url, header=1)
    df = html[0]
    raw = df.drop(df[df.Age == 'Age'].index)  # Deletes repeating headers in content
    raw = raw.fillna(0)
    playerstats = raw.drop(['Rk'], axis=1)
    return playerstats

playerstats = load_data(selected_year)

# Sidebar - Team selection
sorted_unique_team = sorted(playerstats.Tm.unique())
selected_team = st.sidebar.multiselect('Team', sorted_unique_team, sorted_unique_team)

# Sidebar - Position selection
unique_pos = ['RB', 'QB', 'WR', 'FB', 'TE']
selected_pos = st.sidebar.multiselect('Position', unique_pos, unique_pos)

# Filtering data
df_selected_team = playerstats[(playerstats.Tm.isin(selected_team)) & (playerstats.Pos.isin(selected_pos))]

st.header('Display Player Stats of Selected Team(s)')
st.write('Data Dimension: ' + str(df_selected_team.shape[0]) + ' rows and ' + str(df_selected_team.shape[1]) + ' columns.')
st.dataframe(df_selected_team.style.highlight_max(axis=0))

def filedownload(df):
    csv = df.to_csv(index=False)
    b64 = base64.b64encode(csv.encode()).decode()  # strings <-> bytes conversions
    href = f'<a href="data:file/csv;base64,{b64}" download="playerstats.csv">Download CSV File</a>'
    return href

st.markdown(filedownload(df_selected_team), unsafe_allow_html=True)


# Interactive Plotly Scatter Plot
if st.button('Interactive Scatter Plot'):
    st.header('Interactive Scatter Plot of Rushing Yards vs. Attempts')
    fig = px.scatter(df_selected_team, x='Att', y='Yds', color='Pos',
                     hover_data=['Player', 'Tm', 'Age'],
                     labels={'Att': 'Rushing Attempts', 'Yds': 'Rushing Yards'})
    st.plotly_chart(fig)
