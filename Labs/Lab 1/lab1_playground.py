#%%
import pandas as pd
import numpy as np
#%%
df = pd.read_csv('/Users/pergolicious/Library/CloudStorage/OneDrive-SyracuseUniversity/Syracuse University/Courses/IST 718/Labs/Lab 1/IST_718-master/Coaches9.csv')

# %%
coaches_df = pd.read_csv('/Users/pergolicious/Library/CloudStorage/OneDrive-SyracuseUniversity/Syracuse University/Courses/IST 718/Labs/Lab 1/IST_718-master/Coaches9.csv')
coaches_df
coaches_df.info()

# %%
coaches_df.replace('--', 0, inplace=True)
coaches_df = coaches_df.dropna()
coaches_df.head()

# %%
coaches_df['School'] = coaches_df['School'].astype(str).str.replace(',', '', regex=True)
coaches_df['Conference'] = coaches_df['Conference'].astype(str).str.replace(',', '', regex=True)
coaches_df['Coach'] = coaches_df['Coach'].astype(str).str.replace(',', '', regex=True)

coaches_df['SchoolPay'] = coaches_df['SchoolPay'].astype(str).str.replace(',', '', regex=True).str.replace('$', '', regex=True).astype(float)
coaches_df['TotalPay'] = coaches_df['TotalPay'].astype(str).str.replace(',', '', regex=True).str.replace('$', '', regex=True).astype(float)
coaches_df['Bonus'] = coaches_df['Bonus'].astype(str).str.replace(',', '', regex=True).str.replace('$', '', regex=True).astype(float)
coaches_df['BonusPaid'] = coaches_df['BonusPaid'].astype(str).str.replace(',', '', regex=True).str.replace('$', '', regex=True).astype(float)
coaches_df['AssistantPay'] = coaches_df['AssistantPay'].astype(str).str.replace(',', '', regex=True).str.replace('$', '', regex=True).astype(float)
coaches_df['Buyout'] = coaches_df['Buyout'].astype(str).str.replace(',', '', regex=True).str.replace('$', '', regex=True).astype(float)
coaches_df.head()

# %%
grades_csv = pd.read_csv('/Users/pergolicious/Library/CloudStorage/OneDrive-SyracuseUniversity/Syracuse University/Courses/IST 718/Labs/Lab 1/grades.csv')
grades_csv
grades_csv = grades_csv.drop('index', axis=1)
grades_csv

# %%
donations_csv = pd.read_csv('/Users/pergolicious/Library/CloudStorage/OneDrive-SyracuseUniversity/Syracuse University/Courses/IST 718/Labs/Lab 1/donations_with_conf.csv')
donations_csv
donations_csv = donations_csv.drop('index', axis=1)
donations_csv

# %%
coaches_df = coaches_df.merge(grades_csv, left_on='School', right_on='School')
coaches_df.info()

# %
# %%
coaches_df = coaches_df.merge(donations_csv, left_on='School', right_on='School')
coaches_df = coaches_df.drop('Conference_y', axis=1)
coaches_df = coaches_df.rename(columns={'Conference_x': 'Conference'})
coaches_df = coaches_df.drop('Donations (in millions)_x', axis=1)
coaches_df = coaches_df.rename(columns={'Donations (in millions)_y': 'Donations (in millions)'})
coaches_df.info()
# %%
import statsmodels.api as sm
# %%
# Fit a regression model with salary as the response and relevant predictors
# X = coaches_df[['Donations (in millions)', 'Graduation Rate (%)']] # Replace with relevant predictors
X = coaches_df[['Donations (in millions)']] # Replace with relevant predictors
print(X)
y = coaches_df['TotalPay']
print(y)
X = sm.add_constant(X)
model = sm.OLS(y, X).fit()
model.summary()
# %%
# Get the recommended salary for Syracuse football coach
# syracuse_df = coaches_df[coaches_df['School'] == 'Syracuse']
# syracuse_df
# syracuse_df = coaches_df[coaches_df['School'] == 'Syracuse'].reset_index(drop=True)
# syracuse_df
# syracuse_predictors = syracuse_df[['Donations (in millions)', 'Graduation Rate (%)']] # Replace with relevant predictors
# syracuse_predictors = sm.add_constant(syracuse_predictors)
# syracuse_predictors.info()
# syracuse_salary = model.predict(syracuse_predictors)[0]
# syracuse_salary = model.predict(syracuse_predictors)[0]
# #%%
# %%
X_new = sm.add_constant(np.array([20000]))
y_pred = model.predict(X_new)
y_pred
# %%
# try get a prediction with x varialbe
# prediction with multiple variables (choose what you feel is most)
# categorize schools in different conferences
# Add new column to our schools data frame that includes conference information
#     - conference column would be a new predictor (X variable) in our analysis

#%%
import pandas as pd

# Read data
coaches_df = pd.read_csv('/Users/pergolicious/Library/CloudStorage/OneDrive-SyracuseUniversity/Syracuse University/Courses/IST 718/Labs/Lab 1/IST_718-master/Coaches9.csv')
grades_csv = pd.read_csv('grades.csv').drop('index', axis=1)
donations_csv = pd.read_csv('donations_with_conf.csv').drop('index', axis=1)

# Clean coaches_df
coaches_df.replace('--', 0, inplace=True)
coaches_df = coaches_df.dropna()
replace_dict = {col: str for col in ['School', 'Conference', 'Coach']}
coaches_df = coaches_df.astype(replace_dict).replace(',', '', regex=True)

money_columns = ['SchoolPay', 'TotalPay', 'Bonus', 'BonusPaid', 'AssistantPay', 'Buyout']
for col in money_columns:
    coaches_df[col] = coaches_df[col].str.replace('[^0-9.]', '', regex=True).astype(float)

# Merge data
coaches_df = coaches_df.merge(grades_csv, on='School')
coaches_df = coaches_df.merge(donations_csv, on='School')

# Clean merged data
#coaches_df = coaches_df.drop(['Conference_y', 'Donations (in millions)_x'], axis=1)
coaches_df = coaches_df.drop(['Conference_y'], axis=1)
coaches_df = coaches_df.rename(columns={'Conference_x': 'Conference', 'Donations (in millions)_y': 'Donations (in millions)'})
coaches_df

# %%
