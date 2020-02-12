from sportsreference.nba.teams import Teams
from sportsreference.nba.boxscore import Boxscore
import pandas as pd
from datetime import datetime, timedelta
import tri_code_dict 
import nba_scrape
import feature_creation
import get_info
from tqdm import tqdm
import numpy as np
import model

def main():
	try:
		schedule_df = pd.read_csv('output/schedule.csv')
	except: 
		nba_scrape.main()
		schedule_df = pd.read_csv('output/schedule.csv')

	update_games()



	date_str = get_formatted_date()
	todays_games = schedule_df[schedule_df['BoxscoreIndex'].str.contains(date_str)==True]
	
	today,layout = fill_box(todays_games)

	#print(layout[['team_x','team_y']])
	prediction,prediction2 = predict(today)

	layout['ProjDiff'] = prediction
	layout['ProjTot'] = prediction2

	print(layout[['team_x','ProjDiff','team_y','ProjTot']])



def predict(today):
	#drop the excess
	path = 'output/train.csv'
	path_tot = 'output/train_tot.csv'
	
	model_lgb,X,y,train = model.train(path)
	train = train.drop(columns=['Unnamed: 0','target'])
	X = X.drop(columns = ['Unnamed: 0'])
	model_lgb.fit(X, y)
	train_prediction = model_lgb.predict(train)

	model_lgb2 , X2,y2, train_tot = model.train(path_tot)
	train_tot  = train_tot.drop(columns=['Unnamed: 0','target'])
	X2= X2.drop(columns = ['Unnamed: 0'])
	model_lgb2.fit(X2, y2)
	train_prediction_tot = model_lgb2.predict(train_tot)



	today1 = today.drop(columns=['date_x','Season_x','BoxscoreIndex','HomeTeam_x','home_loc_x','date_y','Season_y','TeamName','DayOfSeason_y','HomeTeam_y','team_y','id_y','home_loc_y'])
	today1 = today1.drop(columns=['team_x','id_x','Sea_PF_x','Sea_PF_y','Sea_FT_x','Sea_FT_y','Sea_TO_x','Sea_TO_y'])

	prediction = model_lgb.predict(today1)
	prediction2 = model_lgb2.predict(today1)
	print(prediction)
	return prediction, prediction2

def fill_box(todays_games):
	train, feats, df=feature_creation.main(range(2011,2021))
	todays_games['season'] = todays_games['Season']
	todays_games = get_info.add_dos(todays_games)
	ctc = tri_code_dict.create_team_conversion()
	rev_ctc = dict([(value,key) for key, value in ctc.items()])
	todays_games['HomeTeam'] = todays_games['BoxscoreIndex'].str[-3:].map(rev_ctc)

	teams1 = todays_games.drop_duplicates(subset=['BoxscoreIndex'],keep='first')
	teams2 = todays_games.drop_duplicates(subset=['BoxscoreIndex'],keep='last')

	teams1['at_home_x'] = np.where(teams1['TeamName'].copy()==teams1['HomeTeam'],1,0)
	#should only need one home location
	#teams2['at_home_y'] = np.where(teams2['TeamName'].copy()==teams2['HomeTeam'],1,0)

	teams1['team_x'] = teams1['TeamName']
	teams1['rolling_x'] = teams1['rollingGames']

	teams2['team_y'] = teams2['TeamName']
	teams2['rolling_y'] = teams2['rollingGames']

	teams1['id_x'] = teams1['Season'].astype(str) +teams1['team_x'].str.lower().str.replace(" ","")
	teams2['id_y'] = teams2['Season'].astype(str) + teams2['team_y'].str.lower().str.replace(" ","")

	teams1 = teams1.drop(columns=['season','rollingGames','season_start','TeamName'])
	teams2 = teams2.drop(columns=['season','rollingGames','season_start'])

	todays_games = teams1.merge(teams2,on='BoxscoreIndex')

	#next steps
	#set index to home team
	#merge on home team
	#fill out featuers

	feats = feats.drop_duplicates(subset=['id'],keep='last')
	feats = feats.tail(30)

#taken care of above	
#	todays_games['id'] = todays_games['Season'].astype(str)+todays_games['TeamName'].str.lower().str.replace(" ","")
	
	feats = feats.set_index('id')
	
	feats1 = feats.loc[teams1['id_x']]
	feats2 = feats.loc[teams2['id_y']]

	feats1= feats1.reset_index()
	feats2 = feats2.reset_index()
	fncols_x =[]
	fncols_y = []
	fcols = list(feats1)
	for col in fcols:
		col +='_x'
		fncols_x.append(col)
	for col in fcols:
		col+='_y'
		fncols_y.append(col)

	feats1[fncols_x] = feats1[fcols]
	feats2[fncols_y] = feats2[fcols]

	feats1 = feats1.drop(columns=fcols)
	feats2 = feats2.drop(columns=fcols)

	feats1 = feats1.set_index('id_x')
	today_x = teams1.merge(feats1,on='id_x')

	today_y = teams2.merge(feats2,on='id_y')

	today = today_x.merge(today_y, on='BoxscoreIndex')

	print(today)
	print(list(today))
	return today, todays_games

	today = today.drop(columns=['date_x','date_y','Season_x','Season_y','DayOfSeason_y','BoxscoreIndex','HomeTeam_x','team_x','HomeTeam_y','team_y','home_loc_y','home_loc_x','TeamName'])

	return today, todays_games



#	today_feats = feats.loc[todays_games['id']]

	#test = pd.DataFrame(columns=list(train))
	#test['DayOfSeason_x'] = todays_games['DayOfSeason']






def update_games():
	#get what season we're in, season is defined by end year
	season = get_info.get_season()

	#get the box score data already pulled
	season_box = pd.read_csv('output/{}_boxscores.csv'.format(season))
	
	#get the schedule df
	schedule_df = pd.read_csv('output/schedule.csv')
	
	#find out when the last update was
	last_update = pd.to_datetime(season_box['date']).max()
	#find out waht day yesterday was 
	yesterday = pd.to_datetime(datetime.today()-timedelta(days=1))
	schedule_df['date'] = pd.to_datetime(schedule_df['date'])

	schedule_df = schedule_df.loc[(schedule_df['date']>last_update)]

	schedule_df = schedule_df.loc[(schedule_df['date']<=yesterday)]
	print(schedule_df)
	box_df = update_box(schedule_df)
	print(box_df)
	season_box = pd.concat([season_box,box_df],axis=0)
	season_box.to_csv('output/{}_boxscores.csv'.format(season),index=None)


def get_formatted_date():
	t = datetime.today().isoformat()
	year = t[:4]
	month = t[5:7]
	day =  t[8:10]
	return year+month+day



def update_box(schedule_df):

	tcd = tri_code_dict.create_team_conversion()
	box_df = None
	for index, row in tqdm(schedule_df.iterrows()):
		print(row)
		box_link = row['BoxscoreIndex']
		try:
			_df = Boxscore(box_link).dataframe
        
			if(tcd[row['TeamName']]==row['BoxscoreIndex'][-3:]):
				_df['home_rolling'] = row['rollingGames']
			else: _df['away_rolling'] = row['rollingGames']
			if box_df is not None:
				print (season)
				box_df = pd.concat([box_df,_df],axis=0)

        
			else: box_df = _df
        
		except: continue
      
	return box_df



if __name__ == "__main__":
  main()











