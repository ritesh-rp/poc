import streamlit as st
from snowflake_session import create_snowflake_session
from snowflake.snowpark import DataFrame
from snowflake.snowpark.functions import sum, col, when, max, lag, lower, desc
from ui_components.table_card import team_card,player_card

import math

session = create_snowflake_session()


def reset_pagination(pagination_key):
    """
    Args: pagination_key : used to reset correct state, same key which was used to create pagination container should be provided.
    """
    pagination_btn_state_name = f"pagination_btn_state_{pagination_key}"
    if pagination_btn_state_name in st.session_state:
        st.session_state[pagination_btn_state_name] = {
            "current_page": 1,
            "offset": 0
        }

def container_with_pagination_view(table_data: DataFrame, rows_per_page = 10, pagination_key="Some", dataframe_options={
    "full_width": True,
    "hide_index": True
},
   custom_table_config={
        "show":False,
        "table_type": "team",
        "id_key": None,
        "name_key": None,
        "value_key": None
   }                                
):
    pagination_btn_state_name = f"pagination_btn_state_{pagination_key}"
    if pagination_btn_state_name not in st.session_state:
        st.session_state[pagination_btn_state_name] = {
            "current_page": 1,
            "offset": 0
        }
    
    # main_container = st.container()
    data_container = st.container(border=True, height=600)
    page_size = rows_per_page
    data_count = table_data.count()
    total_pages = math.ceil(data_count / page_size) or 1
    st.write(f"Total number of rows: {data_count}")
    bottom_menu = st.columns((2, 4, 2))
    active_page = st.session_state[pagination_btn_state_name]["current_page"]
    offset = st.session_state[pagination_btn_state_name]["offset"]
    
    def get_data(page_size, offset_rows=0):
        data = table_data.limit(page_size,offset=offset_rows)
        return data.collect()

    def change_page(state_name, btn_type, last_page):
        current_page = st.session_state[state_name]["current_page"]
        
        if (btn_type == "prev") and (current_page > 1):
            st.session_state[state_name]["current_page"] = current_page - 1
            current_page = st.session_state[state_name]["current_page"]   
            offset = (current_page * page_size) - page_size
            st.session_state[state_name]["offset"] = offset
        elif (btn_type == "next") and (current_page < last_page):
            st.session_state[state_name]["current_page"] = current_page + 1
            current_page = st.session_state[state_name]["current_page"]   
            offset = (current_page * page_size) - page_size
            st.session_state[state_name]["offset"] = offset
       

    with bottom_menu[2]:
            pass
            # batch_size = st.selectbox("Page Size", options=[25, 50, 100])
    with bottom_menu[1]:
            btn_col= st.columns([1,2,1])
            with btn_col[0]:
                prev = st.button("Prev", on_click= change_page, args=[pagination_btn_state_name, "prev",total_pages])
            with btn_col[1]:
                
                st.write(f"Page **{active_page}** - of -  **{total_pages}**")
            with btn_col[2]:
               next =  st.button("Next", on_click= change_page, args=[pagination_btn_state_name, "next", total_pages])
            
    with bottom_menu[0]:
            pass
            
    data_to_show = get_data(page_size=page_size, offset_rows=offset)
    
    
    with data_container:
        if custom_table_config["show"]:
            if custom_table_config["table_type"] == "team":
                for item in data_to_show:
                    id_key = custom_table_config["id_key"]
                    team_name_key = custom_table_config["name_key"]
                    value_key = custom_table_config["value_key"]
                    # st.write(id_key, item)
                    team_card(
                        team_id=item[id_key],
                        team_name=item[team_name_key],
                        param_value=item[value_key],
                        param_name=value_key
                    )
            elif custom_table_config["table_type"] == "player":
                for item in data_to_show:
                    id_key = custom_table_config["id_key"]
                    team_name_key = custom_table_config["name_key"]
                    value_key = custom_table_config["value_key"]
                    player_card(
                        id=item[id_key],
                        name=item[team_name_key],
                        param_value=item[value_key],
                        param_name=value_key
                    )
        else:
            data_container.dataframe(data_to_show, use_container_width=dataframe_options["full_width"], hide_index=dataframe_options["hide_index"])
    # st.write("Active page", active_page, st.session_state[pagination_btn_state_name])