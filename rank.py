import itertools
import numpy as np
import pylab as pl

from sklearn import svm, linear_model, cross_validation

def check_percent(data):
    rank = {0:0.0, 1:0.0, 2:0.0, 3:0.0, 4:0.0, 5:0.0, 6:0.0}
    for count in range(len(data)):
         rank[data[count]] = rank[data[count]] + 1 
    for count in range(0,len(rank)):
         rank[count] = rank[count]/len(data)
    return rank

def transform_pairwise(X, y):
    X_new = []
    y_new = []
    y = np.asarray(y)
    if y.ndim == 1:
        y = np.c_[y, np.ones(y.shape[0])]
    comb = itertools.combinations(range(X.shape[0]), 2)
    for k, (i, j) in enumerate(comb):
        if y[i, 0] == y[j, 0] or y[i, 1] != y[j, 1]:
            continue
        X_new.append(X[i] - X[j])
        y_new.append(np.sign(y[i, 0] - y[j, 0]))
        if y_new[-1] != (-1) ** k:
            y_new[-1] = - y_new[-1]
            X_new[-1] = - X_new[-1]
    return np.asarray(X_new), np.asarray(y_new).ravel()


class RankSVM(svm.LinearSVC):
    def fit(self, X, y):
        X_trans, y_trans = transform_pairwise(X, y)
        super(RankSVM, self).fit(X_trans, y_trans)
        return self

    def predict(self, X):
        if hasattr(self, 'coef_'):
            np.argsort(np.dot(X, self.coef_.T))
        else:
            raise ValueError("Must call fit() prior to predict()")

    def score(self, X, y):
        X_trans, y_trans = transform_pairwise(X, y)
        return np.mean(super(RankSVM, self).predict(X_trans) == y_trans)


if __name__ == '__main__':
    data = np.loadtxt('training_features.csv', delimiter=',')
    n_samples = len(data)
    n_features = len(data[0])
    true_coef = np.random.randn(n_features)
    X = data 
    noise = np.random.randn(n_samples) / np.linalg.norm(true_coef)
    y = np.loadtxt('training_target.csv',delimiter=",") 
    ratios = check_percent(y)
    y = np.arctan(y)
    y += .05 * noise 
    Y = np.c_[y, np.mod(np.arange(n_samples), 5)]
    cv = cross_validation.KFold(n_samples, 5)
    train, test = iter(cv).next()
    pl.scatter(np.dot(X, true_coef), y,)
    pl.title('League of Legends Ranking')
    pl.xlabel('Confidence')
    pl.ylabel('Ranking As Average')
    pl.show()

    rank_svm = RankSVM().fit(X[train], Y[train])
    print 'Performance of ranking ', rank_svm.score(X[test], Y[test])

    ridge = linear_model.RidgeCV(fit_intercept=True)
    ridge.fit(X[train], y[train])
    X_test_trans, y_test_trans = transform_pairwise(X[test], y[test])
    score = np.mean(np.sign(np.dot(X_test_trans, ridge.coef_)) == y_test_trans)
    print 'Performance of linear regression ', score

    print 'Real placement ratios in file:'
    print ratios
