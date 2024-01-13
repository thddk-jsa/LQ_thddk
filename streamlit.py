import streamlit as st
from dotenv import load_dotenv
from riotwatcher import LolWatcher

RIOT_API_KEY = 'RGAPI-d143d510-85b6-406d-8c91-3a9a311b0295'

load_dotenv(verbose=True)
lol_watcher = LolWatcher(RIOT_API_KEY)
my_region = 'kr'

def get_summoner_data(nickname):
    summoner_json = lol_watcher.summoner.by_name(my_region, nickname)
    return summoner_json

def get_matchlist_data(puuid):
    matchlist_json = lol_watcher.match.matchlist_by_puuid(my_region, puuid)
    return matchlist_json

def get_match_data(matchid):
    match_json = lol_watcher.match.by_id(my_region, matchid)
    return match_json

summoner_json = {}

def main():
    global summoner_json  # 전역 변수로 선언

    st.title("League of Legends Summoner Data Viewer")

    user_name = st.text_input("Enter your summoner name:")
    if st.button("Get Summoner Data"):
        summoner_json = get_summoner_data(user_name)
        st.json(summoner_json)

    puuid = st.text_input("Enter your puuid:")
    if st.button("Get Match List"):
        matchlist_json = get_matchlist_data(puuid)
        st.json(matchlist_json)

    match_id = st.text_input("Enter match id in Match List:")
    if st.button("Get Match Data"):
        match_json = get_match_data(match_id)
        st.json(match_json)

# Run the app
if __name__ == "__main__":
    main()
