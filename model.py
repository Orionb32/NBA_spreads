from sklearn.model_selection import KFold, cross_val_score, train_test_split, cross_validate
from sklearn.metrics import mean_absolute_error
import lightgbm as lgb
from sklearn.preprocessing import RobustScaler,StandardScaler
import pandas as pd

def mae_cv(model, lin_reg=False):

  kf = KFold(n_folds, shuffle=True, random_state=17).get_n_splits(X.values)
  output = cross_validate(model,X.values, y,cv=kf,scoring = 'neg_mean_absolute_error',return_estimator=True)
  all_estimators=[]
  for idx, estimator in enumerate(output['estimator']):
    if lin_reg:
      all_estimators.append(list(estimator.coef))
    else:
      all_estimators.append(list(estimator.feature_importances_))
  all_estimators = pd.DataFrame(all_estimators)
  avg_imp = all_estimators.values.mean(axis=0)
  feature_importances = pd.DataFrame(avg_imp, index=feat_names,columns=['importance']).sort_values('importance',ascending=False).reset_index()

  feature_importances.columns = ['feats','importance']
  return output, feature_importances



path = "output/train_test.csv"
df = pd.read_csv(path)
df.isna().sum(axis=1)
print(len(df))
df = df.dropna(axis=0)
print(len(df))
with pd.option_context('mode.use_inf_as_na',True):
  dr=df.fillna(0)

to_drop = ['Sea_TO_x','Sea_TO_y','Sea_FT_x','Sea_FT_y','Sea_PF_x','Sea_PF_y']
df = df.drop(columns=to_drop)
y = df.target
X= df.drop(columns=['target'])

scaler = StandardScaler()
cat = []
num = [i for i in list(df)]

df[num] = scaler.fit_transform(df[num])
n_folds = 8
feat_names = list(X)

model_lgb = lgb.LGBMRegressor(objective='regression',learning_rate=0.09,importance='gain')

output,feat_imp = mae_cv(model_lgb)
print(feat_imp)

print("LGBM score: {:.4f} ({:.4f})\n" .format(-1*output['test_score'].mean(), output['test_score'].std()))







