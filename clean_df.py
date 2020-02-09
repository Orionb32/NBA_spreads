import pandas as pd
import numpy as np
import gc




def change_col_names(df):
  #split into home/away
  home_games = df.loc[df['home_id']==df['team_id']]
  away_games = df.loc[df['away_id']==df['team_id']]
  #clear df
  del df
  gc.collect()
  old_cols = list(home_games)
  home_cols=[]

  for oc in old_cols:
    if 'away_' in oc:
      hc = oc.replace('away_','opp_')
    elif 'home_' in oc:
      hc = oc.replace('home_','')
    else: hc=oc
    home_cols.append(hc)
  
  away_cols=[]
  for oc in old_cols:
    if 'home_' in oc:
        ac = oc.replace('home_','opp_')
    elif 'away_' in oc:
        ac = oc.replace('away_','')
    else:
        ac = oc
    away_cols.append(ac)

  home_games.columns=home_cols
  away_games.columns=away_cols

  col_order = list(away_games)
  home_games = home_games[col_order]

  df = pd.concat([home_games,away_games], axis=0)

  # already have this column
  df = df.drop(columns=['team_id'])

  df = df.sort_values(by=['season','alt_id','date'], ascending=[True,True,True])

  
  df = df.reset_index(drop=True)
  
  return df


  
#game Ids
def add_ids(df):
  df['wn_copy'] = df['winning_name'].str.replace('\n\t\t\t','').str.replace(' ','').str.lower()
  df['ln_copy'] = df['losing_name'].str.replace('\n\t\t\t','').str.replace(' ','').str.lower()
    
  df['wn_copy2'] = df['wn_copy'].str[:4]
  df['wn_copy3'] = df['wn_copy'].str[-4:]
    
  df['ln_copy2'] = df['ln_copy'].str[:4]
  df['ln_copy3'] = df['ln_copy'].str[-4:]
    
  df['game_id'] = df['date'].dt.strftime('%m%d%y') + df['wn_copy2'] + df['wn_copy3'] + df['ln_copy2']  + df['ln_copy3']
    
#     old = len(df)
  #transfer rolling games to all boxscores
  _df = df[['game_id','home_rolling','away_rolling']].groupby(['game_id']).sum()
  df= df.set_index('game_id')
  df = df.drop(columns=['home_rolling','away_rolling'])
  df = df.join(_df,on='game_id')
  df = df.reset_index()



  df = df.drop_duplicates(subset=['game_id'])
#     new = len(df)
    # 53184
    
#     print("Successfully dropped {} duplicate box scores".format(old-new))
    
  df = df.drop(columns=['wn_copy2','ln_copy2','wn_copy3','ln_copy3'])
    
  df['team1_id'] = df['season'].astype(str)+df['wn_copy']
  df['team2_id'] = df['season'].astype(str)+df['ln_copy']
    
  df['alt1_id'] = df['wn_copy']
  df['alt2_id'] = df['ln_copy']
    
  df2 = df.copy()
    
  df = df.drop(columns=['team1_id'])
  df2 = df2.drop(columns=['team2_id'])
  df = df.drop(columns=['alt1_id'])
  df2 = df2.drop(columns=['alt2_id'])
    
  df = df.rename(columns={'team2_id':'team_id','alt2_id':'alt_id'})
  df2 = df2.rename(columns={'team1_id':'team_id','alt1_id':'alt_id'})
    
  df = pd.concat([df,df2],axis=0)
    
  df['home_id'] = np.where(df['winner']=='Home', df['season'].astype(str)+df['wn_copy'], df['season'].astype(str)+df['ln_copy'])
  df['away_id'] = np.where(df['winner']=='Away', df['season'].astype(str)+df['wn_copy'], df['season'].astype(str)+df['ln_copy'])
    
  df['win_id'] = df['season'].astype(str)+df['wn_copy']
  df['lose_id'] = df['season'].astype(str)+df['ln_copy']
    
  df = df.drop(columns=['wn_copy','ln_copy'])
    
  print(len(df))
    #106,368
    
  return df

