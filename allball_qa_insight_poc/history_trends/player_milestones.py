import streamlit as st
from snowflake_session import create_snowflake_session
from snowflake.snowpark.functions import sum, col, when, max, lag, lower
from ui_components.container_with_pagination import container_with_pagination_view, reset_pagination


session = create_snowflake_session()



def player_milestone_query(table_name, milestone_type=None, sort_type="desc" ,show_player_id=False, filter_options={
    "name":None,
    "player_id": None,
    "milestone_level":None,
    "is_above": True 
}):
    print("Recieved type:",milestone_type )
    milestone_type_options = [
        "TOTAL_SCORE","FIELD_GOALS_MADE","MISSED_FIELD_GOALS","TOTAL_OFFENSIVE_REBOUNDS","TOTAL_DEFENSIVE_REBOUNDS","TOTAL_ASSIST","TOTAL_BLOCKS","TOTAL_STEALS","TOTAL_TURNOVER"
    ]
    milestone_data = session.table(table_name).select("*")

    if milestone_type in milestone_type_options:
        if show_player_id:
            milestone_data = session.table(table_name).select("PLAYER_ID","PLAYER_NAME", milestone_type)
        else: 
            milestone_data = session.table(table_name).select("PLAYER_NAME", milestone_type)
    else:
        return None
    
    if filter_options["player_id"]:
        print(filter_options)
        id = filter_options["player_id"]
        condition = col("PLAYER_ID") == id
        milestone_data = milestone_data.where(condition)
    
    if filter_options["name"]:
        print(filter_options)
        provided_name = filter_options["name"].lower()
        condition = lower(col("PLAYER_NAME")).like(f"%{provided_name}%")
        milestone_data = milestone_data.where(condition)
        
    if filter_options["milestone_level"]:
        print(filter_options)
        level = filter_options["milestone_level"]
        
        condition = col(milestone_type) > level
        
        if filter_options["is_above"] == False:
            condition = col(milestone_type) < level
        
        milestone_data = milestone_data.where(condition)
    
    if sort_type == "asc":
        milestone_data = milestone_data.order_by(col(milestone_type).asc())
    else:
        milestone_data = milestone_data.order_by(col(milestone_type).desc())
        
        
    return milestone_data

HISTORY_TRENDS_SECTION = "history&trends"
                                             
def player_milestone_view():
    st.subheader("Player Milestones")
    options = {
    "SCORE": "TOTAL_SCORE",\
    "FIELD GOALS MADE": "FIELD_GOALS_MADE",
    "MISSED FIELD GOALS": "MISSED_FIELD_GOALS",
    "OFFENSIVE REBOUNDS": "TOTAL_OFFENSIVE_REBOUNDS",
    "DEFENSIVE REBOUNDS": "TOTAL_DEFENSIVE_REBOUNDS",
    "ASSIST": "TOTAL_ASSIST",
    "BLOCKS": "TOTAL_BLOCKS",
    "STEALS": "TOTAL_STEALS",
    "TURNOVER": "TOTAL_TURNOVER",
    }
    options_asc_desc = {
        "DESC":"desc",
        "ASC":"asc", 
    }
    pagination_key = "Player_milestone_table_view"
    
    
    custom_table_config = {
        "show":True,
        "table_type": "player",
        "id_key": "PLAYER_ID",
        "name_key": "PLAYER_NAME",
        "value_key": options["SCORE"]
    }
    
    player_milestone_view_form_param_key = f"table_form_param_{pagination_key}"
    
    
    # these states are require for pagination to work properly.
    if player_milestone_view_form_param_key not in st.session_state:
        st.session_state[player_milestone_view_form_param_key] = {
            "milestone_key_name" : "SCORE",
            "milestone_type":options["SCORE"],
            "player_name": None, 
            "show_id":True,
            "milestone_number": None,
            "sort_type":options_asc_desc["DESC"],
            "custom_table_config": custom_table_config
        }

    
    # Create the checkbox for showing player ID
    def get_data(milestone_type, filter_options, show_player_id, sort_type):
        player_milestone_view = "ALLBALL_QA.QA_DATA.PLAYER_MILESTONE"
        different_milestone_type_df = player_milestone_query(
            table_name=player_milestone_view,
            milestone_type=milestone_type, 
            show_player_id=show_player_id,
            sort_type=sort_type,
            filter_options=filter_options
            )
        return different_milestone_type_df
    
    def process_data(milestone_key_name, milestone_type, player_name, show_id, milestone_number, sort_type):
        filter_options={
            "name": None or player_name,
            "milestone_level": None or milestone_number,
            "player_id": None,
            "is_above": True
        }
        
        different_milestone_type_df = get_data(milestone_type=milestone_type, filter_options=filter_options, show_player_id=show_id, sort_type=sort_type)
        return different_milestone_type_df
   
                    
    milestone_data =  process_data(
                milestone_key_name = "SCORE",
                milestone_type= options["SCORE"],
                player_name = None, 
                show_id=True,
                milestone_number=None,
                sort_type=options_asc_desc["DESC"]
                )
    with st.form(key="player_milestones_form"):
                field_col = st.columns(4)
                with field_col[0]:
                    selected_option = st.selectbox('Select Milestone type', list(options.keys()))
                with field_col[1]:
                    player_name = st.text_input('Filter by player name (optional)')
                with field_col[2]:
                    milestone_number = st.number_input("Minimum Milestone Value (optional)",value=None)
                with field_col[3]:
                    asc_desc = st.selectbox('Sort by Asc or Desc', list(options_asc_desc.keys()))
                    
                submit_col = st.columns(1)
                with submit_col[0]:
                    submitted = st.form_submit_button('Submit')
    if submitted:
            db_value =  options[selected_option]
            custom_table_config_player = {
                "show":True,
                "table_type": "player",
                "id_key": "PLAYER_ID",
                "name_key": "PLAYER_NAME",
                "value_key": db_value
            }
            
            st.session_state[player_milestone_view_form_param_key]={
            "milestone_key_name" : selected_option,
            "milestone_type":options[selected_option],
            "player_name": player_name, 
            "show_id":True,
            "milestone_number": milestone_number,
            "sort_type":options_asc_desc[asc_desc],
            "custom_table_config": custom_table_config_player
        }
    
            # milestone_data= process_data(
            #     milestone_key_name = selected_option,
            #     milestone_type=db_value,
            #     player_name = player_name, 
            #     show_id=True,
            #     milestone_number = milestone_number,
            #     sort_type=options_asc_desc[asc_desc]
            #     )
            reset_pagination(pagination_key=pagination_key)
            
            
    
    active_table_options = st.session_state[player_milestone_view_form_param_key]
    milestone_data= process_data(
        milestone_key_name = active_table_options["milestone_key_name"],
        milestone_type=active_table_options["milestone_type"],
        player_name = active_table_options["player_name"], 
        show_id=True,
        milestone_number = active_table_options["milestone_number"],
        sort_type=active_table_options["sort_type"]
        )
    
    custom_table_config = active_table_options["custom_table_config"]
    # st.write(st.session_state)
    # st.write(milestone_data)
            
    container_with_pagination_view(table_data=milestone_data, pagination_key=pagination_key,custom_table_config=custom_table_config)
    
    # st.dataframe(milestone_data, use_container_width=True, hide_index=True)
   
    return None


                                  