import pandas as pd
import numpy as np
import statsmodels.api as sm

# Load the Coaches dataset
coaches_df = pd.read_csv('https://raw.githubusercontent.com/2SUBDA/IST_718/main/Coaches9.csv')

# Clean the data
coaches_df = coaches_df.drop(['SchoolPay', 'Conference'], axis=1) # Drop unnecessary columns
coaches_df = coaches_df.dropna() # Drop any rows with missing data

# Load additional data
stadium_size_df = pd.read_csv('stadium_size.csv') # Replace with actual file name and path
grad_rates_df = pd.read_csv('grad_rates.csv') # Replace with actual file name and path

# Combine the data
merged_df = coaches_df.merge(stadium_size_df, on='School')
merged_df = merged_df.merge(grad_rates_df, on='School')

# Fit a regression model with salary as the response and relevant predictors
X = merged_df[['StadiumSize', 'GSR']] # Replace with relevant predictors
y = merged_df['TotalPay']
X = sm.add_constant(X)
model = sm.OLS(y, X).fit()

# Get the recommended salary for Syracuse football coach
syracuse_df = merged_df[merged_df['School'] == 'Syracuse']
syracuse_predictors = syracuse_df[['StadiumSize', 'GSR']] # Replace with relevant predictors
syracuse_predictors = sm.add_constant(syracuse_predictors)
syracuse_salary = model.predict(syracuse_predictors)[0]

# What would his salary be if we were still in the Big East?
big_east_df = merged_df[merged_df['ConferenceAbbrev'] == 'BE']
big_east_predictors = big_east_df[['StadiumSize', 'GSR']] # Replace with relevant predictors
big_east_predictors = sm.add_constant(big_east_predictors)
big_east_salary = model.predict(big_east_predictors).mean()

# What if we went to the Big Ten?
big_ten_df = merged_df[merged_df['ConferenceAbbrev'] == 'BT']
big_ten_predictors = big_ten_df[['StadiumSize', 'GSR']] # Replace with relevant predictors
big_ten_predictors = sm.add_constant(big_ten_predictors)
big_ten_salary = model.predict(big_ten_predictors).mean()

# What schools did we drop from our data and why?
dropped_schools = set(coaches_df['School']).difference(set(merged_df['School']))
print("We dropped the following schools from our data:", dropped_schools)
print("We dropped these schools because they had missing data.")

# What effect does graduation rate have on the projected salary?
grad_rate_coef = model.params['GSR']
print("The coefficient for graduation rate is:", grad_rate_coef)
print("This indicates that a 1 unit increase in graduation rate is associated with a", round(grad_rate_coef, 2), "unit increase in salary.")

# How good is our model?
rsquared = model.rsquared
print("The R-squared value of the model is:", round(rsquared, 3))
print("This indicates that the model explains", round(rsquared*100, 2), "percent of the variance in salary.")

# What is the single biggest impact on salary size?
biggest_coef = model.params.abs().idxmax()
print("The single biggest impact on salary size comes from the", biggest_coef, "predictor.")