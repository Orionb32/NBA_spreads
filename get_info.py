import feature_creation
import pandas as pd
import numpy as np
import tri_code_dict
from datetime import datetime

def get_df(seasons):
	df = None
	tcd = tri_code_dict.create_team_conversion()
	schedule_df = pd.read_csv('output/schedule.csv')

	for s in seasons:
		path = 'output/{}_boxscores.csv'.format(str(s))
		_df = pd.read_csv(path)
		if df is not None:
	  		df = pd.concat([df,_df],axis=0)
		else: df = _df
	return df

def get_season():
	season = datetime.today().year
	if(datetime.today().month>=9): season+=1
	return season


def get_teams(df):
	#fixes missing team names and also gets a list of all team names... for fun...?
	df = df.copy().replace('Charlotte Bobcats','Charlotte Hornets')
	df = df.copy().replace('New Orleans Hornets','New Orleans Pelicans')
	df = df.copy().replace('New Jersey Nets','Brooklyn Nets')
	all_teams = list(set(list(df['winning_name'].values)+list(df['losing_name'].values)))
	teams=[]
	for t in all_teams:
		if '\n\t\t' not in t:
		  teams.append(t)
	print(len(teams))
	print(len(all_teams))
	print(teams)
	return df,teams


def add_season(df):
    # datetime
    df['date'] = pd.to_datetime(df['date'])
    
    df['month'] = df['date'].copy().dt.month.astype(int)
    df['year'] = df['date'].copy().dt.year.astype(int)
    df['season'] = df['year'].copy()
    df['season'] = np.where(df['month']>9, df['season']+1, df['season'])
    
    df = df.drop(columns=['month','year'])
    
    return df

def add_dos(df):
    
	df['season_start'] = df['season'].copy() - 1
	df['season_start'] = df['season_start'].copy().astype(str) + '-10-20'
    
	df['DayOfSeason'] = pd.to_datetime(df['date']) - pd.to_datetime(df['season_start'])
	df['DayOfSeason'] = df['DayOfSeason'].dt.days.astype(int)
    
	return df

def get_home_arenas(df):
	# get home, away, or neutral
	# will merge in later
	home_arenas = df.groupby(['id'])['location'].apply(pd.Series.mode).reset_index()
	home_arenas = home_arenas.drop(columns=['level_1'])
	home_arenas.head()
	return home_arenas
