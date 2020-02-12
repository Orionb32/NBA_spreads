import numpy as np
import pandas as pd
from functools import reduce
import gc
import get_info
import clean_df
import format_df
import feat_add
import feature_math


def main(seasons):
  df = None
  #seasons=list(range(2011,2021))
  
  #  path = './output/{}_boxscores.csv'.format(str(s))
  
  #load all boxscores into df
  df = get_info.get_df(seasons)

  #fix team changes and get all team names in a list
  df,teams = get_info.get_teams(df)
  
  #create seasons column
  df = get_info.add_season(df)

  #add what day of season game was on
  df = get_info.add_dos(df)

  #add winning and losing IDs as well as home/away IDs
  #additionally, fill out rolling games columns
  df = clean_df.add_ids(df)

  #change column names
  df = clean_df.change_col_names(df)



  
  
  df = format_df.prep_new_cols(df)



  home_arenas = get_info.get_home_arenas(df)


  gb,gb2 = feat_add.add_features(df)


  gb3,ewm,em = feature_math.vector_calc(df)

  
  es = feature_math.vector_calc_2(df)

  
  ews = feature_math.weighted_sum(df)

  to_add = combine_es_ews(es,ews)
  

  gb3 = pd.concat([gb3,to_add],axis=1)

 # gb3.head()

  
  feats, feat_cols = feats_creation(gb3,gb2,gb)

  feats = feats_home_merge(feats,home_arenas)

  df = df.drop(columns=['id']) #using feats id

  df = pd.concat([df,feats],axis=1)

  print("preparing train data")
  #df.head()

  train = create_train(df,feat_cols)
  return train , feats, df

  


def create_train(df,feat_cols):
  ids = ids_create(df,feat_cols)
  #print(list(ids))
  team1 = ids.drop_duplicates(subset=['game_id'],keep='first')
  team2 = ids.drop_duplicates(subset=['game_id'],keep='last')

  del ids
  gc.collect()

  train1 = pd.merge(team1,team2,on=['game_id','game_id'],how='left')
  train2 = pd.merge(team2,team1,on=['game_id','game_id'],how='left')

  train = pd.concat([train1,train2],axis=0)
  del train1
  del train2
  gc.collect()

  print("Length of training data", len(train))
  #print(train['rolling'].head())

  #neutral sites
  train['at_home_x'] = np.where((train['at_home_x'].copy()==0)&(train['at_home_y'].copy()==0), 0.5, train['at_home_x'].copy())

  train_tot = train
  train['target'] = train['points_x'].copy() - train['points_y'].copy()

  train_tot['target'] = train_tot['points_x'].copy() + train['points_y'].copy()


  train_df = train.drop(columns=['DayOfSeason_y','at_home_y','points_x','points_y','game_id'])
  print("ready to train")
  train_df.to_csv('output/train_test.csv')
  train_tot = train.drop(columns=['DayOfSeason_y','at_home_y','points_x','points_y','game_id'])

  train_tot.to_csv('output/train_tot.csv')
  return train






def ids_create(df,feat_cols):
  ids = df[feat_cols]
  ids.loc[:,'at_home'] = np.where(ids['location'].copy()==ids['home_loc'].copy(),1,0)
  ids = ids.drop(columns=['location','home_loc'])
  return ids





def feats_home_merge(feats,home_arenas):
  print("home arena length:", len(home_arenas))
  home_arenas = home_arenas.drop_duplicates(subset=['id'])
  print("home arenas after dropping dups: ", len(home_arenas))
  home_arenas  = home_arenas.rename(columns={'location':'home_loc'})

  feats = pd.merge(feats,home_arenas, on=['id','id'],how='left')

  return feats
  

def feats_creation(gb3,gb2,gb):
  gbs = [gb3,gb2,gb]
  feats = reduce(lambda left,right: pd.merge(left,right,on='id',how='left'),gbs)
  feat_cols = list(feats)
  #print(list(feats))
  feat_cols.remove('id')
  feat_cols.insert(0,'home_loc')
  feat_cols.insert(0,'rolling')

  feat_cols.insert(0,'location')
  feat_cols.insert(0,'DayOfSeason')
  feat_cols.insert(0,'points')
  feat_cols.insert(0,'game_id')


  print(list(feat_cols))

  return feats, feat_cols




def combine_es_ews(es,ews):
  es = es[['DRebPct','ORebPct','FTPct','2ptPct','3ptPct','TO%','W%']]
  ews = ews[['DRebPct','ORebPct','FTPct','2ptPct','3ptPct','TO%','W%']]

  es.columns= ['Sea_DReb','Sea_OReb','Sea_FT','Sea_2pt','Sea_3pt','Sea_TO','Sea_W']
  ews.columns= ['wSea_DReb','wSea_OReb','wSea_FT','wSea_2pt','wSea_3pt','wSea_TO','wSea_W']

  to_add = pd.concat([es,ews],axis=1)
  to_add = to_add[['Sea_W','Sea_3pt','Sea_FT','Sea_TO']]

  return to_add




if __name__ == "__main__":
  seasons = range(2011,2021)
  main(seasons)