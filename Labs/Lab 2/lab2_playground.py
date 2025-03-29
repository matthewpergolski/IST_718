#%%
import pandas as pd

# %%
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



# %%

# Little Rock

hotsprings = interp_re_df_nonull[interp_re_df_nonull['City'] == 'Hot Springs']
print(hotsprings.shape)
hotsprings.head()

#%%

hotsprings.groupby('Metro').groupby('Metro').mean()


# %%

# Little Rock

lilrock = interp_re_df_nonull[interp_re_df_nonull['City'] == 'Little Rock']
print(lilrock.shape)
lilrock.head()

# %%
fayetteville = interp_re_df_nonull[interp_re_df_nonull['City'] == 'searcy']
print(lilrock.shape)
lilrock.head()


#%%
searcy = interp_re_df_nonull[interp_re_df_nonull['City'] == 'searcy']
print(lilrock.shape)
lilrock.head()

# %%

# %%
