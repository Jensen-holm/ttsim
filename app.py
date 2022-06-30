# from bs4 import BeautifulSoup
# import requests
import streamlit as st
from objects import Team
import scrape
import game_functions
from streamlit_option_menu import option_menu

# theme not working on git hub and actual app, but it is on local app. fix this.

# title and stuff
st.set_page_config(page_title = 'Ball.Sim', page_icon = '⚾️')
st.title('Ball.Sim')
st.write('\nCreated by Jensen Holm')

# get rid of streamlit option menu stuff
st.markdown(""" <style>
#MainMenu {visibility: hidden;}
footer {visibility: hidden;}
</style> """, unsafe_allow_html=True)

# get list of all teams ever to put into the select box, so when user types a team, it suggests closest team
# bbref_leagues_tags = BeautifulSoup(requests.get('https://baseball-reference.com/leagues').text, features = 'lxml').find_all('a', href = True)
# years = [link.text for link in bbref_leagues_tags if int(link.text) >= 1800]


# select which functinality to use (make this a variable in the simulation function)
# functionality = st.selectbox('Choose Functionality', ('Base','Situational','Lineup Optimization'))
functionality_bar = option_menu(menu_title = None, options = ['Base', 'Situational', 'Lineup Opt.', 'Examples'], icons = None, orientation = 'horizontal')

# user input drop down bars
if functionality_bar != 'Examples':
    team1 = st.text_input('Enter Team (ex: 2001 Seattle Mariners)').title().strip()
    team2 = st.text_input('Enter Team (ex: 1927 New York Yankees)').title().strip()
    # parse user input
    year_1, team1_name = team1[:4], team1[5:].strip()
    year_2, team2_name = team2[:4], team2[5:].strip()

if functionality_bar == 'Base':
    lineup_settings = st.selectbox('Lineup Settings', ('Manual', 'Automatic'))
    num_sims = st.slider('Number of Simulations', min_value = 2, max_value = 1620)
    
if functionality_bar == 'Situational':
    inning_options = [1, 1.5, 2, 2.5, 3, 3.5, 4, 4.5, 5, 5.5, 6, 6.5, 7, 6.5, 7, 7.5, 8, 8.5, 9, 9.5]
    inning = st.selectbox('Inning', (inning_options))
   
if functionality_bar == 'Lineup Optimization':
    opp_pitcher = st.selectbox('Opposing Pitcher',('Working on this'))
    
if functionality_bar == 'Examples':
    st.header("Fun things to explore")
    st.markdown("-  Who would've won the (insert year here) World Series if they played a 100 game series?")
    st.markdown("-  How many home runs would 2004 Barry Bonds have hit if he played 162 games against bad pitching?")
    st.markdown("-  How dominant would Jacob Degrom be agianst teams from the dead ball era?")
    

init_button = st.button('Go', help = 'Begin Simulation with the above settings (ignore if on examples page)')

if init_button:
    # when init button is pressed, collect data and simulate games
    # allow users to download play by play data in csv file
    # also visualize metrics in the app with st.metric()

    data1 = scrape.get_team(year_1, team1_name)
    data2 = scrape.get_team(year_2, team2_name)

    team1 = Team(team1_name, year_1, data1, lineup_settings)
    team2 = Team(team2_name, year_2, data2, lineup_settings)


# add a donate button in the footer so people can send money to my paypal
# as well as documentation, and disclaimers
st.write('[Twitter](https://twitter.com/JensenH_) [GitHub](https://github.com/Jensen-holm) [Linkedin](https://www.linkedin.com/in/jensen-holm-3584981bb/) [Donate](https://www.paypal.com/donate/?business=HPLUVQJA6GFMN&no_recurring=0&currency_code=USD)')
st.write('[Disclaimers, Documentation, and Code](https://github.com/Jensen-holm/sports-sim-app)')
st.write('Data Credit: [Sports Reference](https://Sports-reference.com)')
