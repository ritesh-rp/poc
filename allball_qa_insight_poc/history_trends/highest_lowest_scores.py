import streamlit as st
from snowflake_session import create_snowflake_session
from snowflake.snowpark.functions import sum, col, when, max, lag, lower, desc
from ui_components.container_with_pagination import container_with_pagination_view, reset_pagination

session = create_snowflake_session()

def player_score_query(sort_type = 'desc', show_player_id=True, filter_options={
    "name":None,
    "player_id": None,
    "milestone_level":None,
    "is_above": True 
}):
    table_name = 'ALLBALL_QA.QA_DATA.PLAYER_OVERALL_SCORE_FROM_ALL_EVENTS'
    
    if show_player_id:
        if sort_type == 'asc':
            score_data = session.table(table_name).select(col("PLAYER_ID"),col("PLAYER_NAME"),col("OVERALL_SCORE")).orderBy(col("OVERALL_SCORE").asc())
        else:
            score_data = session.table(table_name).select(col("PLAYER_ID"),col("PLAYER_NAME"),col("OVERALL_SCORE")).orderBy(col("OVERALL_SCORE").desc())
    else:
        if sort_type == 'asc':
            score_data = session.table(table_name).select(col("PLAYER_NAME"),col("OVERALL_SCORE")).orderBy(col("OVERALL_SCORE").asc())
        else:
            score_data = session.table(table_name).select(col("PLAYER_NAME"),col("OVERALL_SCORE")).orderBy(col("OVERALL_SCORE").desc())


    
    if filter_options["player_id"]:
        print(filter_options)
        id = filter_options["player_id"]
        condition = col("PLAYER_ID") == id
        score_data = score_data.where(condition)
    
    if filter_options["name"]:
        print(filter_options)
        provided_name = filter_options["name"].lower()
        condition = lower(col("PLAYER_NAME")).like(f"%{provided_name}%")

        score_data = score_data.where(condition)

    return score_data    

def team_score_query(sort_type = 'desc',show_team_id=True, filter_options={
    "name":None,
    "team_id": None,
  
}):
    table_name = 'ALLBALL_QA.QA_DATA.TEAM_OVERALL_SCORE_FROM_ALL_EVENTS'
    
    if show_team_id:
        if sort_type == 'asc':
            score_data = session.table(table_name).select(col("TEAM_ID"), col("TEAM_NAME"), col("OVERALL_TOTAL_SCORE")).orderBy(col("OVERALL_TOTAL_SCORE").asc())
        else:
            score_data = session.table(table_name).select(col("TEAM_ID"), col("TEAM_NAME"), col("OVERALL_TOTAL_SCORE")).orderBy(col("OVERALL_TOTAL_SCORE").desc())
    else:
        if sort_type == 'asc':
            score_data = session.table(table_name).select(col("TEAM_NAME"),col("OVERALL_TOTAL_SCORE")).orderBy(col("OVERALL_TOTAL_SCORE").asc())
        else:
            score_data = session.table(table_name).select(col("TEAM_NAME"), col("OVERALL_TOTAL_SCORE")).orderBy(col("OVERALL_TOTAL_SCORE").desc())
        
    if filter_options["team_id"]:
        print(filter_options)
        id = filter_options["team_id"]
        condition = col("TEAM_ID") == id
        score_data = score_data.where(condition)
    
    if filter_options["name"]:
        print(filter_options)
        provided_name = filter_options["name"].lower()
        condition = lower(col("TEAM_NAME")).like(f"%{provided_name}%")
        score_data = score_data.where(condition)
    
    return score_data


HISTORY_TRENDS_SECTION = "history&trends"


def player_team_overall_score_view():
    
    options = {
        "Players":"player",
        "Team":"team", 
    }
    options_asc_desc = {
        "DESC":"desc",
        "ASC":"asc", 
    }
    
    pagination_key = "high/low_score_table_view"
    
    score_data = player_score_query(sort_type="desc")
    
    custom_table_config = {
        "show":True,
        "table_type": "player",
        "id_key": "PLAYER_ID",
        "name_key": "PLAYER_NAME",
        "value_key": "OVERALL_SCORE"
    }
        
    st.subheader("Overall High/Low Score View")
    
    overall_score_view_form_param_key = f"table_form_param_{pagination_key}"
    
    
    # these states are require for pagination to work properly.
    if overall_score_view_form_param_key not in st.session_state:
        st.session_state[overall_score_view_form_param_key] = {
            "show_team_table" : False,
            "filter_options" : {
                    "name":  None,
                    "player_id": None
                },
            "sort_type":options_asc_desc["DESC"],
            "custom_table_config": custom_table_config
        }

    with st.form(key="player_or_team_score_form"):
                field_col = st.columns(4)
                with field_col[0]:
                    selected_option = st.selectbox('Select Team Or Players', list(options.keys()))
                with field_col[1]:
                    player_or_team_name = st.text_input('Filter by Name (optional)')
                with field_col[2]:
                    player_or_team_id = st.text_input('Filter by Id (optional)')
                with field_col[3]:
                    asc_desc = st.selectbox('Sort by Asc or Desc', list(options_asc_desc.keys()))

                submit_col = st.columns(1)
                with submit_col[0]:
                    submitted = st.form_submit_button('Submit')
    if submitted:
            score_variant = options[selected_option]
            if score_variant == 'team':
                custom_table_config_team = {
                    "show":True,
                    "table_type": "team",
                    "id_key": "TEAM_ID",
                    "name_key": "TEAM_NAME",
                    "value_key": "OVERALL_TOTAL_SCORE"
                }
                st.session_state[overall_score_view_form_param_key] = {
                                            "show_team_table" : True,
                                            "filter_options" : {
                                                    "name":  player_or_team_name or None,
                                                    "team_id": player_or_team_id or None
                                                },
                                            "sort_type":options_asc_desc[asc_desc],
                                            "custom_table_config": custom_table_config_team
                                        }
                
            else:
                custom_table_config_player = {
                    "show":True,
                    "table_type": "player",
                    "id_key": "PLAYER_ID",
                    "name_key": "PLAYER_NAME",
                    "value_key": "OVERALL_SCORE"
                }
               
                st.session_state[overall_score_view_form_param_key] = {
                                            "show_team_table" : False,
                                            "filter_options" : {
                                                    "name":  player_or_team_name or None,
                                                    "team_id": player_or_team_id or None
                                                },
                                            "sort_type":options_asc_desc[asc_desc],
                                            "custom_table_config": custom_table_config_player
                                        }
    
            reset_pagination(pagination_key)
            
            
    if(st.session_state[overall_score_view_form_param_key]["show_team_table"]):
        active_table_state = st.session_state[overall_score_view_form_param_key]
        asc_or_desc = active_table_state["sort_type"]
        active_filter_options = active_table_state["filter_options"]
        score_data = team_score_query(sort_type=asc_or_desc, show_team_id=True, filter_options=active_filter_options)
    else:
        active_table_state = st.session_state[overall_score_view_form_param_key]
        asc_or_desc = active_table_state["sort_type"]
        active_filter_options = active_table_state["filter_options"]
        score_data = player_score_query(sort_type=asc_or_desc,show_player_id=True,filter_options=active_filter_options)
        
    # st.dataframe(score_data, use_container_width=True, hide_index=True)
    # st.write(score_data)
    
    # st.write(st.session_state)
    custom_table_config = st.session_state[overall_score_view_form_param_key]["custom_table_config"]
    container_with_pagination_view(table_data=score_data, pagination_key=pagination_key,custom_table_config=custom_table_config)
    
    return None


