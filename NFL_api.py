import requests
import pandas as pd
import numpy as np


def api_get_weekly_schedule(year, season_type, week_num):
    string = 'http://api.sportradar.us/nfl-t1/%i/%s/%i/schedule.json?api_key=jdmq6nfne2a7ucg6g5jkvsz7' %(year, season_type, week_num)
    answer = requests.get(string)
    test  = answer.json()
    return test
    
    
    
def flatten_schedule(dict_in):
    n=0
    weeks = []
    key1 = 'games'
    for n in range(0,len(dict_in[key1])):
        week_row = dict_in[key1][n].copy()
        del week_row['venue']
        del week_row['weather']
        del week_row['away_rotation']
        del week_row['home_rotation']
        week_row['surface'] = dict_in[key1][n]['venue']['surface']
        week_row['temperature'] = dict_in[key1][n]['weather']['temperature']
        week_row['condition'] = dict_in[key1][n]['weather']['condition']
        week_row['week'] = dict_in['number']
        weeks.append(week_row)
    df_out = pd.DataFrame(weeks)
    return df_out
    
    
    
def api_get_injuries(year,season_type,week,home_team,away_team):
    string = 'http://api.sportradar.us/nfl-t1/%i/%s/%i/%s/%s/injuries.json?api_key=jdmq6nfne2a7ucg6g5jkvsz7' %(year, season_type, week, home_team, away_team)
    answer = requests.get(string)
    dict_out  = answer.json()
    return dict_out
    
    
    
def flatten_injuries(dict_in):
    i=0
    n=0
    m=0
    list_dicts = []
    
    for key1 in dict_in.keys():
        if (type(dict_in[key1]) == dict):
            for key2 in dict_in[key1].keys():
                #print key2
                if (type(dict_in[key1][key2]) == list):
                    for i in range(0,len(dict_in[key1][key2])):
                        #print dict_in[key1][key2][i]
                        #df_out = pd.DataFrame(dict_in[key1][key2][i])
                        if (type(dict_in[key1][key2][i]) == dict):
                            for key3 in dict_in[key1][key2][i].keys():
                                #print key3
                                if (type(dict_in[key1][key2][i][key3]) == list):
                                    #print dict_in[key1][key2][i][key3]
                                    for n in range(0,len(dict_in[key1][key2][i][key3])):
                                        if (type(dict_in[key1][key2][i][key3][n]) == dict):
                                            #print type(dict_in[key1][key2][i][key3][n])
                                            dict1 = dict_in[key1][key2][i][key3][n].copy()
                                            #print 'dict 1 is', dict1
                                            dict2 = dict_in[key1][key2][i].copy()
                                            #print 'dict 2 is '
                                            del dict2[key3]
                                            row = dict(dict2, **dict1)
                                            #print 'row is', row
                                            dict3 = dict_in[key1].copy()
                                            #print dict3
                                            del dict3[key2]
                                            list_dicts.append(dict(dict3, **row))
                                            m += 1
    dfOut = pd.DataFrame(list_dicts)
    game_id = pd.Series([dict_in['id']]*len(dfOut.index), name = 'game_id')
    dfOut = pd.concat([game_id,dfOut], axis=1)
    return dfOut

    
    
def api_get_stats(year, season_type, week_num, away_team, home_team):
    string = 'http://api.sportradar.us/nfl-t1/%i/%s/%i/%s/%s/statistics.json?api_key=jdmq6nfne2a7ucg6g5jkvsz7' %(year, season_type, week_num, away_team, home_team)
    answer = requests.get(string)
    test  = answer.json()
    return test
    
    
    
def flatten_game_stats(dict_in, stat_key):
    i=0
    n=0
    m=0
    player_stats = []
    team_stats = []
    
    for key1 in dict_in.keys():
        if (type(dict_in[key1]) == dict):
            for key2 in dict_in[key1].keys():
                if (type(dict_in[key1][key2]) == dict):
                    for key3 in dict_in[key1][key2][stat_key].keys():
                        if (key3 == 'players'):
                            for n in range(0,len(dict_in[key1][key2][stat_key][key3])):
                                player_row = dict_in[key1][key2][stat_key][key3][n].copy()
                                player_row['market'] = dict_in[key1]['market']
                                player_row['team_name'] = dict_in[key1]['name']
                                player_stats.append(player_row)
                                n+=1
                        elif (key3 == 'team'):
                            team_row = dict_in[key1][key2][stat_key][key3]
                            team_row['market'] = dict_in[key1]['market']
                            team_row['team_name'] = dict_in[key1]['name']
                            team_stats.append(team_row)
                        
    player_df_out = pd.DataFrame(player_stats)
    team_df_out = pd.DataFrame(team_stats)
    
    game_id_players = pd.Series([dict_in['id']]*len(player_df_out.index), name = 'game_id')
    game_id_team = pd.Series([dict_in['id']]*len(team_df_out.index), name = 'game_id')
    
    scheduled_players = pd.Series([dict_in['scheduled']]*len(player_df_out.index), name = 'scheduled')
    scheduled_team = pd.Series([dict_in['scheduled']]*len(team_df_out.index), name = 'scheduled')
    
    player_df_out = pd.concat([game_id_players, scheduled_players, player_df_out], axis=1)
    team_df_out = pd.concat([game_id_team, scheduled_team, team_df_out], axis = 1)
    
    return player_df_out,team_df_out
    
