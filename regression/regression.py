import numpy
import statsmodels.api as sm

# build the matricies, adding a ones column
# to x for higher precision
x = numpy.loadtxt('../sample_features.csv', delimiter="," , ndmin=2)
o = numpy.ones((x.shape[0],1))
x = numpy.concatenate((x, o), axis=1)
y = numpy.loadtxt('../sample_target.csv', delimiter=",", ndmin=2)

# perform a linear regresion on the data
results = sm.OLS(y, x).fit()
weights = results.params
summary = results.summary().as_text()

with open('linear_out.txt', 'w') as f:
	f.write(summary)
	f.write("\n")

# determine the success rate of the algorithm
success = 0
failure = 0
for i in range(x.shape[0]):
	val = int(numpy.round(numpy.dot(weights, x[i])))
	if val == y[i]:
		success += 1
	else:
		failure += 1

total = success + failure
percent_correct = int((float(success) / float(failure)) * 100)
print "success\tfailure\ttotal\tpercent correct"
print "{0}\t{1}\t{2}\t{3}%".format(success, failure, total, percent_correct)

# break down placement
placement_matrix = numpy.zeros((6,6), dtype=numpy.int)
for i in range(x.shape[0]):
	val = int(numpy.round(numpy.dot(weights, x[i])))
	placement_matrix[int(y[i]),val] += 1

print "placement matrix"
print placement_matrix