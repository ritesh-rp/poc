import streamlit as st
import snowflake.connector
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np


def get_connection():
    conn = snowflake.connector.connect(
        user='SOFTPRODIGY',
        password='4ChEU3ktYFh2UH9',
        account='QCQQFNP-JX01681',
        warehouse='COMPUTE_WH',
        database='ALLBALL_QA',
        schema='QA_DATA'
    )
    return conn  

connectionVariable = get_connection()

def fetch_defensive_efficiency(conn):
    query = "SELECT * FROM defensive_efficiency_view"
    df = pd.read_sql(query, conn)
    return df

def plot_defensive_efficiency(df):
    fig, ax = plt.subplots(figsize=(10, 6))    
    df = df.sort_values(by='DEFENSIVE_EFFICIENCY', ascending=False)    
    ax.bar(df['PLAYER_ID'], df['DEFENSIVE_EFFICIENCY'])    
    ax.set_xlabel('Player ID')
    ax.set_ylabel('Defensive Efficiency')
    ax.set_title('Defensive Efficiency by Player')
    ax.set_xticklabels(df['PLAYER_ID'], rotation=45, ha='right')
    ax.grid(True)
    st.pyplot(fig)

def plotDefensive():
    st.title('Defensive Efficiency Dashboard')
    conn = connectionVariable
    defensive_efficiency_df = fetch_defensive_efficiency(conn)
    st.subheader('Defensive Efficiency Data')
    st.write(defensive_efficiency_df)
    st.subheader('Defensive Efficiency Graph')
    plot_defensive_efficiency(defensive_efficiency_df)
    


    

def fetch_offensive_efficiency(conn):
    query = "SELECT * FROM offensive_efficiency_view"
    df = pd.read_sql(query, conn)
    return df

def plot_offensive_efficiency(df):
    fig, ax = plt.subplots()
    ax.bar(df['PLAYER_ID'], df['OFFENSIVE_EFFICIENCY'])
    ax.set_xlabel('Player ID')
    ax.set_ylabel('Offensive Efficiency')
    ax.set_title('Offensive Efficiency by Player')
    ax.grid(True)
    st.pyplot(fig)


def plotOffensive():
    st.title('Offensive Efficiency Dashboard')
    conn = connectionVariable
    efficiency_df = fetch_offensive_efficiency(conn)
    st.subheader('Offensive Efficiency Data')
    st.write(efficiency_df)
    st.subheader('Offensive Efficiency Graph')
    plot_offensive_efficiency(efficiency_df)


def fetch_team_synergy(conn):
    query = "SELECT * FROM team_synergy_view"
    df = pd.read_sql(query, conn)
    return df

def plot_team_synergy(df):
    fig, ax = plt.subplots()
    ax.scatter(df['PLUS_MINUS'], df['TOTAL_POINTS_ALLOWED'])
    ax.set_xlabel('Plus minus')
    ax.set_ylabel('Total Points Allowed')
    ax.set_title('Team Synergy - Points Scored vs Points Allowed')
    ax.grid(True)
    st.pyplot(fig)


def plotSynergy():
    st.title('Team Synergy Dashboard')
    conn = connectionVariable
    synergy_df = fetch_team_synergy(conn)
    st.subheader('Team Synergy Data')
    st.write(synergy_df)
    st.subheader('Team Synergy Graph')
    plot_team_synergy(synergy_df)
    





def plot_win_loss_ratio(df):
    fig, ax = plt.subplots(figsize=(10, 6))
    bar_width = 0.2
    index = np.arange(len(df))
    bar1 = ax.bar(index, df['TOTAL_WINS'], bar_width, label='Total Wins')
    bar2 = ax.bar(index + bar_width, df['TOTAL_LOSSES'], bar_width, label='Total Losses')
    bar3 = ax.bar(index + 2 * bar_width, df['WIN_LOSS_RATIO'], bar_width, label='Win-Loss Ratio')
    ax.set_xlabel('Team Name')
    ax.set_ylabel('Count / Ratio')
    ax.set_title('Team Win-Loss Ratio, Total Wins and Losses')
    ax.set_xticks(index + bar_width)
    ax.set_xticklabels(df['TEAM_NAME'], rotation=45, ha='right')
    ax.legend()
    st.pyplot(fig)




def fetch_win_loss_ratio(conn):
    query = "SELECT * FROM Team_Win_Loss_Ratio"
    df = pd.read_sql(query, conn)
    return df

def plotWinLiss():
    st.title('Team Win-Loss Ratio Dashboard')
    conn = connectionVariable
    win_loss_df = fetch_win_loss_ratio(conn)
    st.subheader('Team Win-Loss Ratio Data')
    st.write(win_loss_df)
    st.subheader('Team Win-Loss Ratio Graph')
    plot_win_loss_ratio(win_loss_df)
  



def startPlotingData():
    plotDefensive()
    plotOffensive()
    plotSynergy()
    plotWinLiss()
    connectionVariable.close()