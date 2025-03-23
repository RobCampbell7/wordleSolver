import sys
from wordleSim import averageRun, easisestWord, hardestWord
import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import norm
from warnings import catch_warnings, simplefilter
from sklearn.gaussian_process import GaussianProcessRegressor
from math import sin, pi

# YELLOW WEIGHT SET TO 1
# objective = lambda x : averageRun(x, 1, 2000)
COUNT = 0
def objective(x):
    global COUNT
    COUNT += 1
    x = averageRun(x, 1, 2000)
    return x

def surrogate(model, X):
	with catch_warnings():
		simplefilter("ignore")
		return model.predict(X, return_std=True)

def acquisition(X, Xsamples, model):
	yhat, _ = surrogate(model, X)
	best = min(yhat)
	# calculate mean and stdev via surrogate function
	mu, std = surrogate(model, Xsamples)
	mu = mu.flatten()
	# calculate the probability of improvement
	probs = norm.cdf((mu - best) / (std+1E-9))
	return probs
 
def optAcquisition(X, y, model):
	# random search, generate random samples
	Xsamples = np.random.random(100)
	Xsamples = Xsamples.reshape(len(Xsamples), 1)
	# calculate the acquisition function for each sample
	scores = acquisition(X, Xsamples, model)
	# locate the index of the largest scores
	ix = np.argmax(scores)
	return Xsamples[ix, 0]
 
def plot(X, y, model):
	# scatter plot of inputs and real objective function
	plt.plot(X, y, "rx")
	# line plot of surrogate function across domain
	Xsamples = np.asarray(np.arange(0, 1, 0.001))
	Xsamples = Xsamples.reshape(len(Xsamples), 1)
	ysamples, _ = surrogate(model, Xsamples)
	plt.plot(Xsamples, ysamples, "k-")
	# show the plot
	plt.show()

if __name__=="__main__":
    X = np.random.random(100)
    y = np.asarray([objective(x) for x in X])
    print("Domain sampled")

    X = X.reshape(len(X), 1)
    y = y.reshape(len(y), 1)

    model = GaussianProcessRegressor()
    model.fit(X, y)

    for i in range(100):
        x = optAcquisition(X, y, model)
        actual = objective(x)
        est, _ = surrogate(model, [[x]])
        print("i={0}, x={1:.3f}, f()={2:3f}, actual={3:.3f}, c={4}".format(i, x, est[0], actual, COUNT))

        X = np.vstack((X, [[x]]))
        y = np.vstack((y, [[actual]]))
    
        model.fit(X, y)

    plot(X, y, model)
    # best result
    ix = np.argmin(y)
    print('Best Result: x=%.3f, y=%.3f' % (X[ix], y[ix]))
    
    # Best Result: x=0.396, y=4.705