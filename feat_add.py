import pandas as pd
import feature_math
from feature_math import team_ewm



def add_features(df):
  # to add: 
  # 'two_point_field_goal_percentage','three_point_field_goal_percentage', 'free_throw_percentage'
  # 'opp_two_point_field_goal_percentage','opp_three_point_field_goal_percentage', 'opp_free_throw_percentage'
  gb = add_init_features(df)
  #6/10 features done....

  #corresponds to feature creation.ipnyb "IN15"
  gb2 = add_secondary_features(df)
  return gb,gb2



def add_secondary_features(df):
  gb2 = df.groupby(['season','alt_id'])['free_throws','two_point_field_goals','three_point_field_goals','offensive_rebounds','defensive_rebounds','opp_offensive_rebounds','opp_defensive_rebounds','turnovers','wins','losses','pace'].sum().reset_index()

  #shift rows down 1 and rename some columns
  gb2[['fts','2pt','3pt','oreb','dreb','oor','odr','tos','w','l','pace']] = gb2.groupby(['alt_id'])['free_throws','two_point_field_goals','three_point_field_goals','offensive_rebounds','defensive_rebounds','opp_offensive_rebounds','opp_defensive_rebounds','turnovers','wins','losses','pace'].shift()

  gb2 = gb2.dropna()

  gb2 = feature_math.feature_calculation(gb2)

  gb2[['5y_DReb','5y_OReb','5y_FTPct','5y_2PT','5y_3PT','5y_TO','5y_Win']] = gb2.groupby(['alt_id'])['DRebPct','ORebPct','FTPct','2ptPct','3ptPct','TO%','W%'].transform(team_ewm)
  
  gb2['id'] = gb2['season'].astype(str)+gb2['alt_id']

  gb2 = gb2[['id','5y_OReb','5y_FTPct','5y_3PT','5y_TO','5y_Win']]

  return gb2



def add_init_features(df):
  gb = df.groupby(['season','alt_id'])['offensive_rating','pace','opp_two_point_field_goal_percentage','free_throw_percentage','three_point_field_goal_percentage','steal_percentage'].mean().reset_index()

  gb[['ORtg','pace','Opp_FGM%','FTM%','3FGM%','Stl%']] = gb.groupby(['alt_id'])['offensive_rating','pace','opp_two_point_field_goal_percentage','free_throw_percentage','three_point_field_goal_percentage','steal_percentage'].shift()
  gb = gb.dropna()
  gb[['5y_ORtg','5y_pace','5y_Opp_FGM%','5y_FTM%','5y_3FGM%','5y_Stl%']] = gb.groupby(['alt_id'])['ORtg','pace','Opp_FGM%','FTM%','3FGM%','Stl%'].transform(team_ewm)

  gb['id'] = gb['season'].astype(str)+gb['alt_id']

  gb = gb[['id','5y_ORtg','5y_pace','5y_Opp_FGM%','5y_FTM%','5y_3FGM%','5y_Stl%']]
  return gb