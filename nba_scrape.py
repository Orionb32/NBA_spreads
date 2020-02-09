import numpy as np
import pandas as pd

from sportsreference.nba.teams import Teams
from sportsreference.nba.boxscore import Boxscore
from tqdm import tqdm
import tri_code_dict
from datetime import datetime


def main(seasons):
  
  schedule_df = season_scraper(seasons)
  schedule_df = pd.read_csv('output/schedule.csv')
  box_scraper(seasons, schedule_df)

def season_scraper(seasons):
  master_array = []
  schedule_df=None
  for season in tqdm(seasons): #tqdm shows progress bar
    try:
      season_team_list = Teams(str(season))
      for team in season_team_list:
        team_schedule = team.schedule
        team_season_array = []
        for game in team_schedule:
          boxscore = game.boxscore_index
          team_season_array.append([str(season),team.name,boxscore,game.date])
        team_season_df = pd.DataFrame(team_season_array,columns = ['Season','TeamName','BoxscoreIndex','date'])
        team_season_df['date'] = pd.to_datetime(team_season_df['date'])
        team_season_df = team_season_df.set_index('date')
        team_season_df['rollingGames'] = team_season_df['Season'].rolling('5D').count()
        
        if schedule_df is not None:
          schedule_df=pd.concat([schedule_df,team_season_df],axis=0)
        else: schedule_df=team_season_df
        #master_array.append([str(season),team.name,boxscore])
    
    except:
      print("didn't work")
      continue

  #schedule_df = pd.DataFrame(master_array, columns = ['Season','TeamName','BoxscoreIndex','rollingGames'])

  schedule_df.to_csv('output/schedule_test.csv',index=True)
  return schedule_df


def box_scraper(seasons, schedule_df):

  tcd = tri_code_dict.create_team_conversion()
  for season in seasons:

    season_df = schedule_df.loc[schedule_df.Season == season]

    season_df['date'] = pd.to_datetime(season_df['date'])
    today = pd.to_datetime(datetime.today())
    #print(season_df.head())
    box_df = None
    for index, row in tqdm(season_df.iterrows()):
      if(row['date'].year>today.year):
        print("passing over")
        continue
      elif(row['date'].year==today.year):
        if(row['date'].month>today.month):
          print("passing over")
          continue
        elif(row['date'].month==today.month):
          if(row['date'].day>=today.day):
            print('passing over')
            continue

      #print(row)
      box_link = row['BoxscoreIndex']
     #try:
      _df = Boxscore(box_link).dataframe
        
      if(tcd[row['TeamName']]==row['BoxscoreIndex'][-3:]):
        _df['home_rolling'] = row['rollingGames']
      else: _df['away_rolling'] = row['rollingGames']
      if box_df is not None:
        print (season)
        box_df = pd.concat([box_df,_df],axis=0,sort=False)

          #_df['rollingGames']= row['rollingGames']
      else: 

        box_df = _df
          #_df['rollingGames']= row['rollingGames']
      #except: continue
    

    box_df.to_csv('output/{}_boxscores.csv'.format(season),index=None)
  
  



if __name__ == "__main__":
  seasons = range(2011,2021)
  main(seasons)