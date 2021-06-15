import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

#Get the month and year
import os
os.chdir("/Users/hs/Projects/pyqgis")

# quick start
X = np.linspace(0, 2*np.pi,100)
Y=np.cos(X)
Z=np.sin(X)

plt.plot(X, Y, 'r.', X, Z, 'g-')

x = [1, 2, 3]
y = np.array([[1, 2], [3, 4], [5, 6]])
plt.plot(x, y)
plt.show()


fig, [ax1,ax2] = plt.subplots(2,1,sharex=True)
ax1.plot(X,Y)
ax2.plot(X,Z)
# fig.show()

np.random.seed(19680801)
data = np.random.randn(2, 100)

fig, axs = plt.subplots(2, 2, figsize=(5, 5))
axs[0, 0].hist(data[0])
axs[1, 0].scatter(data[0], data[1])
axs[0, 1].plot(data[0], data[1])
axs[1, 1].hist2d(data[0], data[1])

plt.show()

df=pd.read_csv("Data/Groceries_dataset.csv")

df['year'] = pd.DatetimeIndex(df['Date']).year
df['month'] = pd.DatetimeIndex(df['Date']).month
df['month_year'] = pd.to_datetime(df['Date']).dt.to_period('M')

#Group items counted by month-year
group_by_month = df.groupby('month_year').agg({'Member_number':'nunique'}).reset_index()
#Sort the month-year by time order
group_by_month = group_by_month.sort_values(by = ['month_year'])
group_by_month['month_year'] = group_by_month['month_year'].astype('str')
print(group_by_month.head())

#Create subplot
sns.set_style('whitegrid')
fig,ax=plt.subplots(figsize=(16,7))

#Create lineplot
chart=sns.lineplot(x=group_by_month['month_year'], y=group_by_month['Member_number'],ax=ax)
sns.despine(left=True)

#Customize chart
chart.set_xlabel('Period',weight='bold',fontsize=13)
chart.set_ylabel('Total Unique Customer', weight='bold',fontsize=13)
chart.set_title('Monthly Unique Customers',weight='bold',fontsize=16)
chart.set_xticklabels(group_by_month['month_year'], rotation = 45, ha="right")

ymin, ymax = ax.get_ylim()
bonus = (ymax - ymin)/28# still hard coded bonus but scales with the data
for x, y, name in zip(group_by_month['month_year'], group_by_month['Member_number'], group_by_month['Member_number'].astype('str')):
    ax.text(x, y + bonus, name, color = 'black', ha='center')

plt.show()


# bar chart
#Count and group by category
category = df.groupby('itemDescription').agg({'Member_number':'count'}).rename(columns={'Member_number':'total sale'}).reset_index()

#Get 10 first categories
category2 = category.sort_values(by=['total sale'], ascending = False).head(10)
print(category2.head())

#Horizontal barchart
#Create subplot
sns.set_style('darkgrid') #set theme
fig,ax=plt.subplots(figsize=(16,7))

#Create barplot
chart2 = sns.barplot(x=category2['total sale'],y=category2['itemDescription'], palette=sns.cubehelix_palette(len(x)))

#Customize chart
chart2.set_xlabel('Total Sale',weight='bold',fontsize=13)
chart2.set_ylabel('Item Name', weight='bold',fontsize=13)
chart2.set_title('Best Sellers',weight='bold',fontsize=16)

#Value number on chart
for p in ax.patches:
    width = p.get_width()    # get bar length
    ax.text(width + 1,       # set the text at 1 unit right of the bar
            p.get_y() + p.get_height() / 2, # get Y coordinate + X coordinate / 2
            '{:1.0f}'.format(width), # set variable to display
            ha = 'left',   # horizontal alignment
            va = 'center')  # vertical alignment

plt.show()
