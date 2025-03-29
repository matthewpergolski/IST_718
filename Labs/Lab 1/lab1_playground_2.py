#%%
%%markdown

# IST 718
## Laboratory Exercise - 1
## Matthew L. Pergolski

#%%
%%markdown

### Import Packages/Dependencies

#%%
import pandas as pd
import numpy as np
import seaborn as sns
import statsmodels.api as sm

#%%
%%markdown

### Data Import and Cleaning

The 'Coaches9.csv' is read into a Pandas DataFrame. The DataFrame is then cleaned by replacing '--' with 0, dropping rows with missing values, and replacing commas with empty strings.

The data is then merged with the 'grades.csv' and 'donations_with_conf.csv' files to form a single DataFrame.

The output is an overview of the DataFrame via the '.info()' method as well as a preview of the DataFrame via the '.head()' method.
#%%
# Read data
generic_df = pd.read_csv('/Users/pergolicious/Library/CloudStorage/OneDrive-SyracuseUniversity/Syracuse University/Courses/IST 718/Labs/Lab 1/IST_718-master/Coaches9.csv')
coaches_df = pd.read_csv('/Users/pergolicious/Library/CloudStorage/OneDrive-SyracuseUniversity/Syracuse University/Courses/IST 718/Labs/Lab 1/IST_718-master/Coaches9.csv')
grades_csv = pd.read_csv('/Users/pergolicious/Library/CloudStorage/OneDrive-SyracuseUniversity/Syracuse University/Courses/IST 718/Labs/Lab 1/grades.csv').drop('index', axis=1)
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

# Syracuse has NAN values for Bonus, BonusPaid, and Buyout columns.  Remove from dataset?
coaches_df = coaches_df.dropna()
coaches_df.info()

#%%
coaches_df.head()

#%%
%%markdown

### Data Exploration

The following code block explores the data by calculating the correlation matrix and plotting the correlation matrix as a heatmap.

The overall findings are that the most correlated variables with TotalPay are Buyout, Graduation Rate, and Donations.  The least correlated variables are Bonus, BonusPaid, and AssistantPay.

#%%
# View Distribution of TotalPay
sns.histplot(coaches_df['TotalPay'])

#%%
# Explore the data
correlations = coaches_df.corr()

# Remove The AssistantPay column from the correlations DataFrame
correlations = correlations.drop('AssistantPay', axis=0
                                 ).drop('AssistantPay', axis=1)
correlations['TotalPay']
correlations

#%%
import seaborn as sns

sns.heatmap(correlations, cmap='coolwarm')

'''
Correlation Matrix shows the following are the most correlated with TotalPay (Ignoring SchoolPay):
    - Buyout
    - Graduation Rate
    - Donations

'''

#%%
# View Distribution of of Buyout, Graduation Rate, and Donations
sns.histplot(coaches_df['Buyout'])

#%%
sns.histplot(coaches_df['Graduation Rate (%)'])

#%%
sns.histplot(coaches_df['Donations (in millions)'])


#%%
sns.pairplot(coaches_df, 
             x_vars=['Buyout', 'Graduation Rate (%)', 'Donations (in millions)'], 
             y_vars='TotalPay', 
             height=5, 
             aspect=0.7)

#%%
%%markdown

### Modeling (Linear Regression)

With the above data exploration findings in mind, a linear regression model will be fit with the following independenet variables: Buyout, Graduation Rate, and Donations.  The predicting variable will be TotalPay.
# %%
# Prepare the data
# X = coaches_df[['Bonus', 'BonusPaid', 'AssistantPay', 'Buyout', 'Graduation Rate (%)', 'Donations (in millions)']]
X = coaches_df[['Buyout', 'Graduation Rate (%)', 'Donations (in millions)']]
y = coaches_df['TotalPay']
y = coaches_df['TotalPay']

# Add a constant term to the predictor variables (X)
X = sm.add_constant(X)

# Create the linear model and fit it to the data
model = sm.OLS(y, X).fit()

# Print the model summary
model.summary()

# %% 
%%markdown 

### QUESTION 1

- What is the predicted salary for Syracuse's next football coach?

To predict the recommended salary for Syracuse's next football coach, the predict() will be called on our model variable to estimate the salary:

# %%
# Create a dictionary of data for Syracuse
syracuse_data = {
    'const': 1,
    'Buyout': np.mean(coaches_df['Buyout']),
    'Graduation Rate (%)': np.mean(coaches_df['Graduation Rate (%)']),
    'Donations (in millions)': np.mean(coaches_df['Donations (in millions)'])
}

# Convert the dictionary to a DataFrame
syracuse_df = pd.DataFrame(syracuse_data, index=[0])

# Predict the salary
predicted_salary = model.predict(syracuse_df)
formatted_salary = "${:,.2f}".format(round(predicted_salary[0], 2))
print(f"Predicted salary for Syracuse football coach: {formatted_salary}")

# %% 
%%markdown
### QUESTION 2

- What would his salary be if we were still in the Big East? What if we went to the Big Ten?

To answer this question, you can first calculate the average values for each independent variable in the model based on the conference. Then, you can use these averages to predict the coach's salary in different conferences.

