import streamlit as st
import pandas as pd
import preprocess
import importlib
import plotly.express as px
import matplotlib.pyplot as plt
import os

importlib.reload(preprocess)

# Sidebar
st.sidebar.title("Cricket Data Analysis")
st.sidebar.image(r"C:\Users\ZIYAD\Downloads\Cricket-Data-Analysis\cricket_image.jpg")

user_menu = st.sidebar.selectbox("Select User Type", ("Batting Statistics", "Bowling Statistics"))

# ---------------------------- BATTING SECTION ---------------------------- #
if user_menu == "Batting Statistics":
    format_selected = st.sidebar.radio("Select Format", ("ODI", "T20", "Test"))

    if format_selected == "ODI":
        df = pd.read_csv("AnalyzedData/ODI_Batting.csv", index_col=False)
    elif format_selected == "T20":
        df = pd.read_csv("AnalyzedData/T20_Batting.csv", index_col=False)
    else:
        df = pd.read_csv("AnalyzedData/Test_batting.csv", index_col=False)

    players = df["Player"].nunique()
    countries = df["Country"].nunique()
    centuries = df["Centuries"].sum()
    half_centuries = df["Half-Centuries"].sum()
    high_score = df["Highest Score"].max()
    high_score_player = df[df["Highest Score"] == high_score]

    st.title("Top Statistics")
    col1, col2, col3 = st.columns(3)
    with col1:
        st.header("Players")
        st.title(players)
    with col2:
        st.header("Countries")
        st.title(countries)
    with col3:
        st.header("Centuries")
        st.title(centuries)

    col1, col2 = st.columns(2)
    with col1:
        st.header("Half Centuries")
        st.title(half_centuries)
    with col2:
        st.header("Highest Score")
        if not high_score_player.empty:
            st.subheader(f"{high_score_player.iloc[0]['Player']} - {high_score_player.iloc[0]['Highest Score']}")
        else:
            st.write("No player data available")

    # Top stats
    top_runs = df.loc[df["Runs"].idxmax(), ["Player", "Runs"]] if "Runs" in df.columns else None
    top_avg = df[df["Innings"] >= 20].nlargest(1, "Average")[["Player", "Average"]].iloc[0] if "Average" in df.columns else None
    top_sr = df[df["Balls Faced"] >= 500].nlargest(1, "Strike Rate")[["Player", "Strike Rate"]].iloc[0] if "Strike Rate" in df.columns and "Balls Faced" in df.columns else None
    top_100s = df.loc[df["Centuries"].idxmax(), ["Player", "Centuries"]] if "Centuries" in df.columns else None
    top_50s = df.loc[df["Half-Centuries"].idxmax(), ["Player", "Half-Centuries"]] if "Half-Centuries" in df.columns else None

    st.markdown("<br><br>", unsafe_allow_html=True)
    st.title("Top players with major categories")

    col1, col2, col3 = st.columns(3)
    with col1:
        st.subheader("Most Runs")
        st.write(top_runs['Player']) if top_runs is not None else st.write("Not Available")
        st.write(f"Runs: {top_runs['Runs']}") if top_runs is not None else None

    with col2:
        st.subheader("Best Batting Average")
        st.write(top_avg['Player']) if top_avg is not None else st.write("Not Available")
        st.write(f"Avg: {top_avg['Average']:.2f}") if top_avg is not None else None

    with col3:
        st.subheader("Highest Strike Rate")
        st.write(top_sr['Player']) if top_sr is not None else st.write("Not Available")
        st.write(f"SR: {top_sr['Strike Rate']:.2f}") if top_sr is not None else None

    col1, col2 = st.columns(2)
    with col1:
        st.subheader("Most Centuries")
        st.write(top_100s['Player']) if top_100s is not None else st.write("Not Available")
        st.write(f"100s: {top_100s['Centuries']}") if top_100s is not None else None

    with col2:
        st.subheader("Most Half-Centuries")
        st.write(top_50s['Player']) if top_50s is not None else st.write("Not Available")
        st.write(f"50s: {top_50s['Half-Centuries']}") if top_50s is not None else None

    # Bar chart for top 10 players by runs
    st.markdown("<br><br>", unsafe_allow_html=True)
    st.header("Top 10 Players by Runs")
    top_players = df.sort_values("Runs", ascending=False).head(10)
    fig = px.bar(top_players,
                 x="Runs",
                 y="Player",
                 title="Top 10 Players by Runs Scored",
                 color="Runs",
                 orientation='h',
                 category_orders={"Player": top_players["Player"].tolist()})
    fig.update_layout(height=300, margin=dict(l=100, r=50, t=50, b=50), font=dict(size=14))
    st.plotly_chart(fig, use_container_width=True)

    # Player filter
    st.markdown("<br><br>", unsafe_allow_html=True)
    st.header("Most successful players")
    players1, countries1 = preprocess.converter(df)
    col1, col2 = st.columns(2)
    with col1:
        selected_player = st.selectbox("Select Player", players1)
    with col2:
        selected_country = st.selectbox("Select Country", countries1)

    players_df = preprocess.table_return(df, selected_player, selected_country)

    if selected_player == 'Overall' and selected_country == 'Overall':
        st.title("All Players stat")
    elif selected_player != 'Overall' and selected_country == 'Overall':
        st.title(f"Statistics of {selected_player} in Cricket")
    elif selected_player == 'Overall' and selected_country != 'Overall':
        st.title(f"Players of {selected_country}")
    else:
        st.title(f"Statistics of {selected_player}")

    styled_df = players_df.style.set_table_styles(
        [
            {'selector': 'thead th', 'props': [('background-color', 'black'), ('color', 'white')]},
            {'selector': 'tbody td', 'props': [('background-color', '#333'), ('color', 'white')]}
        ]
    )
    st.table(styled_df)

# ---------------------------- BOWLING SECTION ---------------------------- #
else:
    format_selected = st.sidebar.radio("Select Format", ("ODI", "T20", "Test"))

    if format_selected == "ODI":
        df = pd.read_csv("AnalyzedData/ODI_Bowling.csv")
    elif format_selected == "T20":
        df = pd.read_csv("AnalyzedData/T20_Bowling.csv")
    elif format_selected=="Test":
        df = pd.read_csv("AnalyzedData/Test_Bowling.csv")

    players = df["Player"].nunique()
    countries = df["Country"].nunique()
    
    total_5 = df["Fifer"].sum()
    if format_selected=="Test":
        total_4=df["10-Wickets"].count()
    else:
        total_4 = df["4-Wickets"].count()
    if format_selected == "T20":
        main = df.loc[df["Maidens"].idxmax()]
    else:
        main = df.loc[df["Runs"].idxmax()]


    st.title("Top Statistics")
    col1, col2, col3 = st.columns(3)
    with col1:
        st.header("Players")
        st.title(players)
    with col2:
        st.header("Countries")
        st.title(countries)
    with col3:
        if format_selected == "TEST":
            st.header("Total 10-Wickets")
            st.title(total_4)
        else:
            st.header("Total 4-Wickets")
            st.title(total_4)
    col1, col2 = st.columns(2)
    with col1:
        st.header("Total Fifers")
        st.title(total_5)
    with col2:
        if format_selected == "T20":
            st.header("Highest Maidens")
            st.subheader(f"{main['Player']} - Runs: {main['Maidens']}, Overs: {main['Overs']}")
        else:
            st.header("Most runs conceded")
            st.subheader(f"{main['Player']} - Maidens: {main['Runs']}")
