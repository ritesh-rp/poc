import streamlit as st
from snowflake_session import create_snowflake_session
from snowflake.snowpark.functions import sum, col, when, max, lag, lower, desc, lit, concat_ws, to_date
import datetime



session = create_snowflake_session()

def playing_style_query(sort_type = 'desc', show_general_data=True, filter_options={
    "team_id": None,
    "style_type": None,
    "start_date": None,
    "end_date": None
}):
    table_name = 'ALLBALL_QA.QA_DATA.TEAM_PLAYING_STYLE_OVERTIME'
    team_name = col("TEAM_NAME")
    team_id = col("TEAM_ID")
    week = col("WEEK")
    offensive_actions = col("OFFENSIVE_ACTIONS")
    defensive_actions = col("DEFENSIVE_ACTIONS")
    
    
    score_data = session.table(table_name).select(team_id, team_name, week, offensive_actions,defensive_actions)
    
    if filter_options["style_type"]:
        playing_style = filter_options["style_type"]
        if playing_style == "offensive":
            score_data = score_data.select(week, offensive_actions)
        else:
            score_data = score_data.select(week, defensive_actions)   
        
    if filter_options["team_id"]:
        id = filter_options["team_id"]
        condition = team_id == id
        score_data = score_data.where(condition)
        
    if (filter_options["start_date"] and filter_options["end_date"]):
        start_date = filter_options["start_date"]
        end_date = filter_options["end_date"]
        condition = (to_date(week) >= start_date) & (to_date(week) <= end_date)
        
        score_data = score_data.where(condition)
        
    return score_data.collect()

def team_options():
    table_name = 'ALLBALL_QA.QA_DATA.TEAM_SCORING_TREND_OVERTIME'
    team_name = col("TEAM_NAME")
    team_id = col("TEAM_ID")
    # options = session.table(table_name).select(team_name,team_id)
    options = session.table(table_name).select(concat_ws(lit("_"),team_name,team_id))
    return options.collect()

def playing_style_trend_view():
    
    options = team_options()
    playing_style_options = {
        "Offensive": "offensive",
        "Defensive": "defensive"
    }
    
    pagination_key = "Player_milestone_table_view"
    
    
    custom_table_config = {
        "show":True,
        "table_type": "player",
        "id_key": "PLAYER_ID",
        "name_key": "PLAYER_NAME",
        "value_key": ""
    }
    
    score_data = playing_style_query(sort_type="desc")
    st.subheader("Team Playing Style Trends")
    trend_to_draw = "offensive"
    show_chart = False
    with st.form(key="playing_style_trend_form"):
                field_col = st.columns(4)
                with field_col[0]:
                    selected_team = st.selectbox('Select a Team', options)
                with field_col[1]:
                    selected_style = st.selectbox('Select Playing Style', list(playing_style_options.keys()))
                with field_col[2]:
                    start_date = st.date_input("Start Date", value=None)
                with field_col[3]:
                    end_date = st.date_input("End Date", value=None,max_value=datetime.date.today())
                
                submit_col = st.columns(1)
                with submit_col[0]:
                    submitted = st.form_submit_button('Submit')
    if submitted:
            team_id = selected_team.split("_")[1]
            # score_variant = options[selected_option]
            # if score_variant == 'winning':
            filter_options = {
                    "team_id": team_id or None,
                    "style_type": playing_style_options[selected_style] or None,
                    "start_date": None or start_date,
                    "end_date": None or end_date,
                }
            score_data = playing_style_query(show_general_data=False, filter_options=filter_options)
            show_chart = True
            trend_to_draw = playing_style_options[selected_style]
    if show_chart:
        if trend_to_draw == "offensive":
         st.line_chart(score_data, x="WEEK", y="OFFENSIVE_ACTIONS")
        else: 
         st.line_chart(score_data, x="WEEK", y="DEFENSIVE_ACTIONS")
         
        st.dataframe(score_data, use_container_width=True, hide_index=True)

    else:
        info_col = st.columns(1)
        info_col[0].container(border=True).markdown("### ℹ️ Select team from dropdown to see playing style trends")
        # st.dataframe(score_data, use_container_width=True, hide_index=True)

    return None