#%%
# Create a function to predict the salary by conference
def predict_salary_by_conference(conference, coaches_df=coaches_df, model=model):
    # Filter the dataframe for the specific conference
    conference_df = coaches_df[coaches_df['Conference'] == conference]
    conference = conference
    # Calculate the average values of the independent variables for the conference
    conference_averages = {
        'const': 1,
        'Buyout': conference_df['Buyout'].mean(),
        'Graduation Rate (%)': conference_df['Graduation Rate (%)'].mean(),
        'Donations (in millions)': conference_df['Donations (in millions)'].mean()
    }

    # Convert the dictionary to a DataFrame
    conference_averages_df = pd.DataFrame(conference_averages, index=[0])

    # Predict the salary
    predicted_conference_salary = model.predict(conference_averages_df)
    formatted_conference_salary = "${:,.2f}".format(round(predicted_conference_salary[0], 2))
    
    return formatted_conference_salary

# Create a list of conferences
conferences = coaches_df['Conference'].unique()

# Create an empty dictionary to store the predicted salaries
predicted_salaries = {}

# Loop through each conference and predict the salary
for conference in conferences:
    predicted_salary = predict_salary_by_conference(conference)
    predicted_salaries[conference] = predicted_salary

# Convert the dictionary to a DataFrame
predicted_salaries_df = pd.DataFrame.from_dict(predicted_salaries, orient='index', columns=['Predicted Salary'])

predicted_salaries_df

#%%
def print_salary(conference, predicted_salaries_df=predicted_salaries_df):
    print(f"Predicted average salary for {conference} football coach: {predicted_salaries_df.loc[conference]['Predicted Salary']}") 

print_salary('Big Ten')
print_salary('ACC')

#%%
%%markdown

### QUESTION 3
- What schools did we drop from our data and why?

Overall, 42 schools were dropped:
- 'Air Force',
- 'Arizona',
- 'Arizona State',
- 'Arkansas',
- 'Army',
- 'Baylor',
- 'Boston College',
- 'Brigham Young',
- 'Central Florida',
- 'Duke',
- 'Florida',
- 'Florida State',
- 'Georgia Southern',
- 'Kent State',
- 'Liberty',
- 'Louisiana-Lafayette',
- 'Miami (Fla.)',
- 'Mississippi',
- 'Mississippi State',
- 'Navy',
- 'Nebraska',
- 'Northwestern',
- 'Notre Dame',
- 'Oregon',
- 'Oregon State',
- 'Pittsburgh',
- 'Rice',
- 'South Alabama',
- 'Southern California',
- 'Southern Methodist',
- 'Stanford',
- 'Syracuse',
- 'Tennessee',
- 'Texas A&M',
- 'Texas Christian',
- 'Texas-El Paso',
- 'Tulane',
- 'Tulsa',
- 'UCLA',
- 'Vanderbilt',
- 'Wake Forest',
- 'Wisconsin'

The schools were dropped from the state becasue they had '--' values that were turned to NaN via the data cleansing process.

#%%
# Create dropped schools data frame
generic_df = pd.read_csv('/Users/pergolicious/Library/CloudStorage/OneDrive-SyracuseUniversity/Syracuse University/Courses/IST 718/Labs/Lab 1/IST_718-master/Coaches9.csv')
generic_df.replace('--', np.nan, inplace=True)
null = generic_df[generic_df.isnull().any(axis=1)]
null.info()

#%%
# Identify dropped schools
null_schools = null['School'].unique().tolist()
null_schools

#%%
%%markdown
### QUESTION 4
- What effect does graduation rate have on the projected salary?

To answer this question, viewing the output of the linear regression model will be required.

For the graduation rate coefficient, the p-value is less than the standard threshold of 0.05. This means that the coefficient is statistically significant. The coefficient value is 3.792e+04 (37920), which means that for every 1% increase in graduation rate, the predicted salary increases by ~$37,920. It is the single largest contributor to the predicted salary (TotalPay).
#%%
model.summary()

#%%
%%markdown
### QUESTION 5
- How good is our model?

To answer this question, it will be necessary to again review the model summary.

When first reviewing the output of a linear regression model, the first step is to evaluate the p-value of the f-statistic itself.  Since this appears to be well under the standard 0.05 threshold (1.43e-32), it can be determiend that the model can be interpreted.

It's then advisable to move onto the R-squared value.  It's seen that the value for this is 0.837, which tells the reader that ~83.7% of the change in our Y variable (TotalPay) is explained by the change in our independent (X) variables -- which is 'Buyout', 'Graduation Rate (%)', and 'Donations (in millions)'.
    
The coefficients for these varialbes, as well as their respective p-values, can be viewed in the output as well.
    
The p-values for each indepdnent variable look to be under the 0.05 threshold, which means that they are statistically significant to the model.

#%%
model.summary()

#%%
%%markdown
### QUESTION 6
- What is the single biggest impact on salary size?

As mentioned above, the single biggest impact on salary size is the graduation rate.  This is seen in the coefficient for the graduation rate variable, which is 3.792e+04 (37920).  This means that for every 1% increase in graduation rate, the predicted salary increases by ~$37,920.

# %%
# Get the coefficients from the model
coefficients = model.params
coefficients

# %%
