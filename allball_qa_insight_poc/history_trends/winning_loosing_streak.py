import streamlit as st
from snowflake_session import create_snowflake_session
from snowflake.snowpark.functions import sum, col, when, max, lag, lower, desc
from ui_components.container_with_pagination import container_with_pagination_view, reset_pagination


session = create_snowflake_session()

def winning_streak_query(sort_type = 'desc', show_team_id=True, filter_options={
    "name":None,
    "team_id": None,
}):
    table_name = 'ALLBALL_QA.QA_DATA.TEAM_WINNING_STREAK'
    
    if show_team_id:
        if sort_type == 'asc':
            score_data = session.table(table_name).select(col("WINNING_TEAM_ID"),col("TEAM_NAME"),col("CURRENT_WINNING_STREAK")).orderBy(col("CURRENT_WINNING_STREAK").asc())
        else:
            score_data = session.table(table_name).select(col("WINNING_TEAM_ID"),col("TEAM_NAME"),col("CURRENT_WINNING_STREAK")).orderBy(col("CURRENT_WINNING_STREAK").desc())
    else:
        if sort_type == 'asc':
            score_data = session.table(table_name).select(col("TEAM_NAME"),col("CURRENT_WINNING_STREAK")).orderBy(col("CURRENT_WINNING_STREAK").asc())
        else:
            score_data = session.table(table_name).select(col("TEAM_NAME"),col("CURRENT_WINNING_STREAK")).orderBy(col("CURRENT_WINNING_STREAK").desc())


    
    if filter_options["team_id"]:
        print(filter_options)
        id = filter_options["team_id"]
        condition = col("WINNING_TEAM_ID") == id
        score_data = score_data.where(condition)
    
    if filter_options["name"]:
        print(filter_options)
        provided_name = filter_options["name"].lower()
        condition = lower(col("TEAM_NAME")).like(f"%{provided_name}%")
        score_data = score_data.where(condition)

    return score_data    

def losing_streak_query(sort_type = 'desc',show_team_id=True, filter_options={
    "name":None,
    "team_id": None,
  
}):
    table_name = 'ALLBALL_QA.QA_DATA.TEAM_LOSING_STREAK'
    
    if show_team_id:
        if sort_type == 'asc':
            score_data = session.table(table_name).select(col("LOSING_TEAM_ID"),col("TEAM_NAME"),col("CURRENT_LOSING_STREAK")).orderBy(col("CURRENT_LOSING_STREAK").asc())
        else:
            score_data = session.table(table_name).select(col("LOSING_TEAM_ID"),col("TEAM_NAME"),col("CURRENT_LOSING_STREAK")).orderBy(col("CURRENT_LOSING_STREAK").desc())
    else:
        if sort_type == 'asc':
            score_data = session.table(table_name).select(col("TEAM_NAME"),col("CURRENT_LOSING_STREAK")).orderBy(col("CURRENT_LOSING_STREAK").asc())
        else:
            score_data = session.table(table_name).select(col("TEAM_NAME"),col("CURRENT_LOSING_STREAK")).orderBy(col("CURRENT_LOSING_STREAK").desc())
        
    if filter_options["team_id"]:
        print(filter_options)
        id = filter_options["team_id"]
        condition = col("LOSING_TEAM_ID") == id
        score_data = score_data.where(condition)
    
    if filter_options["name"]:
        print(filter_options)
        provided_name = filter_options["name"].lower()
        condition = lower(col("TEAM_NAME")).like(f"%{provided_name}%")
        score_data = score_data.where(condition)
    
    return score_data


HISTORY_TRENDS_SECTION = "history&trends"


