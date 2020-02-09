import pandas as pd



def feature_calculation(df):

	# defensive rebounds available
	df['dra'] = df['dreb'] + df['oor']

	# offensive rebounds available
	df['ora'] = df['oreb'] + df['odr']

	#off/def rebound percentage

	df['DRebPct'] = df['dreb']/df['dra']
	df['ORebPct'] = df['oreb']/df['ora']
	df['_points'] = df['fts'] + 2*df['2pt'] + 3*df['3pt']
	df['FTPct'] = df['fts']/df['_points']
	df['2ptPct'] = df['2pt']/df['_points']
	df['3ptPct'] = df['3pt']/df['_points']
	df['TO%'] = df['tos']/df['pace']
	df['gp'] = df['w'] + df['l']
	df['W%'] = df['w']/df['gp']

	return df


def level_1_drop(frame):
	if 'level_1' in list(frame):
		return frame.drop(columns=['level_1'])
	else: return frame

def team_ewm(team, span=5, alpha=0.85):
	feature_ewm = team.rolling(window=span, min_periods=1).mean()[:span]
	rest = team[span:]
	return pd.concat([feature_ewm, rest]).ewm(alpha=alpha, adjust=False).mean()


#compute vecotrs for evrey team at time of each game
#already sorted by date
def vector_calc(df):
  # season-to-date avg
	df[['ORtg','DRtg','pace','Ast%','Blk%','PF','Stl%','FGM%','3FGM%','FTM%','Opp_Ast%','Opp_Blk%','Opp_PF','Opp_Stl%','Opp_FGM%','Opp_3FGM%','Opp_FTM%']] = df.groupby(['id'])['offensive_rating','defensive_rating','pace','assist_percentage','block_percentage', 'personal_fouls', 'steal_percentage', 'two_point_field_goal_percentage','three_point_field_goal_percentage', 'free_throw_percentage','opp_assist_percentage', 'opp_block_percentage', 'opp_personal_fouls', 'opp_steal_percentage','opp_two_point_field_goal_percentage','opp_three_point_field_goal_percentage','opp_free_throw_percentage'].shift()
  
  #expanding mean
	em = df.groupby(['id'])['ORtg','DRtg','pace','Ast%','Blk%','PF','Stl%','FGM%','3FGM%','FTM%','Opp_Ast%','Opp_Blk%','Opp_PF','Opp_Stl%','Opp_FGM%','Opp_3FGM%','Opp_FTM%'].expanding().mean().reset_index()

	em = level_1_drop(em)
  
  #might need to rework this - trying to pass args into team_ewm since they change from other definition
  #just added expanded team ewm instead of team ewm
	ewm = df.groupby(['id'])['ORtg','DRtg','pace','Ast%','Blk%','PF','Stl%','FGM%','3FGM%','FTM%','Opp_Ast%','Opp_Blk%','Opp_PF','Opp_Stl%','Opp_FGM%','Opp_3FGM%','Opp_FTM%'].apply(expanded_team_ewm).reset_index()

	ewm = level_1_drop(ewm)

	ewm.columns=['id','wORtg','wDRtg','wpace','wAst%','wBlk%','wPF','wStl%','wFGM%','w3FGM%','wFTM%','wOpp_Ast%','wOpp_Blk%','wOpp_PF','wOpp_Stl%','wOpp_FGM%','wOpp_3FGM%','wOpp_FTM%']

	gb3 = pd.concat([em, ewm.drop(columns=['id'])], axis=1)

	gb3.columns=['id','Sea_ORtg','Sea_DRtg','Sea_pace','Sea_Ast%','Sea_Blk%','Sea_PF','Sea_Stl%','Sea_FGM%','Sea_3FGM%','Sea_FTM%','Sea_Opp_Ast%','Sea_Opp_Blk%','Sea_Opp_PF','Sea_Opp_Stl%','Sea_Opp_FGM%','Sea_Opp_3FGM%','Sea_Opp_FTM%','wSea_ORtg','wSea_DRtg','wSea_pace','wSea_Ast%','wSea_Blk%','wSea_PF','wSea_Stl%','wSea_FGM%','wSea_3FGM%','wSea_FTM%','wSea_Opp_Ast%','wSea_Opp_Blk%','wSea_Opp_PF','wSea_Opp_Stl%','wSea_Opp_FGM%','wSea_Opp_3FGM%','wSea_Opp_FTM%']

	gb3 = gb3[['id','Sea_DRtg','Sea_Opp_3FGM%','Sea_Opp_PF','Sea_pace','wSea_ORtg','wSea_Stl%','wSea_Ast%','wSea_Opp_Ast%','wSea_Blk%','wSea_FGM%','Sea_FTM%','Sea_PF']]

	return gb3, ewm,em





def vector_calc_2(df):
  # shift up one
	df[['fts','2pt','3pt','oreb','dreb','oor','odr','tos','w','l','pace']] = df.groupby(['id'])['free_throws','two_point_field_goals','three_point_field_goals','offensive_rebounds','defensive_rebounds','opp_offensive_rebounds','opp_defensive_rebounds','turnovers','wins','losses','pace'].shift()

	es = df.groupby(['id'])['fts','2pt','3pt','oreb','dreb','oor','odr','tos','w','l','pace'].expanding().sum().reset_index()

	es= level_1_drop(es)
	es = feature_calculation(es)
	return es




def weighted_sum(df):
	ews = df.groupby(['id'])['fts','2pt','3pt','oreb','dreb','oor','odr','tos','w','l','pace'].apply(team_ews).reset_index()

	ews = level_1_drop(ews)

	ews = feature_calculation(ews)
	return ews


#weighted sum
def team_ews(team, span=50, alpha=0.84):
	feature_ewm = team.rolling(window=span, min_periods=1).sum()[:span]
	rest = team[span:]
	return pd.concat([feature_ewm, rest]).ewm(alpha=alpha, adjust=False).mean()










def expanded_team_ewm(team,span=50,alpha=0.84):
	feature_ewm = team.rolling(window=span, min_periods=1).mean()[:span]
	rest = team[span:]
	return pd.concat([feature_ewm, rest]).ewm(alpha=alpha, adjust=False).mean()