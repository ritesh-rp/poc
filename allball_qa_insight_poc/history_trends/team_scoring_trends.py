import streamlit as st
from snowflake_session import create_snowflake_session
from snowflake.snowpark.functions import sum, col, when, max, lag, lower, desc, lit, concat_ws, to_date
import datetime

# streamlit-datetime-range-picker
    
session = create_snowflake_session()

def scoring_trend_query(sort_type = 'desc', show_general_data=True, filter_options={
    "team_id": None,
    "start_date": None,
    "end_date": None
}):
    table_name = 'ALLBALL_QA.QA_DATA.TEAM_SCORING_TREND_OVERTIME'
    team_name = col("TEAM_NAME")
    team_id = col("TEAM_ID")
    week = col("WEEK")
    total_points = col("TOTAL_POINTS")
    
              
    score_data = session.table(table_name).select(team_id, team_name, week, total_points).orderBy(total_points.desc())
        
    
    if filter_options["team_id"]:
        id = filter_options["team_id"]
        condition = team_id == id
        score_data = score_data.select(week, total_points).where(condition)
        
    if (filter_options["start_date"] and filter_options["end_date"]):
        start_date = filter_options["start_date"]
        end_date = filter_options["end_date"]
        condition = (to_date(week) >= start_date) & (to_date(week) <= end_date)
        
        score_data = score_data.select(week, total_points).where(condition)
        
    return score_data.collect()
                 
def team_options():
    table_name = 'ALLBALL_QA.QA_DATA.TEAM_SCORING_TREND_OVERTIME'
    team_name = col("TEAM_NAME")
    team_id = col("TEAM_ID")
    # options = session.table(table_name).select(team_name,team_id)
    options = session.table(table_name).select(concat_ws(lit("_"),team_name,team_id))
    return options.collect()
      
def scoring_trend_view():
    
    options = team_options()
    options_asc_desc = {
        "DESC":"desc",
        "ASC":"asc", 
    }
                     
    score_data = scoring_trend_query(sort_type="desc")
    show_chart = False
    st.subheader("Team Scoring Trends")
                                                                    
    with st.form(key="scoring_trend_form"):
                field_col = st.columns(3)
                with field_col[0]:
                    selected_team = st.selectbox('Select a Team', options)
                with field_col[1]:
                    start_date = st.date_input("Start Date", value=None)
                with field_col[2]:
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
                    "start_date": None or start_date,
                    "end_date": None or end_date,
                }
            score_data = scoring_trend_query(show_general_data=False, filter_options=filter_options)
            show_chart = True
    if show_chart:
        st.line_chart(score_data, x="WEEK", y="TOTAL_POINTS")
        st.dataframe(score_data, use_container_width=True, hide_index=True)

    else:
        info_col = st.columns(1)
        info_col[0].container(border=True).markdown("### ℹ️ Select team from dropdown to see playing style trends")
        # st.dataframe(score_data, use_container_width=True, hide_index=True)

    return None

        
          