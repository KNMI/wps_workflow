# python
# KNMI clipc
# author: andrej
# clipc@knmi.nl
import numpy as np

# normalisation functions
#
# normalisation functions 
# requested by johannes
#

def norm(X,normCommandType):
	return nrm[normCommandType](X)

def none(X):
	return X

def norm0(X):
	return np.zeros(X.shape) 
	
# min max normalisation
# also feature scaling...
def normA(X):
	minX = np.min(X)
	maxX = np.max(X)

	return ((X -  minX ) / ( maxX - minX ))

# normalisation by standardisation
# standard score
def normB(X):
	meanX = np.mean(X)
	stdX  = np.std(X)

	return (X - meanX) / stdX

# norm by percentiles...
def normC(X):
	return 0

nrm = { "normnone" : none ,
		"normzero" : norm0 ,
		"normminmax": normA , 
        "normstndrd": normB }