import numpy as np
import csv as csv

csv_file_object = csv.reader(open('./csv/train.csv', 'rb'))
header = csv_file_object.next()
data = []

for row in csv_file_object:
	data.append(row)
data = np.array(data)


# So we add the ceiling
fare_ceiling = 40

# Then modify the data in the Fare column to = 39, if it is greater or equal to the ceiling
data[data[0::,9].astype(np.float) >= fare_ceiling, 9] = fare_ceiling - 1.0

fare_bracket_size = 10
number_of_price_brackets = fare_ceiling / fare_bracket_size

# I know there were 1st, 2nd, 3rd classes on the board
number_of_classes = 3

# But it's better practice to calculate this from the data directly
# Take the length of any array of unique values in column index 2
number_of_classes = len(np.unique(data[0::, 2]))

# Initialize the survival table with all zeros 2*3*4 matrix
survival_table = np.zeros((2, number_of_classes, number_of_price_brackets))

print survival_table
# data[ where function, 1] means it's finding the second column for the conditional criteria
for i in xrange(number_of_classes):				# Loop through each class
	for j in xrange(number_of_price_brackets):	# Loop through each price bin

		women_only_stats = data[
			(data[0::, 4] == 'female')										# Which element is a female
			& (data[0::, 2].astype(np.float) == i + 1)						# and was in ith class
			& (data[0::, 9].astype(np.float) > j * fare_bracket_size)		# was greater than this bin
			& (data[0::, 9].astype(np.float) < (j + 1) * fare_bracket_size)	# and less than the next bin
			, 1
		]

		men_only_stats = data[
			(data[0::, 4] != 'female')
			& (data[0::, 2].astype(np.float) == i + 1)
			& (data[0::, 9].astype(np.float) > j * fare_bracket_size)
			& (data[0::, 9].astype(np.float) < (j + 1 ) * fare_bracket_size)
			, 1
		]

		survival_table[0, i, j] = np.mean(women_only_stats.astype(np.float))
		survival_table[1, i, j] = np.mean(men_only_stats.astype(np.float))

survival_table[ survival_table != survival_table ] = 0.
print survival_table

# Update our survival_table
survival_table[survival_table < 0.5] = 0
survival_table[survival_table >= 0.5] = 1
print survival_table

'''Predict'''
test_file = open('./csv/test.csv', 'rU')
test_file_object = csv.reader(test_file)
header = test_file_object.next()
prediction_file = open('./csv/genderclassmodel.csv', 'wb')
prediction_file_object = csv.writer(prediction_file)

prediction_file_object.writerow(['PassengerId', 'Survived'])

for row in test_file_object:							# We are going to loop
														# through each passenger in the test set
	for j in xrange(number_of_price_brackets):			# For each passenger we 
														# loop thro each price bin
		try:											# Some passengers have no
														# fare data so try to
			row[8] = float(row[8])						# make a float
		except:											# If fails: no data, so
			bin_fare = 3 - float(row[1])				# bin the fare according Pclass
			break										# break from the loop
		if row[8] > fare_ceiling:						# If there is data see if
														# it's greater than fare
														# ceiling we set eariler
			bin_fare = number_of_price_brackets - 1     # If so, set to highest bin
			break										# and then break loop
		if row[8] >= j * fare_bracket_size\
					and row[8] <\
					(j + 1) * fare_bracket_size:		# If passed these tests
														# then loop thro each bin
			bin_fare = j								# then assign index
			break
	if row[3] == 'female':										# If the passenger if female
		prediction_file_object.writerow([row[0], '%d' % \
			int(survival_table[0, float(row[1])-1, bin_fare])])
	else:														# else if male
		prediction_file_object.writerow([row[0], '%d' % \
			int(survival_table[1, float(row[1])-1, bin_fare])])
# Close out the files
test_file.close()
prediction_file.close()

