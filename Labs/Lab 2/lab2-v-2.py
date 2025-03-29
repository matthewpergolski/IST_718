#%%
import pandas as pd
import matplotlib.pyplot as plt

# %%
#re_df = pd.read_csv('http://files.zillowstatic.com/research/public_csvs/zhvi/Zip_zhvi_uc_sfr_month.csv')
re_df = pd.read_csv('/Users/pergolicious/Downloads/Zip_zhvi_uc_sfrcondo_tier_0.33_0.67_sm_sa_month.csv')
re_df.head()

# %%
#re_df.isnull().sum().to_csv('nulls_re.csv')
print(re_df.shape)
re_df.info()

# %%
re_df_nonull = re_df.dropna()
print(re_df_nonull.shape)
re_df_nonull.info()
# %%

interp_re_df = pd.concat([re_df.iloc[:, :7], re_df.iloc[:, 7:].interpolate()], axis=1)
print(interp_re_df.shape)
interp_re_df.head()
# %%

'''
Interpolate the missing values in the dataframe for date columns


Remove nulls from Region, Size, Rank, RegionName, RegionType

'''

interp_re_df_nonull = interp_re_df.dropna()
print(interp_re_df_nonull.shape)
interp_re_df_nonull.info()
interp_re_df_nonull.head()

#%%

#%%
interp_re_df_nonull = interp_re_df_nonull[interp_re_df_nonull['State'] == 'AR']

# Data Cleaning and Preprocessing
selected_metros = ['Hot Springs', 'Little Rock', 'Fayetteville', 'Searcy']
df_filtered = interp_re_df_nonull[interp_re_df_nonull['City'].isin(selected_metros)]
print(df_filtered.shape)
df_filtered.head()

#%%
# Keep only the date columns
date_columns = [col for col in df_filtered.columns if col.startswith('19') or col.startswith('20')]
columns_to_keep = ['RegionName', 'Metro'] + date_columns
df_filtered = df_filtered[columns_to_keep]
print(df_filtered.shape)
df_filtered.head()
#%%
# Convert wide format to long format for easier time series analysis
df_long = pd.melt(df_filtered, id_vars=['RegionName', 'Metro'], var_name='Date', value_name='Value')
df_long['Date'] = pd.to_datetime(df_long['Date'], format="%Y-%m")
df_long = df_long.sort_values(by=['RegionName', 'Date'])
print(df_long.shape)
df_long.head()

#%%
# # Exploratory Data Analysis
# grouped_metros = df_long.groupby(['Metro', 'Date']).mean().reset_index()
# # Time Series Plots
# fig, ax = plt.subplots(figsize=(10, 6))

# for metro in selected_metros:

#     metro_data = grouped_metros[grouped_metros['Metro'] == metro]
#     ax.plot(metro_data['Date'], metro_data['Value'], label=metro)
# ax.set_xlabel('Date')
# ax.set_ylabel('Average Median Housing Value')
# ax.set_title('Average Median Housing Value for Selected Metro Areas (1997 - Present)')
# ax.legend()
# plt.show()
# %%
import matplotlib.pyplot as plt

df_long = df_long.groupby(['Metro', 'Date']).mean().reset_index()

df_long.plot(x='Date', y='Value')
plt.show()
# %%
for name, group in df_long.groupby('Metro'):
    group.plot(x='Date', y='Value', title=name)
    plt.show()
# %%
import matplotlib.pyplot as plt

fig, axs = plt.subplots(nrows=len(df_long['Metro'].unique()), figsize=(10, 20))

for i, (name, group) in enumerate(df_long.groupby('Metro')):
    group.plot(x='Date', y='Value', title=name, ax=axs[i])
    
plt.tight_layout()
plt.show()

#%%
fig, ax = plt.subplots(figsize=(10, 20))

for name, group in df_long.groupby('Metro'):
    ax.plot(group['Date'], group['Value'], label=name)

ax.legend()
plt.show()
# %%
# larger influxes in value since 2000

#%%
import numpy as np
import itertools
from statsmodels.tsa.statespace.sarimax import SARIMAX
from sklearn.metrics import mean_squared_error




#%%
# Function to calculate the SARIMAX model's AIC
def get_sarimax_aic(data, order, seasonal_order):
    try:
        model = SARIMAX(data, order=order, seasonal_order=seasonal_order, enforce_stationarity=False, enforce_invertibility=False)
        model_fit = model.fit(disp=0)
        return model_fit.aic
    except:
        return np.inf

#%%
# Choose one zip code for demonstration
selected_zip = df_long['RegionName'].iloc[0]
selected_zip
#%%
df_zip = df_long[df_long['RegionName'] == selected_zip]
df_zip.head()

#%%
# Split the dataset into training (1997-2017) and test (2018) sets
train_data = df_zip[df_zip['Date'] < '2018-01-01']
test_data = df_zip[df_zip['Date'] >= '2018-01-01']

# Grid search to find the best SARIMAX model
p = q = range(0, 3)
d = range(0, 2)
pdq = list(itertools.product(p, d, q))

seasonal_pdq = [(x[0], x[1], x[2], 12) for x in pdq]

best_aic = np.inf
best_order = None
best_seasonal_order = None

for order in pdq:
    for seasonal_order in seasonal_pdq:
        aic = get_sarimax_aic(train_data['Value'], order, seasonal_order)
        if aic < best_aic:
            best_aic = aic
            best_order = order
            best_seasonal_order = seasonal_order

# Train the best SARIMAX model
best_model = SARIMAX(train_data['Value'], order=best_order, seasonal_order=best_seasonal_order, enforce_stationarity=False, enforce_invertibility=False)
best_model_fit = best_model.fit()

# Forecasting for 2018
forecast_steps = len(test_data)
forecast = best_model_fit.forecast(steps=forecast_steps)

# Calculate the RMSE for the model
rmse = np.sqrt(mean_squared_error(test_data['Value'], forecast))
print(f"RMSE for the SARIMAX model: {rmse:.2f}")

#%%
plt.plot(test_data['Date'], forecast, label='Forecast')
plt.plot(test_data['Date'], test_data['Value'], label='Actual')
plt.legend(loc='upper left')
plt.show()





# %%
