import pandas as pd
from sklearn.metrics import roc_auc_score
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction import DictVectorizer
from sklearn.ensemble import RandomForestClassifier
import joblib

df_name = 'Car Ownership.csv'
df = pd.read_csv(df_name)

modelFileName = 'model.bin'
dictVectorizerFileName  ='dv.bin'

# Data normalization
print("data normalization")
df.columns = df.columns.str.lower().str.replace(' ', '_')
df = df[df.occupation.isna()!=True]
df = df[df.car.isna()!=True]

df.number_of_children = df.number_of_children.str.replace('na', '0').fillna(0).astype(int)

df.monthly_income = df.monthly_income.str.lower().str.replace('$','').str.replace(',','').str.replace('.', '').str.replace(' ', '').str.replace('usd','').str.replace('k', '000')
mean_monthly_income = df.monthly_income[df.monthly_income.isna() != True].astype(int).mean()
df.monthly_income = df.monthly_income.fillna(mean_monthly_income)
df.monthly_income = df.monthly_income.astype(int)

df.occupation = df.occupation.str.lower().str.replace(' ', '_')

df.years_of_employment = df.years_of_employment.fillna(0)
df.years_of_employment = df.years_of_employment.apply(lambda x: str(x).strip().partition(' ')[0]).str.replace('nan', '0').fillna(0).astype(int)

df.finance_status = df.finance_status.str.lower()

df.finance_history = df.finance_history.str.lower().str.replace(' ','_').str.replace(',','_').str.replace('__','_')

df.car = df.car.str.lower()

df.car = (df.car=='yes').astype(int)

df.finance_status = df.finance_status.fillna('unkonw')

df.finance_history = df.finance_history.fillna('no_issues')
df.finance_history = df.finance_history.str.replace('no_significant_issues', 'no_significant_issue')
df.finance_history = df.finance_history.str.replace('late_payments', 'late_payment')

df.credit_score = df.credit_score.fillna(0)

# Split data
print("data split")
SEED = 11
data_class = df.copy()

df_full_train, df_test = train_test_split(data_class, test_size=0.2, random_state=SEED)
df_train, df_val = train_test_split(df_full_train, test_size=0.25, random_state=SEED)

df_train = df_train.reset_index(drop=True)
df_val = df_val.reset_index(drop=True)
df_test = df_test.reset_index(drop=True)

y_train = df_train.car.values
y_val = df_val.car.values
y_test = df_test.car.values

del df_train['car']
del df_val['car']
del df_test['car']

dv = DictVectorizer(sparse=False)
train_dict = df_train.to_dict(orient='records')
X_train = dv.fit_transform(train_dict)
val_dict = df_val.to_dict(orient='records')
X_val = dv.transform(val_dict)

print("random forest model training")
rf = RandomForestClassifier(n_estimators=110,
                            max_depth=15,
                            min_samples_leaf=1,
                            random_state=1)
rf.fit(X_train, y_train)

y_pred = rf.predict_proba(X_val)[:, 1]
random_forest_auc = roc_auc_score(y_val, y_pred)

print('ROC AUC Score: %.3f' % random_forest_auc)


print(f"saving model object to {modelFileName}")
joblib.dump(rf, modelFileName)
print(f"dictVectorizer object to {dictVectorizerFileName}")
joblib.dump(dv, dictVectorizerFileName)