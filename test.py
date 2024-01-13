import json
from dotenv import load_dotenv
from riotwatcher import LolWatcher

load_dotenv(verbose=True)
lol_watcher = LolWatcher('RGAPI-d143d510-85b6-406d-8c91-3a9a311b0295')
my_region = 'kr'

def get_summoner_data(nickname):
    summoner_json = lol_watcher.summoner.by_name(my_region, nickname)
    return summoner_json

def get_matchlist_data(puuid):
    matchlist_json = lol_watcher.match.matchlist_by_puuid(my_region, puuid)
    return matchlist_json

def get_match(matchid):
    match_json = lol_watcher.match.by_id(my_region, matchid)
    return match_json

user_name = input("Enter your name: ")

summoner_json = get_summoner_data(user_name)
print(f"{summoner_json['name']}'s puuid is {summoner_json['puuid']}")
print(summoner_json)

# puuid = summoner_json['puuid']
# matchlist_data = get_matchlist_data(puuid)
# print()
# match_json = get_match(matchlist_data[0])
#
# with open('data.json', 'w') as json_file:
#     json.dump(match_json, json_file)

# for matchid in matchlist_data:
#     print(matchid)
#     match_json = get_match(matchid)
#     print(match_json)
#     with open('data.json', 'w') as json_file:
#         json.dump(match_json, json_file)
