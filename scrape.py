from bs4 import BeautifulSoup, Comment
import pandas as pd
import requests
from stqdm import stqdm
import streamlit as st

prefix = 'https://baseball-reference.com'
start_url = prefix + '/leagues/'

def sewp_info_player(player_html):
    # find player information like name (located in span tags on baseball reference)
    # instead of taking a link as input, we want to limit the amount of requests we make.
    span_tags = player_html.find_all('span')
    # some of this could be off in different years not sure yets
    name = span_tags[5].text
    height = span_tags[7].text
    weight = span_tags[8].text
    birthday = span_tags[9].text
    home_town = span_tags[10].text
    # collecting this data in case someone downloads the output and wants to model it or something
    return name, height, weight, birthday, home_town

def find_player_links(yr_link_text, team_link_text):
    a_tags = BeautifulSoup(requests.get(start_url).text, features = 'lxml').find_all('a', href = True)
    yr_tags = BeautifulSoup(requests.get(prefix + [tag['href'] for tag in a_tags if tag.text == yr_link_text][0]).text, features = 'lxml').find_all('a', href = True)
    team_links = [prefix + tag['href'] for tag in yr_tags if tag.text == team_link_text]
    team_link = ''
    # error message if team not found
    # make this same sort of error message for the year link!
    if len(team_links) < 1:
        st.error(f'TeamNotFound Error: "{team_link_text}" could not be found. Refresh the page, check spelling and try again.')
        st.stop()
    else:
        team_link = team_links[0]

        team_tags = BeautifulSoup(requests.get(team_link).text, features = 'lxml').find_all('a', href = True)
        player_links = [prefix + link['href'] for link in team_tags if '/players/' in link['href']]

        split_links = []
        for link in player_links:
            a_tags = BeautifulSoup(requests.get(link).text, features= 'lxml').find_all('a', href = True)
            split_link = [prefix + link['href'] for link in a_tags if link.text == yr_link_text]

        # some players that it finds do not have split statistics, skip those with this branch
            if len(split_link) > 0:
                split_links.append(split_link[0])
            
        split_links = split_links[:-16] # avoid links we do not need (make sure at some point we are not missing players)
        return split_links

# once we have the links, we will scrape data from those links
# we should collect base running data as well later on probably
def find_split_data(player_links, year, team):
    data_frames = []
    st.text(f'Collecting player data from the {year} {team}...')
    for player in stqdm(player_links):
        soup = BeautifulSoup(requests.get(player).text, features = 'lxml')
        name, height, weight, birthday, home_town  = sewp_info_player(soup)
        # lefty righty split data
        df = pd.read_html([x for x in soup.find_all(string=lambda text: isinstance(text, Comment)) if 'id="plato"' in x][0])[0] # platoon split table in the hmtl comments can't hide from me
        df.reset_index(inplace= True)
        df = df.apply(pd.to_numeric, errors = 'coerce').combine_first(df)
        # add the sewp info columns
        df['Name'] = name
        # name is the only consistent one for now, look into it more later to add columns below
        # df['Height'] = height
        # df['Weight'] = weight
        # df['Birthday'] = birthday
        # df['Home-Town'] = home_town
        data_frames.append(df)
    st.success(f'\nData Collected from {year} {team}!')
    return data_frames
        
# collect everything we need with mlb within this one function for readability on app.py page
def get_team(year, team):
    split_links = find_player_links(year, team)
    data = find_split_data(split_links, year, team)
    return data