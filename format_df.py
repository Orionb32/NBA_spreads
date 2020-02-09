import pandas as pd
import numpy as np


def prep_new_cols(df):
  # cols ready for running averages
  dcols = ['offensive_rating','defensive_rating','opp_offensive_rating','opp_defensive_rating','pace']

  # cols needed for feature creation
  ncols = ['free_throws','two_point_field_goals','three_point_field_goals',
         'offensive_rebounds','defensive_rebounds','opp_offensive_rebounds','opp_defensive_rebounds',
         'turnovers',
         'wins','losses']

  add_cols = ['assist_percentage', 'block_percentage', 'personal_fouls', 'steal_percentage', 'two_point_field_goal_percentage','three_point_field_goal_percentage', 'free_throw_percentage','rolling']

  add_opp_cols = ['opp_assist_percentage', 'opp_block_percentage', 'opp_personal_fouls', 'opp_steal_percentage', 
                'opp_two_point_field_goal_percentage', 'opp_three_point_field_goal_percentage', 'opp_free_throw_percentage','opp_rolling']

  # cols necessary to keep 
  nncols = ['date','DayOfSeason','location','id','alt_id','opp_id','game_id','season','win_id','lose_id','points','opp_points']

  cols = nncols+dcols+ncols+add_cols+add_opp_cols

  old_num_cols = len(list(df))
  df = df[cols]
  new_num_cols = len(list(df))

  print("Dropped {} unnecessary columns".format(old_num_cols-new_num_cols))
  df = df.reset_index(drop=True)
  return df