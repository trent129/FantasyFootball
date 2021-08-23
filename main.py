import pandas as pd
import requests
import configparser
import os
import json

config = None

def init_config():
    global config
    config = configparser.RawConfigParser()
    config.read(os.path.abspath(os.path.join(".", "properties.ini")))

def main():
    init_config()
    global config

    espn_config = config['ESPN_CONFIG']
    
    #Input League Data
    league_id = espn_config['league_id']
    season=2020
    week=int(20)
    team_count=16
    espn_s2 = espn_config['espn_s2']
    swid = espn_config['swid']

    #url for the request
    url = 'https://fantasy.espn.com/apis/v3/games/ffl/seasons/' + \
          str(season) + '/segments/0/leagues/' + str(league_id)

    #API request to  private sites, get the swid and espn_s2   
    # r = requests.get(url,"view=mTeam",
    # cookies={"swid": swid,  "espn_s2": espn_s2})

    # results = json.dumps(r.json(), indent=1)

    with open('sample_response.json') as f:
        results = json.load(f)

        teams_df = pd.DataFrame({
            'Team': [team['location'] + ' ' + team['nickname'] for team in results['teams']],
            'FAABSpent': [100 - team['transactionCounter']['acquisitions'] for team in results['teams']],
            'Moves': [team['transactionCounter']['acquisitions'] for team in results['teams']]
        })

        teams_df.to_csv(f'FAAB_{season}_Week_{str(16)}', index=False)
        

if __name__ == "__main__":
    main()