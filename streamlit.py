import streamlit as st
import pandas as pd
from dotenv import load_dotenv
from riotwatcher import LolWatcher

RIOT_API_KEY = 'RGAPI-d143d510-85b6-406d-8c91-3a9a311b0295'

load_dotenv(verbose=True)
lol_watcher = LolWatcher(RIOT_API_KEY)
my_region = 'kr'

def get_summoner_data_by_name(nickname):
    summoner_json = lol_watcher.summoner.by_name(my_region, nickname)
    return summoner_json

def get_summoner_data_by_puuid(by_puuid):
    summoner_json = lol_watcher.summoner.by_puuid(my_region, by_puuid)
    return summoner_json

def get_matchlist_data(puuid):
    matchlist_json = lol_watcher.match.matchlist_by_puuid(my_region, puuid)
    return matchlist_json

def get_match_data(matchid):
    match_json = lol_watcher.match.by_id(my_region, matchid)
    return match_json

def get_rank_tier(summoner_id):
    rank_tier_json = lol_watcher.league.by_summoner(my_region, summoner_id)
    return rank_tier_json

def get_match_time(time_duration):
    minutes = time_duration // 60
    seconds = time_duration % 60
    return minutes, seconds

def main():
    st.title("League of Legends")

    user_name = st.text_input("Enter user name:")
    if st.button("Get Match Data"):
        summoner_json_use_name = get_summoner_data_by_name(user_name)
        rank_tier_json = get_rank_tier(summoner_json_use_name['id'])
        # st.json(rank_tier_json)

        if rank_tier_json:
            tier = rank_tier_json[0]['tier']
            rank = rank_tier_json[0]['rank']
            wins = rank_tier_json[0]['wins']
            losses = rank_tier_json[0]['losses']
            win_rate = round(wins/(wins+losses)*100, 2)

            st.text(f"Tier: {tier}, Rank: {rank}")
            st.text(f"wins: {wins}, losses: {losses}")
            st.text(f"Win Rate {win_rate}%")

        puuid = summoner_json_use_name['puuid']
        matchlist_json = get_matchlist_data(puuid)
        for match_id in matchlist_json:
            st.subheader(f"{match_id}")
            match_json = get_match_data(match_id)

            time_duration = match_json['info']['gameDuration']  # 게임 진행 시간
            minutes, seconds = get_match_time(time_duration)
            st.text(f"This match duration is {minutes} minutes and {seconds} seconds")

            # 매치 데이터(포지션/챔피언/킬/데스/어시/CS 등)
            st.subheader("MatchData")
            participants = match_json['info']['participants']
            match_data = []
            for participant in participants:

                team_id = participant['teamId']  # 팀 id
                summoner_name = participant['summonerName']  # 소환사명
                puuid = participant['puuid']
                summoner_1_id = participant['summoner1Id']  # 소환사 주문1
                summoner_2_id = participant['summoner2Id']  # 소환사 주문2
                team_position = participant['teamPosition']  # 포지션
                champion_id = participant['championId']  # 챔피언 id
                kills = participant['kills']  # 킬
                deaths = participant['deaths']  # 데스
                assists = participant['assists']  # 어시스트
                kda = participant['challenges']['kda']  # kda
                neutral_minions_killed = participant['neutralMinionsKilled']  # 중립 미니언 처치(정글몹)
                total_minions_killed = participant['totalMinionsKilled']  # 미니언 처치
                if team_position == 'UTILITY':
                    team_position = 'SUPPORT'

                match_data.append({
                    "Team ID": team_id,
                    "Summoner Name": summoner_name,
                    "puuID": puuid,
                    "Summoner 1 ID": summoner_1_id,
                    "Summoner 2 ID": summoner_2_id,
                    "Team Position": team_position,
                    "Champion ID": champion_id,
                    "Kills": kills,
                    "Deaths": deaths,
                    "Assists": assists,
                    "KDA": kda,
                    "Neutral Minions Killed": neutral_minions_killed,
                    "Total Minions Killed": total_minions_killed
                })
            match_df = pd.DataFrame(match_data)
            st.dataframe(match_df)

            # 팀 데이터
            st.subheader("TeamData")
            teams = match_json['info']['teams']
            team_data = []
            for team in teams:
                team_id = team['teamId']  # 팀 id
                first_blood = team['objectives']['champion']['first']  # 첫 킬
                first_tower = team['objectives']['tower']['first']  # 첫 타워
                first_inhibitor = team['objectives']['inhibitor']['first']  # 첫 억제기
                first_baron = team['objectives']['baron']['first']  # 첫 바론
                first_dragon = team['objectives']['dragon']['first']  # 첫 드래곤
                first_rift_herald = team['objectives']['riftHerald']['first']  # 첫 전령
                win = team['win']  # 승패
                bans = team['bans']  # 밴 목록

                team_data.append({
                    "Team ID": team_id,
                    "First Blood": first_blood,
                    "First Tower": first_tower,
                    "First Inhibitor": first_inhibitor,
                    "First Baron": first_baron,
                    "First Dragon": first_dragon,
                    "First Rift Herald": first_rift_herald,
                    "Win": win,
                    "Bans": bans
                })
            team_df = pd.DataFrame(team_data)
            st.dataframe(team_df)

            # if st.button("Show_match_json"):
            #     st.json(match_json)

    if st.button("Show_summoner_json"):
        summoner_json_use_name = get_summoner_data_by_name(user_name)
        st.json(summoner_json_use_name)


# Run the app
if __name__ == "__main__":
    main()
