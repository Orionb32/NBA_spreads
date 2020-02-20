import pandas as pd
import numpy as np
import model
import feature_creation
import tri_code_dict
import clean_df
import get_info
from datetime import datetime, date



def main(home_team, road_team, home_rolling=0,road_rolling=0,date=datetime.today()):
	season = get_season(date)
	train, feats, df=feature_creation.main(range(2011,2021))

	feats = feats.drop_duplicates(subset=['id'],keep='last')
	feats = feats.tail(30)

	tri_team = tri_to_team()

	home_id =str(season) + tri_team[home_team].lower().replace(" ","")
	away_id =str(season) + tri_team[road_team].lower().replace(" ","")
	
	feats = feats.set_index('id')

	feats_x = feats.loc[[home_id]]
	feats_y = feats.loc[[away_id]]

	feats_x = feats_x.reset_index()
	feats_y = feats_y.reset_index()

	feats_x.reset_index()
	feats_y.reset_index()

	feats_x = clean_df.append_cols(feats_x, "_x")
	feats_y = clean_df.append_cols(feats_y, "_y")

	feats_x['rolling_x'] = home_rolling
	feats_y['rolling_y'] = road_rolling


	feats_x['game_id'] = date.isoformat()[:10] + home_id[4:] + away_id[4:]
	feats_y['game_id'] = date.isoformat()[:10] + home_id[4:] + away_id[4:]

	feats = feats_x.merge(feats_y,on="game_id")
	
	feats['DayOfSeason_x'] = add_dos(date)
	feats['at_home_x'] = 1


	print(feats)
	list(feats)
	spread, total = predict(feats)

	if (spread>0):
		print(home_team + " wins by: " + str(spread))
	else:
		print(road_team + " wins by: " + str(spread))
	return spread, total


def predict(feats):
	path = 'output/train.csv'
	path_tot = 'output/train_tot.csv'
	
	model_lgb,X,y,train = model.train(path)
	train = train.drop(columns=['target'])
	#X = X.drop(columns = ['Unnamed: 0'])
	model_lgb.fit(X, y)
	train_prediction = model_lgb.predict(train)

	model_lgb2 , X2,y2, train_tot = model.train(path_tot)
	train_tot  = train_tot.drop(columns=['target'])
	#X2= X2.drop(columns = ['Unnamed: 0'])
	model_lgb2.fit(X2, y2)
	train_prediction_tot = model_lgb2.predict(train_tot)



#	today1 = today.drop(columns=['date_x','Season_x','BoxscoreIndex','HomeTeam_x','home_loc_x','date_y','Season_y','TeamName','DayOfSeason_y','HomeTeam_y','team_y','id_y','home_loc_y'])
	feats= feats.drop(columns=['game_id','id_x','Sea_PF_x','Sea_PF_y','Sea_FT_x','Sea_FT_y','Sea_TO_x','Sea_TO_y','home_loc_x','id_y','home_loc_y'])

	prediction = model_lgb.predict(feats)
	prediction2 = model_lgb2.predict(feats)
	print(prediction)
	return prediction, prediction2



def add_dos(date):
	season = get_season(date)
	season_start = datetime(season,10,20)
	DayOfSeason = date - season_start
	return DayOfSeason.days

	
def tri_to_team():
	ctc = tri_code_dict.create_team_conversion()
	rev_ctc = dict([(value,key) for key, value in ctc.items()])
	return rev_ctc

def get_season(date):
	if (date.month>9):
		season = date.year +1
	else: season = date.year
	return season

if __name__ == "__main__":
	main()
