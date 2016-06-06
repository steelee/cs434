import numpy
import sys
import statsmodels.api as sm

def build_matricies(t):
	if t == 'train':
		f_f = '../training_features.csv'
		f_t = '../training_target.csv'
	elif t == 'test':
		f_f = '../testing_features.csv'
		f_t = '../testing_target.csv'
	else:
		print "Bad argument to build_matricies!"
		sys.exit()

	x = numpy.loadtxt(f_f, delimiter=",", ndmin=2)
	o = numpy.ones((x.shape[0],1))
	x = numpy.concatenate((x, o), axis=1)
	y = numpy.loadtxt(f_t, delimiter=",", ndmin=2)

	return x,y

# build the matricies, adding a ones column
# to x for higher precision
x,y = build_matricies('train')

# perform a linear regresion on the data
# OLS is our object model, and fit() executes
model   = sm.OLS(y, x)
results = model.fit_regularized()
weights = results.params
pred    = model.predict(weights)
summary = results.summary().as_text()

with open('linear_out.txt', 'w') as f:
	f.write(summary)
	f.write("\n")

# determine the success rate of the algorithm
# this involves changing the 
x,y = build_matricies('test')
success = 0
failure = 0

for i in range(x.shape[0]):
	val = int(numpy.round(numpy.dot(weights, x[i])))
	yv  = int(y[i])

	if val == yv:
		success += 1
	else:
		failure += 1

total           = success + failure
percent_correct = int((float(success) / float(total)) * 100)
print "success\tfailure\ttotal\tpercent correct"
print "{0}\t{1}\t{2}\t{3}%".format(success, failure, total, percent_correct)

# break down placement
# row is where they should be placed,
# column is where they ended up being placed
placement_matrix = numpy.zeros((7,7), dtype=numpy.int)
for i in range(x.shape[0]):
	val = int(numpy.round(numpy.dot(weights, x[i])))
	try:
		placement_matrix[int(y[i]),val] += 1
	except:
		continue

print "placement matrix"
print placement_matrix
