import numpy as np
import pandas as pd
import gc
import math
import matplotlib.pyplot as plt
import tri_code_dict as tcd
import feature_creation

def main():
	path = "output/nba_lines_2007-2019.csv"
	vegas = pd.read_csv(path)
	vegas = vegas[['Season','1st','2nd', '2H', '3rd','4th', 'Close', 'Date', 'Final', 'ML', 'Open', 'Rot', 'Team','VH']]

	vegas = preprocessing(vegas)
	num_games = int(len(vegas)/2)

	l = ['Team1','Team2']
	l_teams = np.tile(l,num_games)
	vegas.loc[:,'Teams'] = l_teams

	new_vegas = pd.DataFrame(vegas.values.reshape(-1,30),columns=[
		'SeasonA','1stA','2ndA', '2HA', '3rdA','4thA', 'CloseA', 'DateA', 'FinalA', 'MLA', 'OpenA', 'RotA', 'TeamA','VHA','TeamsA','SeasonB','1stB','2ndB', '2HB', '3rdB','4thB', 'CloseB', 'DateB', 'FinalB', 'MLB', 'OpenB', 'RotB', 'TeamB','VHB','TeamsB'
		])

	del vegas
	gc.collect()
  
	vegas = more_pp(new_vegas)
	del new_vegas
	gc.collect()

	vegas = line_adjust(vegas)
  
	vegas = fix_dates(vegas)

	vegas=vegas.dropna(subset=['ActualDiff'])
	vegas = vegas_mae(vegas)
	print("Vegas Opening accuracy" + str(vegas['Open_MAE'].mean()))
	print("Vegas Closing accuracy"+str(vegas['Close_MAE'].mean()))
	print("Vegas Total Opening accuracy" + str(vegas['OpenTot_MAE'].mean()))
	print("Vegas Total Closing accuracy"+ str(vegas['CloseTot_MAE'].mean()))
	mean_err = vegas.groupby(['Season'])['Open_MAE','Close_MAE','OpenTot_MAE','CloseTot_MAE'].mean().reset_index()
	return vegas


def compare_odds():
	vegas = format()
	train, feats, df = feature_creation.main(list(range(2011,2020)))
	train['points'] = train['points_x'] + train['points_y']
	train['temp_game_id'] = train['game_id'].str[4:] + train['points'].astype(str) +abs(train['target']).astype(str)

	new_df = pd.merge(train,vegas, on=['temp_game_id'])
	return new_df



def format():
	path = "output/nba_lines_2007-2019.csv"
	master_df = pd.read_csv(path)
	master_df = preprocessing(master_df)
	num_games = int(len(master_df)/2)
	l = ['Team1','Team2']
	l_teams = np.tile(l,num_games)
	master_df.loc[:,'Teams'] = l_teams

	new_vegas = pd.DataFrame(master_df.values.reshape(-1,30),columns=[
		'SeasonA','1stA','2ndA', '2HA', '3rdA','4thA', 'CloseA', 'DateA', 'FinalA', 'MLA', 'OpenA', 'RotA', 'TeamA','VHA','TeamsA','SeasonB','1stB','2ndB', '2HB', '3rdB','4thB', 'CloseB', 'DateB', 'FinalB', 'MLB', 'OpenB', 'RotB', 'TeamB','VHB','TeamsB'
		])

	del master_df
	gc.collect()
	master_df = more_pp(new_vegas)
	del new_vegas
	gc.collect()
	master_df = line_adjust(master_df)
	master_df = fix_dates(master_df)
	

	master_df = master_df.loc[master_df['Season']>2010]
	#dropcols=[]
	dropcols = ['CloseA','OpenA','OpenB','OpenB','2HA','DateA','CloseB']
	master_df = master_df.drop(columns=dropcols)

	master_df = fix_teams(master_df)

	master_df['winning_name'] = np.where(master_df['ActualDiff']>0,master_df['TeamA'],master_df['TeamB'])
	master_df['losing_name'] = np.where(master_df['ActualDiff']<0,master_df['TeamA'],master_df['TeamB'])

	master_df['wn_copy'] = master_df['winning_name'].str.lower().str.replace(" ","")
	master_df['ln_copy'] = master_df['losing_name'].str.lower().str.replace(" ","")

	master_df['wn_copy2'] = master_df['wn_copy'].str[:4]
	master_df['wn_copy3'] = master_df['wn_copy'].str[-4:]
    
	master_df['ln_copy2'] = master_df['ln_copy'].str[:4]
	master_df['ln_copy3'] = master_df['ln_copy'].str[-4:]

	master_df['temp_game_id'] = master_df['Date'].str[-2:] +  master_df['wn_copy2'] + master_df['wn_copy3'] + master_df['ln_copy2']  + master_df['ln_copy3'] + master_df['ActualTotal'].astype(int).astype(str) +abs(master_df['ActualDiff']).astype(int).astype(str)


	return master_df

	#master_df.to_csv("output/vegas_formatted.csv")

