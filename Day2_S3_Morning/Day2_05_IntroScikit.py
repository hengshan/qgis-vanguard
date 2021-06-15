import matplotlib.pyplot as plt
import numpy as np
from sklearn import datasets, linear_model
from sklearn.metrics import mean_squared_error, r2_score
import geopandas as gpd
import pandas as pd
pd.set_option('display.max_columns', 20)

# change work directory
import os
os.chdir("/Users/hs/Projects/pyqgis")

# open shape file
sz = gpd.read_file('Data/MP14_Subzone_SocioEconIndicators_2017.shp')
print(type(sz))
print(sz.head())

# plot the subzone polygons
# sz.plot()

# Load the sz dataset
# sz_X, sz_y = datasets.load_sz(return_X_y=True)

allattr=[sz[col] for col in sz.columns.drop('geometry')]
for x in allattr:
	print(x.name)
sz_X = sz[['BET0TO2']]
sz_y = sz['BET25TO29']

# # Use only one feature
# sz_X = sz_X[:, np.newaxis, 2]

# Split the data into training/testing sets
sz_X_train = sz_X[:-10]
sz_X_test = sz_X[-10:]

# Split the targets into training/testing sets
sz_y_train = sz_y[:-10]
sz_y_test = sz_y[-10:]

# # Create linear regression object
regr = linear_model.LinearRegression()

# # Train the model using the training sets
regr.fit(sz_X_train, sz_y_train)

# # Make predictions using the testing set
sz_y_pred = regr.predict(sz_X_test)

# # The coefficients
print('Coefficients: \n', regr.coef_)

# # The mean squared error
print('Mean squared error: %.2f'
      % mean_squared_error(sz_y_test, sz_y_pred))

# # The coefficient of determination: 1 is perfect prediction
print('Coefficient of determination: %.2f'
      % r2_score(sz_y_test, sz_y_pred))

# # Plot outputs
plt.scatter(sz_X_test, sz_y_test,  color='black')
plt.plot(sz_X_test, sz_y_pred, color='blue', linewidth=3)

plt.show()