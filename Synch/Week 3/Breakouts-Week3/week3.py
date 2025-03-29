#%%
import pandas as pd
df = pd.read_csv("https://raw.githubusercontent.com/2SUBDA/Breakouts/Week3/Case3SalesProducts.csv", error_bad_lines=False)
df
# %%
# grouped = df.groupby('Country').mean()
# grouped

# %%
df = df[df['Country'] =='United States']
df.head()
# %%
df.info()
# %%
df.isnull().sum()
# %%
df.dropna(inplace=True)
# %%
df.head()
# %%
df.info()
# %%
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression

#%%
# select the features and target variable
#X = df[['Revenue', 'Quantity', 'GrossMargin']]
X = df[['GrossMargin']]
y = df['SustainableClaim']

# split the data into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# train a linear regression model
model = LinearRegression()
model.fit(X_train, y_train)

# make predictions on the testing set
y_pred = model.predict(X_test)

# evaluate the model's performance
score = model.score(X_test, y_test)
print('R^2 score:', score)
# %%
import matplotlib.pyplot as plt

# plot actual vs. predicted values
plt.scatter(df['Revenue'], y_pred)
plt.xlabel('Actual Revenue')
plt.ylabel('Predicted Revenue')
plt.title('Actual vs. Predicted Revenue')
plt.show()
# %%
import seaborn as sns
# select the features
features = ['Revenue', 'Quantity', 'GrossMargin', 'SustainableMarketing']

# create a correlation matrix
corr_matrix = df[features].corr()

# plot the correlation matrix using a heatmap
sns.heatmap(corr_matrix, annot=True, cmap='coolwarm')
# %%
