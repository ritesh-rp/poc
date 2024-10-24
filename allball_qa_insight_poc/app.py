import hmac
import streamlit as st
st.set_page_config(layout="wide")
from player import player_df
from player import display_charts,scoring_pattern_view,efficiency_matrix_view,shooting_accuracy_view
from player import player_df, display_charts
from player import display_charts,display_all_player_data
from history_trends.player_milestones import player_milestone_view
from history_trends.highest_lowest_scores import player_team_overall_score_view
from history_trends.winning_loosing_streak import winning_losing_streak_view
from history_trends.team_scoring_trends import scoring_trend_view
from  history_trends.team_playing_styles import playing_style_trend_view



from snowflake_session import create_snowflake_session
from teams.teams_graph_query import  startPlotingData



def check_password():
    """Returns `True` if the user had a correct password."""

    def login_form():
        """Form with widgets to collect user information"""
        with st.form("Credentials"):
            st.text_input("Username", key="username")
            st.text_input("Password", type="password", key="password")
            st.form_submit_button("Log in", on_click=password_entered)

    def password_entered():
        """Checks whether a password entered by the user is correct."""
        if st.session_state["username"] in st.secrets[
            "passwords"
        ] and hmac.compare_digest(
            st.session_state["password"],
            st.secrets.passwords[st.session_state["username"]],
        ):
            st.session_state["password_correct"] = True
            del st.session_state["password"]  # Don't store the username or password.
            del st.session_state["username"]
        else:
            st.session_state["password_correct"] = False

    # Return True if the username + password is validated.
    if st.session_state.get("password_correct", False):
        return True

    # Show inputs for username + password.
    login_form()
    if "password_correct" in st.session_state:
        st.write("😕 User not known or password incorrect")
    return False


if not check_password():
    st.stop()






session = create_snowflake_session()

PLAYER_SECTION = "player"
player_section_options = {
    "scoring_pattern" : "SCORING PATTERN",
    "efficiency_matrix": "Efficiency Matrix",
    "shooting_accuracy": "Shooting Accuracy"
}
TEAM_SECTION = "team"
HISTORY_TRENDS_SECTION = "history&trends"
history_trends_section_options = {
    "player_milestone" : "Player Milestones",
    "high_low_score": "High/Low Scores",
    "win_loss_streak": "Win/Loss Streak",
    "scoring_trend_view": "Team Scoring Trend",
    "playing_style_trend_view": "Team Playing style Trend"
}



# state setters
def set_history_trends_option(option):
    st.session_state["history_trend_selected_option"] = option

def set_player_option(option):
    st.session_state["player_selected_option"] = option

def set_active_section(section_name):
    st.session_state.active_session = section_name

# Set initial state
if 'active_section' not in st.session_state:
    st.session_state["active_section"] = PLAYER_SECTION
    
if 'history_trend_selected_option' not in st.session_state:
    set_history_trends_option(history_trends_section_options["player_milestone"])


if 'player_selected_option' not in st.session_state:
    set_player_option(player_section_options["scoring_pattern"])


