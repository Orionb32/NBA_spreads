from sportsreference.nba.teams import Teams
from sportsreference.nba.boxscore import Boxscore
import pandas as pd
from datetime import datetime, timedelta
import tri_code_dict
import nba_scrape
import get_info
from tqdm import tqdm

def main():
	try:
		schedule_df = pd.read_csv('output/schedule.csv')
	except: 
		nba_scrape.main()
		schedule_df = pd.read_csv('output/schedule.csv')

	update_games()



	date_str = get_formatted_date()
	todays_games = schedule_df[schedule_df['BoxscoreIndex'].str.contains(date_str)==True]
	return todays_games
	print (todays_games)

def fill_box(todays_games):
	train, feats, df=feature_creation.main(range(2011,2021))
	todays_games['season'] = todays_games['Season']
	todays_games = get_info.add_dos(todays_games)
	ctc = tcd.create_team_conversion()
	rev_ctc = dict([(value,key) for key, value in ctc.items()])
	todays_games['HomeTeam'] = todays_games['BoxscoreIndex'].str[-3:].map(rev_ctc)

	teams1 = todays_games.drop_duplicates(subset=['BoxscoreIndex'],keep='first')
	teams2 = todays_games.drop_duplicates(subset=['BoxscoreIndex'],keep='last')

	teams1['at_home_x'] = np.where(teams1['TeamName'].copy()==teams1['HomeTeam'],1,0)
	teams2['at_home_y'] = np.where(teams2['TeamName'].copy()==teams2['HomeTeam'],1,0)

	teams1['team_x'] = teams1['TeamName']
	teams1['rolling_x'] = teams1['rollingGames']

	teams2['team_y'] = teams2['TeamName']
	teams2['rolling_y'] = teams2['rollingGames']

	teams1['id_x'] = teams1['id']
	teams2['id_y'] = teams2['id']


	#next steps
	#set index to home team
	#merge on home team
	#fill out featuers

	feats = feats.drop_duplicates(subset=['id'],keep='last')
	feats = feats.tail(30)
	
	todays_games['id'] = todays_games['Season'].astype(str)+todays_games['TeamName'].str.lower().str.replace(" ","")
	
	feats = feats.set_index('id')
	
	today_feats = feats.loc[todays_games['id']]

	test = pd.DataFrame(columns=list(train))
	test['DayOfSeason_x'] = todays_games['DayOfSeason']






def update_games():
	#get what season we're in, season is defined by end year
	season = get_info.get_season()

	#get the box score data already pulled
	season_box = pd.read_csv('output/{}_boxscores_update_test.csv'.format(season))
	
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