def add_ids(df):
	df['wn_copy'] = df['winning_name'].str.replace('\n\t\t\t','').str.replace(' ','').str.lower()
	df['ln_copy'] = df['losing_name'].str.replace('\n\t\t\t','').str.replace(' ','').str.lower()

	df['wn_copy2'] = df['wn_copy'].str[:4]
	df['wn_copy3'] = df['wn_copy'].str[-4:]

	df['ln_copy2'] = df['ln_copy'].str[:4]
	df['ln_copy3'] = df['ln_copy'].str[-4:]

def fix_teams(df):
	teamnames = tcd.city_to_all()
	df['TeamA'] = df['TeamA'].map(teamnames)
	df['TeamB'] = df['TeamB'].map(teamnames)
	return df




def vegas_mae(df):
	df['Open_MAE'] = df.apply(lambda x: mae(x.ProjDiffOpen, x.ActualDiff), axis=1)
	df['Close_MAE'] = df.apply(lambda x: mae(x.ProjDiffClose, x.ActualDiff), axis=1)
	df['OpenTot_MAE'] = df.apply(lambda x: mae(x.OpeningTotal, x.ActualTotal), axis=1)
	df['CloseTot_MAE'] = df.apply(lambda x: mae(x.ClosingTotal, x.ActualTotal), axis=1)
	return df


def mae(y_pred, y):
	return np.abs(y_pred - y)


def fix_dates(df):
	df = df.dropna(subset=['DateA'])
	dates = df['DateA'].values
	seasons = df['Season'].values
	assert(len(dates)==len(seasons))
	assert(len(dates)==len(df))

	fdates=[]
	for idx,d in enumerate(dates):
		d = str(d)
		month=d[:-2]
		day=d[-2:]
		season = seasons[idx]
  #  print(month)
		if int(month)>=9:
			season-=1
		format_date = str(month)+'-'+str(day)+'-'+str(season)
		fdates.append(format_date)

	fdate_series = pd.Series(fdates, name='Date')

	df=df.reset_index(drop=True)
	df['Date'] = fdate_series.copy()
	return df



def line_adjust(df):
	df['ActualTotal'] = df['FinalA'].copy() + df['FinalB'].copy()
	df['OpeningTotal'] = df[['OpenA','OpenB']].max(axis=1)
	df['ClosingTotal'] = df[['CloseA','CloseB']].max(axis=1)
	df['TempOpeningLine'] = df[['OpenA','OpenB']].min(axis=1)
	df['TempClosingLine'] = df[['CloseA','CloseB']].min(axis=1)

	df['ProjDiffOpen'] = np.where(df['OpenA']==df['TempOpeningLine'], df['OpenA'], -1*df['OpenB'])
	df['ProjDiffClose'] = np.where(df['CloseA']==df['TempClosingLine'], df['CloseA'], -1*df['CloseB'])

	df = df.drop(columns=['TempOpeningLine','TempClosingLine'])
	df['ActualDiff'] = df['FinalA'].copy() - df['FinalB'].copy()

	return df






def scrape(seasons):
	master_df = None

	for season in seasons:
		season_start = str(season)
		season_end = str(season+1)[-2:]
		season_str = season_start + '-' +season_end
		load_path = "./vegas_lines/nba_basketball_" +season_str+".csv"
		season_df = pd.read_csv(load_path)
		season_df['Season'] = str(season+1)
		season_df = season_df[['Season','1st','2nd', '2H', '3rd','4th', 'Close', 'Date', 'Final', 'ML', 'Open', 'Rot', 'Team','VH']]
		season_df['Season'] = season_df['Season'].copy().astype(str)
		if master_df is not None:
			master_df = pd.concat([master_df,season_df],axis=0)
		else: master_df = season_df
	master_df.to_csv('./output/nba_lines_2007-2019.csv',index=None)



def preprocessing(df):
	df = df.copy().replace('pk','0')
	df = df.copy().replace('p','0')
	df = df.copy().replace('PK','0')
	df = df.copy().replace('197.5u10','197.5')

	return df


def more_pp(df):
	df = df.drop(columns=['TeamsA','TeamsB','DateB','VHB','RotA','RotB','SeasonB'])
	df = df.rename(columns={'SeasonA':'Season'})
	df = df.loc[df['2HA']!='NL']
	df = df.loc[df['MLA']!='NL']
	df = df.loc[df['2HB']!='NL']
	df = df.loc[df['MLB']!='NL']
	df = df.loc[df['OpenA'] != 'NL']
	df = df.loc[df['OpenB'] != 'NL']
	df = df.loc[df['CloseA'] != 'NL']
	df = df.loc[df['CloseB'] != 'NL']
	str_cols = ['Season','TeamA','TeamB','DateA','VHA']
	for col in list(df):
		if col not in str_cols:
			df[col] = df[col].copy().astype(float)
	return df






if __name__ == "__main__":
	seasons = list(range(2007,2019))
	main()