def sidebar_options(type):
    if(type == PLAYER_SECTION):
        # st.sidebar.subheader("Show player stats options")
        # st.sidebar.header ("Please Filter Here:")

        btn_container = st.sidebar.container(border=True)
        with btn_container:
            st.subheader("")
            scoring_pattern = st.button("Scoring Pattern", use_container_width=True)
            efficiency_matrix = st.button("Efficiency Matrix", use_container_width=True)
            shooting_accuracy = st.button("Shooting Accuracy", use_container_width=True)
           
        if scoring_pattern:
            set_player_option(player_section_options["scoring_pattern"])
        elif efficiency_matrix:
            set_player_option(player_section_options["efficiency_matrix"])
        elif shooting_accuracy:
            set_player_option(player_section_options["shooting_accuracy"])
        
    if(type == TEAM_SECTION):
        st.sidebar.subheader("Show Team stats options")
    if(type == HISTORY_TRENDS_SECTION):
        btn_container = st.sidebar.container(border=True)
        with btn_container:
            st.subheader("")
            player_milestone = st.button("Player Milestones", use_container_width=True)
            high_low_score = st.button("High/Low Scores", use_container_width=True)
            win_loss_streak = st.button("Win/Loss Streak", use_container_width=True)
            scoring_trend_view = st.button("Team Scoring Trend", use_container_width=True)
            playing_style_trend_view = st.button("Team Playing Style Trend", use_container_width=True)
        if player_milestone:
            set_history_trends_option(history_trends_section_options["player_milestone"])
        elif high_low_score:
            set_history_trends_option(history_trends_section_options["high_low_score"])
        elif win_loss_streak:
            set_history_trends_option(history_trends_section_options["win_loss_streak"])
        elif scoring_trend_view:
            set_history_trends_option(history_trends_section_options["scoring_trend_view"])
        elif playing_style_trend_view:
            set_history_trends_option(history_trends_section_options["playing_style_trend_view"])
           


        
def main_content(type):
    # title
    if(type == PLAYER_SECTION):
        selected_btn = st.session_state["player_selected_option"]
        if selected_btn == player_section_options["scoring_pattern"]:
            scoring_pattern_view()
        elif selected_btn == player_section_options["efficiency_matrix"]:
            efficiency_matrix_view()
        elif selected_btn == player_section_options["shooting_accuracy"]:
            shooting_accuracy_view()


    elif(type == TEAM_SECTION):
        st.subheader("Show Team content")
    elif(type == HISTORY_TRENDS_SECTION):
        selected_btn = st.session_state["history_trend_selected_option"]
        if selected_btn == history_trends_section_options["player_milestone"]:
            player_milestone_view()
        elif selected_btn == history_trends_section_options["high_low_score"]:
            player_team_overall_score_view()
        elif selected_btn == history_trends_section_options["win_loss_streak"]:
            winning_losing_streak_view()
        elif selected_btn == history_trends_section_options["scoring_trend_view"]:
            scoring_trend_view()
        elif selected_btn == history_trends_section_options["playing_style_trend_view"]:
            playing_style_trend_view()
    else:
        st.title("Main Content will go here")
        st.write("Select a option from sidebar")


        



             
#  Add layout switching buttons
st.sidebar.write("## 📋 Select an option below:")
show_player_stats = st.sidebar.button('Player',use_container_width=True, on_click=set_active_section, args=[PLAYER_SECTION])
show_team_stats = st.sidebar.button(
    'Team',
    use_container_width=True,
    on_click=set_active_section, 
    args=[TEAM_SECTION]
)
show_history_and_trends = st.sidebar.button(
    'History & Trends',
    use_container_width=True,
    on_click=set_active_section, 
    args=[HISTORY_TRENDS_SECTION]
)

if show_player_stats:
    st.session_state['active_section'] = PLAYER_SECTION
if show_team_stats:
    st.session_state['active_section']= TEAM_SECTION
if show_history_and_trends:
    st.session_state['active_section'] = HISTORY_TRENDS_SECTION

# Change sidebar options based on button click

if st.session_state["active_section"] == PLAYER_SECTION:
    sidebar_options(PLAYER_SECTION)
            
elif st.session_state["active_section"] == TEAM_SECTION:
    sidebar_options("team")
    startPlotingData()
    
elif st.session_state["active_section"] == HISTORY_TRENDS_SECTION:
    sidebar_options(HISTORY_TRENDS_SECTION)

  
# Main Content Section
   
if st.session_state["active_section"] == PLAYER_SECTION:
    main_content(PLAYER_SECTION)
elif st.session_state["active_section"] == TEAM_SECTION:
    main_content(TEAM_SECTION)
elif st.session_state["active_section"] == HISTORY_TRENDS_SECTION:
    main_content(HISTORY_TRENDS_SECTION)





           
        
 
    