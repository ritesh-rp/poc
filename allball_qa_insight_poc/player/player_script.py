from player import cnx
import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt
import numpy as np
from snowflake_session import create_snowflake_session 
from snowflake.snowpark.functions import col
# import snowflake.connector

session = create_snowflake_session()

cnx = cnx.cursor()
player_profiles_df = session.table("ALLBALL_QA.QA_DATA.PLAYER_DATA")

# Collect the data as a Pandas DataFrame
player_df = player_profiles_df.to_pandas()


def display_all_player_data():
    st.dataframe(player_df, height=550)

    ################################### scoring_pattern for all #########################

    scoring_pattern_per_player = session.table("scoring_pattern_all_player_view").to_pandas()


    sp_player = scoring_pattern_per_player[['NAME','TOTAL_POINTS_SCORED']]

    st.subheader("SCORING PATTERN")
    st.bar_chart(sp_player.set_index('NAME'))





def display_charts(player_id):
    player_id = player_id[0].split(" - ")
    ################################### scoring_pattern #########################

    scoring_pattern_per_player = session.table("scoring_pattern_view").where(col("player_id")==player_id[1]).to_pandas()

    sp_player = scoring_pattern_per_player[['GAME_ID','TOTAL_POINTS_SCORED']]
    st.header(f"Name : {player_id[0]}")
    st.write(f"Player_Id : {player_id[1]}")


    st.subheader("SCORING PATTERN")
    st.bar_chart(sp_player.set_index('GAME_ID'))


    ################################### efficiency metrics #########################

    

    ################################### shooting Accuracy #########################

    



def get_player_id():
    player_id = st.multiselect(
    "Select the player_id:", 
    options=player_df["NAME"].astype(str) + ' - ' + player_df['PLAYER_ID'],max_selections=1
    )
    if player_id:
        player_id = player_id[0].split(" - ")
    return player_id
        # if player_id and :
        #     display_charts(player_id)
        # else:
        #     st.subheader("List of Registered Players")
        #     display_all_player_data()

    # except Exception as e:
    #     print("error=======================>",e)
    #     st.image("https://img.freepik.com/free-vector/404-error-with-landscape-concept-illustration_114360-7898.jpg",  use_column_width=True)


def scoring_pattern_view():
    player_id = get_player_id()
    if player_id :
        st.subheader(f"Scoring Pattern of {player_id[0]}")
        scoring_pattern_per_player = session.table("scoring_pattern_view").where(col("player_id")==player_id[1]).to_pandas()
        sp_player = scoring_pattern_per_player[['GAME_ID','TOTAL_POINTS_SCORED']]
        st.bar_chart(sp_player.set_index('GAME_ID'))

    else:
        st.subheader("Overall Scoring Pattern")
        scoring_pattern_per_player = session.table("scoring_pattern_all_player_view").to_pandas()
        sp_player = scoring_pattern_per_player[['NAME','TOTAL_POINTS_SCORED']]
        st.bar_chart(sp_player.set_index('NAME'))


    
    # st.bar_chart(sp_player.set_index('NAME'))
    st.dataframe(scoring_pattern_per_player, use_container_width=True, hide_index=True)



def efficiency_matrix_view():
    player_id = get_player_id()
    if player_id :
        st.subheader(f"Efficiency Matrix of {player_id[0]}")
        EM_per_player = session.table("player_efficiency_view").where(col("player_id")==player_id[1]).to_pandas()
    else:
        st.subheader(f"Overall Efficiency Matrix")
        EM_per_player = session.table("player_efficiency_view").to_pandas()
    EM_player = EM_per_player.loc[0, 'EFFICIENCY']

    # Pie chart data
    labels = ["Efficiency Matrix","Remaining"]
    sizes = np.array([float(EM_player), float(1 - EM_player)])
    colors = ['green', 'yellowgreen']
    explode = (0.2, 0)  # explode 1st slice (i.e. 'A')

    # Create a pie chart
    fig, ax = plt.subplots()
    ax.pie(sizes, explode=explode, labels=labels, colors=colors,
        autopct='%1.2f%%', shadow=True, startangle=140)
    ax.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.

    # Display the pie chart in Streamlit
    st.markdown("<hr>", unsafe_allow_html=True)
    st.pyplot(fig)
    st.dataframe(EM_per_player, use_container_width=True, hide_index=True)




def shooting_accuracy_view():
    player_id = get_player_id()
    if player_id :
        st.subheader(f"Shooting Accuracy of {player_id[0]}")
        SA_per_player = session.table("Player_Shooting_Accuracy_By_Type_view").where(col("player_id")==player_id[1]).to_pandas()
        # Sample data
        categories = SA_per_player['SHOTTYPE'].to_list()
        values = SA_per_player['SHOOTINGACCURACY'].to_list()
        colors = ['red', 'green', 'blue']
        # Create horizontal bar chart

        fig, ax = plt.subplots()
        ax.barh(categories, values,color=colors, height=0.3)
        # Customize labels and title
        ax.set_xlabel('Values')
        ax.set_ylabel('Categories')
        # Display the chart using Streamlit
        st.markdown("<hr>", unsafe_allow_html=True)
        st.pyplot(fig)
    
    else:
        st.subheader("Overall Shooting Accuracy")
        SA_per_player = session.table("Player_Shooting_Accuracy_By_Type_view").to_pandas()
    st.dataframe(SA_per_player, use_container_width=True, hide_index=True)


    
