import pandas as pd
import numpy as np
# For .read_csv, always use header = 0 when you know row 0 is the header row
df = pd.read_csv('./csv/train.csv', header = 0)

print df			# Print the DataFrame
print df.head(3)	# Print the first 3 datas of the DataFrame
print df.tail(3)	# Print the last 3 datas of the DataFrame
print df.dtypes		# Data type
print df.info()		# Column information
print df.describe()	# Some stats of the datas


'''Data Munging'''
print '=================================='
print df['Age'][0:10]	# Print the first 10 rows of Age
print df.Age[0:10]		# The alternative syntax
print df['Cabin'] 		# Print the column Cabin
print type(df['Age'])	# a single column is neither an numpy array nor a pandas dataframe, but rather pandas specific object called a data Series
print df['Age'].mean()	# print the mean of column Age
print df.Age.mean()		# with alternative syntax
print df['Age'].median()	# Print the median of Age

print df[['Sex', 'Pclass', 'Age']]								# Get the subset
print df[df['Age'] > 60]										# Filter the dataset
print df[df['Age'] > 60][['Sex', 'Pclass', 'Age']]				# Get the subset that is filtered
print df[df['Age'].isnull()][['Sex', 'Pclass', 'Age']]			# .isnull() to check wether is missing

for each_class in range(1, 4):															# Print the count of men
	print each_class, len(df[(df['Sex'] == 'male') & (df['Pclass'] == each_class)])		# in each class

import pylab as P 				# Derive a histogram of any numerical column
df['Age'].hist()
#P.show()

df['Age'].dropna().hist(bins = 16, range = (0, 80), alpha = .5)		# Explicit the options of the function
#P.show()															# also drop the missing value

print '====================================='
df['Gender'] = 4					# Adding a new column by naming it and passing it a value
print df.head()
df['Gender'] = df['Sex'].map(lambda x: x[0].upper())		# You can put dict, series, and function as .map's param
print df['Gender']
df['Gender'] = df['Sex'].map({'female': 0, 'male': 1}).astype(int)
print df['Gender']

# In order to replace the missing value by median of ages
median_ages = np.zeros((2, 3))
for gender in range(0, 2):
	for each_class in range(0, 3):
		median_ages[gender, each_class] = df[(df['Gender'] == gender) & \
											(df['Pclass'] == each_class + 1)]['Age'].dropna().median()
print median_ages

df['AgeFill'] = df['Age']
print df[df['Age'].isnull()][['Gender', 'Pclass', 'Age', 'AgeFill']].head(10)

for i in range(0, 2):
	for j in range(0, 3):
		df.loc[								# .loc[row_indexer, column_indexer]
			(df.Age.isnull())
			& (df.Gender == i)
			& (df.Pclass == j + 1),
			'AgeFill'
		] = median_ages[i, j]

print df[df['Age'].isnull()][['Gender', 'Pclass', 'Age', 'AgeFill']].head(10)

df['AgeIsNull'] = pd.isnull(df.Age).astype(int)
df['FamilySize'] = df['SibSp'] + df['Parch']
df['Age*Class'] = df['AgeFill'] * df['Pclass']

df = df.drop(['Name', 'Sex', 'Ticket', 'Cabin', 'Embarked', 'Age'], axis = 1)		# Drop the columns which we will not use
df = df.dropna()			# Drop any rows which still have missing value

train_data = df.values		# Convert into a Numpy array by using .values method
print train_data

print '===================================='
print 'Creating csv file ...'
df.to_csv('new_train.csv')
print 'Done!'