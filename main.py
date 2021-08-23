from re import I
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

def save_response_to_json(response, file_name):
    """
    Saves the :response as a json file with :file_name
    """
    with open(f'{file_name}.json', 'w') as f:
        json.dump(response.json(), f)

def get_team_df(url, cookies, season, week):
    """
    Returns teams dataframe

    Currently pulling from json file during prototyping
    """
    # # API request to private sites, get the swid and espn_s2   
    # r = requests.get(url, "view=mTeam", cookies=cookies)

    # results = json.dumps(r.json(), indent=1)

    with open('sample_response.json') as f:
        results = json.load(f)

        df = pd.DataFrame({
            'teamId': [team['id'] for team in results['teams']],
            'Team': [team['location'] + ' ' + team['nickname'] for team in results['teams']],
            'FAABSpent': [100 - team['transactionCounter']['acquisitions'] for team in results['teams']],
            'Moves': [team['transactionCounter']['acquisitions'] for team in results['teams']]
        })

        df = df.set_index('teamId')

        return df

def get_matchup_df(url, cookies):
    """
    Returns matchup dataframe

    Currently pulling from json file during prototyping
    """
    # # API request to private sites, get the swid and espn_s2   
    # r = requests.get(url, "view=mMatchup", cookies=cookies)

    # results = json.dumps(r.json(), indent=1)

    with open('sample_matchup.json') as f:
        results = json.load(f)

        schedule = results['schedule']
        num_games = len(schedule)

        df = pd.DataFrame({
            'homeTeamId': [schedule[i]['home']['teamId'] for i in range(num_games) if schedule[i].get('away') is not None],
            'awayTeamId': [schedule[i]['away']['teamId'] for i in range(num_games) if schedule[i].get('away') is not None],
            'week': [schedule[i]['matchupPeriodId'] for i in range(num_games) if schedule[i].get('away') is not None],
            'PF': [schedule[i]['home']['totalPoints'] for i in range(num_games) if schedule[i].get('away') is not None],
            'PA': [schedule[i]['away']['totalPoints'] for i in range(num_games) if schedule[i].get('away') is not None]
        })

        return df

def main():
    init_config()
    global config

    espn_config = config['ESPN_CONFIG']
    
    #Input League Data
    league_id = espn_config['league_id']
    season = espn_config['season']
    week=int(espn_config['week'])
    cookies = {"swid": espn_config['swid'],  "espn_s2": espn_config['espn_s2']}

    # url for the request
    url = f'https://fantasy.espn.com/apis/v3/games/ffl/seasons/{str(season)}/segments/0/leagues/{str(league_id)}'

    teams_df = get_team_df(url, cookies, season, week)
    matchup_df = get_matchup_df(url, cookies)

    # Swap home and away columns and append to original dataframe
    swap = matchup_df.rename(columns={
        **dict(zip(['homeTeamId', 'PF'], ['awayTeamId', 'PA'])),
        **dict(zip(['awayTeamId', 'PA'], ['homeTeamId', 'PF']))
    })
    matchup_df = matchup_df.append(swap).sort_index(ignore_index=True)

    # # Uncomment these to save the files as csvs
    # teams_df.to_csv(f'FAAB_{season}_Week_{str(week)}.csv', index=False)
    # matchup_df.to_csv('scores.csv', index=False)
    
if __name__ == "__main__":
    main()