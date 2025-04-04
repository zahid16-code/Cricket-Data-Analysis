import streamlit as st
import pandas as pd
import preprocess
import importlib
import plotly.express as px
import matplotlib.pyplot as plt
importlib.reload(preprocess)

st.sidebar.title("Cricket Data Analysis")
st.sidebar.image(r"C:\Users\ZIYAD\Downloads\Cricket-Data-Analysis\cricket_image.jpg")

user_menu = st.sidebar.radio(
    "Select User Type",
    ("Batting Statistics", "Bowling Statistics", "Fielding Statistics")
)

if user_menu == "Batting Statistics":
    format_selected = st.sidebar.radio("Select Format", ("ODI", "T20", "Test"))
    
    if format_selected == "ODI":
        df = pd.read_csv("AnalyzedData/ODI.csv",index_col=False)
    elif format_selected == "T20":
        df = pd.read_csv("AnalyzedData/T20.csv",index_col=False)
    else:
        df = pd.read_csv("AnalyzedData/Test.csv",index_col=False)
    
    players = df["Player"].nunique()
    countries = df["Country"].nunique()
    centuries = df["Centuries"].sum()
    half_centuries = df["Half-Centuries"].sum()
    high_score=df["Highest Score"].max()
    high_score_player=df[df["Highest Score"]==high_score]
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
        if len(high_score_player) > 1:
            st.subheader(f"{high_score_player.iloc[0]['Player']} - {high_score_player.iloc[0]['Highest Score']}")
        elif len(high_score_player) == 1:
            st.subheader(f"{high_score_player.iloc[0]['Player']} -{high_score_player.iloc[0]['Highest Score']}")
        else:
            st.write("No player data available")



    
    if "Runs" in df.columns:
        top_runs = df.loc[df["Runs"].idxmax(), ["Player", "Runs"]]
    else:
        top_runs = None
    
    if "Average" in df.columns:
        top_avg = df[df["Innings"] >= 20].nlargest(1, "Average")[["Player", "Average"]].iloc[0]
    else:
        top_avg = None
    
    if "Strike Rate" in df.columns and "Balls Faced" in df.columns:
        top_sr = df[df["Balls Faced"] >= 500].nlargest(1, "Strike Rate")[["Player", "Strike Rate"]].iloc[0]
    else:
        top_sr = None
    
    if "Centuries" in df.columns:
        top_100s = df.loc[df["Centuries"].idxmax(), ["Player", "Centuries"]]
    else:
        top_100s = None
    
    if "Half-Centuries" in df.columns:
        top_50s = df.loc[df["Half-Centuries"].idxmax(), ["Player", "Half-Centuries"]]
    else:
        top_50s = None
    
    st.markdown("<br><br>", unsafe_allow_html=True)
    st.title("Top players with major categories")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.subheader("Most Runs")
        if top_runs is not None:
            st.write(top_runs['Player'])
            st.write(f" Runs: {top_runs['Runs']}")
        else:
            st.write("Not Available")
    
    with col2:
        st.subheader("Best Batting Average")
        if top_avg is not None:
            st.write(top_avg['Player'])
            st.write(f"Avg: {top_avg['Average']:.2f}")
        else:
            st.write("Not Available")
    
    with col3:
        st.subheader("Highest Strike Rate")
        if top_sr is not None:
            st.write(top_sr['Player'])
            st.write(f"SR: {top_sr['Strike Rate']:.2f}")
        else:
            st.write("Not Available")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Most Centuries")
        if top_100s is not None:
            st.write(top_100s['Player'])
            st.write(f"100s: {top_100s['Centuries']}")
        else:
            st.write("Not Available")
    
    with col2:
        st.subheader("Most Half-Centuries")
        if top_50s is not None:
            st.write(top_50s['Player'])
            st.write(f"50s: {top_50s['Half-Centuries']}")
        else:
            st.write("Not Available")

    
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

    # Adjust figure size using layout
    fig.update_layout(
        width=100000,  # Set width (increase for bigger charts)
        height=300,  # Set height
        margin=dict(l=100, r=50, t=50, b=50),  # Adjust margins
        font=dict(size=14)  # Increase font size for better readability
    )

    # Display plot
    st.plotly_chart(fig, use_container_width=True) 
    st.markdown("<br><br>", unsafe_allow_html=True)
    st.header("Most successfull players")
    players1,countries1=preprocess.converter(df)
    col1,col2=st.columns(2)
    with col1:
        selected_player=st.selectbox("Select Player",players1)
    with col2:
        selected_country=st.selectbox("Select Country",countries1)
    players_df=preprocess.table_return(df,selected_player,selected_country)
    if selected_player == 'Overall' and selected_country == 'Overall':
        st.title("All Players stat")
    if selected_player != 'Overall' and selected_country == 'Overall':
        st.title("Statistics of  " + str(selected_player) + "In Cricket")
    if selected_player == 'Overall' and selected_country != 'Overall':
        st.title("Players of "+ selected_country)
    if selected_player!= 'Overall' and selected_country != 'Overall':
        st.title("Statistics of "+ selected_player)
    styled_df = players_df.style.set_table_styles(
    [
        {'selector': 'thead th', 'props': [('background-color', 'black'), ('color', 'white')]},
        {'selector': 'tbody td', 'props': [('background-color', '#333'), ('color', 'white')]}
    ]
     )
    st.table(styled_df)