def winning_losing_streak_view():
    
    options = {
        "Winning Streak":"winning",
        "Losing Streak":"losing", 
    }
    options_asc_desc = {
        "DESC":"desc",
        "ASC":"asc", 
    }
    
    pagination_key = "winning_loosing_streak_table_view"
    
    
    custom_table_config = {
        "show":True,
        "table_type": "team",
        "id_key": "WINNING_TEAM_ID",
        "name_key": "TEAM_NAME",
        "value_key": "CURRENT_WINNING_STREAK"
    }
    
    winning_losing_streak_view_form_param_key = f"table_form_param_{pagination_key}"
    
    
    # these states are require for pagination to work properly.
    if winning_losing_streak_view_form_param_key not in st.session_state:
        st.session_state[winning_losing_streak_view_form_param_key] = {
            "show_winning_streak":True,
            "filter_options" : {
                    "name": None,
                    "team_id": None
            },
            "sort_type":options_asc_desc["DESC"],
            "custom_table_config": custom_table_config
        }
    
    score_data = winning_streak_query(sort_type="desc")
    
    st.subheader("Winning/Losing Streak View")

    with st.form(key="winning_losing_streak_form"):
                field_col = st.columns(4)
                with field_col[0]:
                    selected_option = st.selectbox('Select Team Or Players', list(options.keys()))
                with field_col[1]:
                    team_name = st.text_input('Filter by Name (optional)')
                with field_col[2]:
                    team_id = st.text_input('Filter by Id (optional)')
                with field_col[3]:
                    asc_desc = st.selectbox('Sort by Asc or Desc', list(options_asc_desc.keys()))
                    
                submit_col = st.columns(1)
                with submit_col[0]:
                    submitted = st.form_submit_button('Submit')
    if submitted:
            score_variant = options[selected_option]
            if score_variant == 'winning':
                filter_options = {
                    "name": team_name or None,
                    "team_id": team_id or None
                }
                
                st.session_state[winning_losing_streak_view_form_param_key]={
                                                    "show_winning_streak":True,
                                                    "filter_options" : {
                                                        "name": team_name or None,
                                                        "team_id":  team_id or None
                                                    },
                                                    "sort_type":options_asc_desc[asc_desc],
                                                    "custom_table_config": custom_table_config
                                            }
                # st.write(filter_options, score_variant, asc_desc, )
                # score_data = winning_streak_query(sort_type=options_asc_desc[asc_desc], show_team_id=True, filter_options=filter_options)
            else:
               st.write("loosing")
               filter_options = {
                    "name": team_name or None,
                    "team_id": team_id or None
                }
               custom_table_config_loosing_team = {
                            "show":True,
                            "table_type": "team",
                            "id_key": "LOSING_TEAM_ID",
                            "name_key": "TEAM_NAME",
                            "value_key": "CURRENT_LOSING_STREAK"
                        }
               st.session_state[winning_losing_streak_view_form_param_key]={
                                                "show_winning_streak":False,
                                                "filter_options" : {
                                                    "name": team_name or None,
                                                    "team_id":  team_id or None
                                                },
                                                "sort_type":options_asc_desc[asc_desc],
                                                "custom_table_config": custom_table_config_loosing_team
                                            }
              # score_data = losing_streak_query(sort_type=options_asc_desc[asc_desc],show_team_id=True,filter_options=filter_options)
    
    active_table_state = st.session_state[winning_losing_streak_view_form_param_key]
    if(st.session_state[winning_losing_streak_view_form_param_key]["show_winning_streak"]):
        asc_or_desc = active_table_state["sort_type"]
        active_filter_options = active_table_state["filter_options"]
        score_data = winning_streak_query(sort_type=asc_or_desc, show_team_id=True, filter_options=active_filter_options)
    else:
        asc_or_desc = active_table_state["sort_type"]
        active_filter_options = active_table_state["filter_options"]
        score_data = losing_streak_query(sort_type=asc_or_desc,show_team_id=True,filter_options=active_filter_options)
    
    custom_table_config=active_table_state["custom_table_config"]
    
    # st.write(st.session_state)
    
    container_with_pagination_view(table_data=score_data, pagination_key=pagination_key, custom_table_config=custom_table_config)
    
    # st.dataframe(score_data, use_container_width=True, hide_index=True)

    return None


