import numpy as np

def makeham_mort(x, t, A = 0.00022, B = 2.7e-6, c = 1.124):
	return np.exp(-(A * t + B * (c ** x) * (c ** t - 1.0) / np.log(c)))    


