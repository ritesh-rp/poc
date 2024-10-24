import streamlit as st
from snowflake_session import create_snowflake_session
from snowflake.snowpark.functions import col

session = create_snowflake_session()

def team_card(
    team_name=None,
    team_id=None,
    param_name=None,
    param_value=None
   
):
    teams_table = 'ALLBALL_QA.QA_DATA.TEAM_OVERALL_SCORE_FROM_ALL_EVENTS'
    
    team_id_col = col("TEAM_ID")
    
    team_detail = session.table(teams_table).select("*").where(team_id_col == team_id).collect()
    
    
    overall_score=None
    total_three_point_make=None
    total_two_point_make=None
    total_one_point_make=None
    
    for item in team_detail:
        overall_score=item["OVERALL_TOTAL_SCORE"] 
        total_three_point_make=item["OVERALL_TOTAL_THREE_POINT_MAKE"] 
        total_two_point_make=item["OVERALL_TOTAL_TWO_POINT_MAKE"] 
        total_one_point_make=item["OVERALL_TOTAT_ONE_POINT_MAKE"] 
    
    card_container = st.container(border=True)
    card_sections = card_container.columns([3,2])
    details = card_container.columns([3,1])
    
    with card_sections[0]:
        st.markdown(f"👨‍👦‍👦 Name: {team_name}")
        
    with card_sections[1]:
        
        st.markdown(f"🎯 {param_name}: {param_value}")
        
    with details[0]:
     
        with st.expander("ℹ️ Team Details"):
            team_details = st.container()
            team_info = team_details.columns(2)            
            with team_info[0]:
                st.write(f"🆔:  {team_id}")
            with team_info[1]:
                st.write(f"👥 Name :  {team_name}")
            
            st.write(f"➡️ Overall SCORE :  {overall_score} ")
            st.write(f"➡️ Total Three Point Make : {total_three_point_make} ")
            st.write(f"➡️ Total Two Point Make :  {total_two_point_make}")
            st.write(f"➡️ Total one Point Make :  {total_one_point_make}")
            
            
            
def player_card(
    name=None,
    id=None,
    param_name=None,
    param_value=None
   
):
    profile_table = 'ALLBALL_QA.QA_DATA.PLAYER_PROFILE_BY_TEAM_ROLE_ID'
    
    id_col = col("PLAYER_ID")
    
    player_detail = session.table(profile_table).select("*").where(id_col == id).collect()
    
    
    email=None 
    gender=None
    selected_team_id=None
            
    for item in player_detail:
        email=item["EMAIL"] 
        gender=item["GENDER"] 
        selected_team_id=item["SELECTED_TEAM_ID"] 
    
    card_container = st.container(border=True)
    card_sections = card_container.columns([3,2])
    details = card_container.columns([3,1])
    
    with card_sections[0]:
        st.markdown(f"👨‍👦‍👦 Name: {name}")
        
    with card_sections[1]:
        
        st.markdown(f"🎯 {param_name}: {param_value}")
        
    with details[0]:
     
        with st.expander("ℹ️ Player Details"):
            team_details = st.container()
            team_info = team_details.columns(2)            
            with team_info[0]:
                st.write(f"🆔:  {id}")
            with team_info[1]:
                st.write(f"👥 Name :  {name}")
            
            st.write(f"➡️ Email:  {email} ")
            st.write(f"➡️ Gender : {gender} ")
            st.write(f"➡️ Selected Team ID :  {selected_team_id}")
