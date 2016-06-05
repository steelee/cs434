import numpy
import statsmodels.api as sm
# from numpy import matrix, polyfit

# build the matricies, adding a ones column
# to x for higher precision
x = numpy.loadtxt('../sample_features.csv', delimiter="," , ndmin=2)
o = numpy.ones((x.shape[0],1))
x = numpy.concatenate((x, o), axis=1)
y = numpy.loadtxt('../sample_target.csv', delimiter=",", ndmin=2)

with open('out.txt', 'w') as f:
	results = sm.OLS(y, x).fit().summary().as_text()
	f.write(results)
	f.write("\n")