#
# Metrics for scoring predictions and also some more specialized
# math needed for skedm


import numpy as np
from scipy import stats as stats
from numba import jit



def weighted_mean(X, distances):
    """Calculates the weighted mean given a set of values and their corresponding
    distances.

    Only 1/distance is implemented. This essentially is just a weighted mean
    down axis=1.

    Parameters
    ----------
    X : 2d array
        Training values of shape(nsamples,number near neighbors).
    distances : 2d array
        Sorted distances to the near neighbors for the indices.
        Shape(nsamples,number near neighbors).

    Returns
    -------
    w_mean : 2d array
        Weighted predictions.

    """
    distances = distances+0.00001 #ensures no zeros when dividing

    W = 1./distances
    denom = np.sum(W, axis=1,keepdims=True)
    W/=denom

    w_mean = np.sum(X * W, axis=1)

    return w_mean.ravel()


def mi_digitize(X):
    """Digitize a time series for mutual information analysis

    Parameters
    ----------
    X : 1D array
        Array to be digitized of length m.

    Returns
    -------
    Y : 1D array
        Digitized array of length m.
    """

    minX = np.min(X) - 1e-5 #subtract for correct binning
    maxX = np.max(X) + 1e-5 #add for correct binning

    nbins = int(np.sqrt(len(X)/20))
    nbins = max(4,nbins) #make sure there are atleast four bins
    bins = np.linspace(minX, maxX, nbins+1) #add one for correct num bins

    Y = np.digitize(X, bins)

    return Y


def corrcoef(preds, actual):
    """Correlation Coefficient of between predicted values and actual values

    Parameters
    ----------
    preds : 1D array
        Predicted values of shape (num samples,).
    test : 1D array
        Actual values from the testing set of shape (num samples,).

    Returns
    -------
    cc : float
        Returns the correlation coefficient.

    """

    cc = np.corrcoef(preds,actual)[1,0]

    return cc


def class_compare(preds, actual):
    """Percent correct between predicted values and actual values.

    Parameters
    ----------
    preds : 1D array
        Predicted values of shape (num samples,).
    actual : 1D array
       Actual values from the testing set. Shape (num samples,).

    Returns
    -------
    cc : float
       Returns the correlation coefficient.

    """

    cc = np.mean( preds == actual )

    return cc

def classification_error(preds, actual):
    """Percent correct between predicted values and actual values scaled
    to the most common prediction of the space.

    Parameters
    ----------
    preds : 1D array
        Predicted values of shape (num samples,).
    actual : 1D array
       Actual values of shape (num samples,).

    Returns
    -------
    cc : float
       Returns the correlation coefficient

    """

    most_common,_=stats.mode(actual,axis=None)

    num = np.mean(preds == actual)
    denom = np.mean(actual == most_common)

    cc = num/denom.astype('float')

    return cc

def kleckas_tau(preds, actual):
    """
    Calculates kleckas tau

    Parameters
    ----------
    preds : 1D array
        Predicted values of shape (num samples,).
    actual : 1D array
        Actual values of shape (num samples,).

    Returns
    -------
    tau : float
    	Returns kleckas tau
    """

    ncorr = np.sum(preds == actual) #number correctly classified
    cats_unique = np.unique(actual)

    sum_t = 0
    for cat in cats_unique:
        ni = np.sum(cat==actual)
        pi = float(ni)/len(preds)
        sum_t += ni*pi


    tau = (ncorr - sum_t) / (len(preds) - sum_t)

    return tau

def cohens_kappa(preds, actual):
    """Calculates cohens kappa.

    Parameters
    ----------
    preds : 1D array
        Predicted values of shape (num samples,).
    test : array of shape (num samples,)
        Actual values from the testing set.

    Returns
    -------
    c : float
        Returns the cohens_kappa.
    """

    c = cohen_kappa_score(preds,actual)

    return c

def klekas_tau_spatial(X, max_lag, percent_calc=.5):
    """Calculates the kleckas tau value between a shifted and unshifted slice
    of the space.

    Parameters
    ----------
    X : 2D array
        Spatail image.
    max_lag : integer
        Maximum amount to shift the space.
    percent_calc : float
        How many rows and columns to use average over. Using the whole space
        is overkill.

    Returns
    -------
    R_mut : 1D array
        Klekas tau averaged down the rows (vertical).
    C_mut : 1-D array
        Klekas tau averaged across the columns (horizontal).
    r_mi : 2-D array
        Klekas tau down each row (vertical).
    c_mi : 2-D array
        Klekas tau across each columns (horizontal).

    """

    rs, cs = np.shape(X)

    rs_iters = int(rs*percent_calc)
    cs_iters = int(cs*percent_calc)

    r_picks = np.random.choice(np.arange(rs),size=rs_iters,replace=False)
    c_picks = np.random.choice(np.arange(cs),size=cs_iters,replace=False)


    # The r_picks are used to calculate the MI in the columns
    # and the c_picks are used to calculate the MI in the rows

    c_mi = np.zeros((max_lag,rs_iters))
    r_mi = np.zeros((max_lag,cs_iters))

    for ii in range(rs_iters):

        m_slice = X[r_picks[ii],:]

        for j in range(max_lag):

            shift = j+1
            new_m = m_slice[:-shift]
            shifted = m_slice[shift:]
            c_mi[j,ii] = kleckas_tau(new_m, shifted)

    for ii in range(cs_iters):

        m_slice = X[:,c_picks[ii]]

        for j in range(max_lag):
            shift = j+1
            new_m = m_slice[:-shift]
            shifted = m_slice[shift:]
            r_mi[j,ii] = kleckas_tau(new_m,shifted)

    r_mut = np.mean(r_mi,axis=1)
    c_mut = np.mean(c_mi,axis=1)

    return r_mut, c_mut, r_mi, c_mi


def variance_explained(preds, actual):
    """Explained variance between predicted values and actual values.

    Parameters
    ----------
    preds : 1D array
        Predict values of shape (num samples,).
    actual : 1D array
        Actual values of shape (num samples,).

    Returns
    -------
    cc : float
        Returns the correlation coefficient

    """

    cc = np.var(preds - actual) / np.var(actual)

    return cc


def score(preds, actual):
    """Calculates the coefficient of determination.

    The coefficient R^2 is defined as (1 - u/v), where u is the regression
    sum of squares ((y_true - y_pred) ** 2).sum() and v is the residual
    sum of squares ((y_true - y_true.mean()) ** 2).sum(). Best possible
    score is 1.0, lower values are worse.

    Parameters
    ----------
    preds : 1D array
        Predicted values of shape (num samples,)
    test : 1D array
        Actual values of shape (num samples,)

    Returns
    -------
    cc : float
        Returns the coefficient of determination.
    """

    u = np.square(actual - preds ).sum()
    v = np.square(actual - actual.mean()).sum()
    r2 = 1 - u/v

    if v == 0.:
        print('Targets are all the same. Returning 0.')
        r2=0
    return r2


def weighted_mode(a, w, axis=0):
    """This function is borrowed from sci-kit learn's extmath.py

    Returns an array of the weighted modal (most common) value in a

    If there is more than one such value, only the first is returned.
    The bin-count for the modal bins is also returned.

    This is an extension of the algorithm in scipy.stats.mode.

    Parameters
    ----------
    a : array_like
        n-dimensional array of which to find mode(s).
    w : array_like
        n-dimensional array of weights for each value.
    axis : int, optional
        Axis along which to operate. Default is 0, i.e. the first axis.

    Returns
    -------
    vals : ndarray
        Array of modal values.
    score : ndarray
        Array of weighted counts for each mode.

    Examples
    --------
    >>> from sklearn.utils.extmath import weighted_mode
    >>> x = [4, 1, 4, 2, 4, 2]
    >>> weights = [1, 1, 1, 1, 1, 1]
    >>> weighted_mode(x, weights)
    (array([ 4.]), array([ 3.]))

    The value 4 appears three times: with uniform weights, the result is
    simply the mode of the distribution.

    >>> weights = [1, 3, 0.5, 1.5, 1, 2] # deweight the 4's
    >>> weighted_mode(x, weights)
    (array([ 2.]), array([ 3.5]))

    The value 2 has the highest score: it appears twice with weights of
    1.5 and 2: the sum of these is 3.

    See Also
    --------
    scipy.stats.mode
    """
    if axis is None:
        a = np.ravel(a)
        w = np.ravel(w)
        axis = 0
    else:
        a = np.asarray(a)
        w = np.asarray(w)
        axis = axis

    if a.shape != w.shape:
        print('both weights')
        w = np.zeros(a.shape, dtype=w.dtype) + w

    scores = np.unique(np.ravel(a))       # get ALL unique values
    testshape = list(a.shape)
    testshape[axis] = 1
    oldmostfreq = np.zeros(testshape)
    oldcounts = np.zeros(testshape)

    for score in scores:
        template = np.zeros(a.shape)
        ind = (a == score)
        template[ind] = w[ind]
        counts = np.expand_dims(np.sum(template, axis), axis)
        mostfrequent = np.where(counts > oldcounts, score, oldmostfreq)
        oldcounts = np.maximum(counts, oldcounts)
        oldmostfreq = mostfrequent

    return mostfrequent, oldcounts




@jit
def quick_mode_axis1(X):
    """Takes the mode of an array across the columns or along axis=1.

    Parameters
    ----------
    X : 2D array
        Array of which of which to find the modes.

    Returns
    -------
    mode : 1D array
        Modes down the first axis. Shape (nrows,)
    """

    X = X.astype(int)
    len_x = len(X)
    mode = np.zeros(len_x)
    for i in range(len_x):
        mode[i] = np.bincount(X[i,:]).argmax()
    return mode

@jit
def quick_mode_axis1_keep_nearest_neigh(X):
    """Mode calculation that takes into consideration the ordering of the
    elements. If there is a tie, the closest element will be chosen.

    For example if the neighbors have values:
    [7,7,2,3,4,1,1] the current implementation will keep 1 as the value. For
    our purposes, the ordering is important, so we want to keep the first value.

    Parameters
    ----------
    X : 2D array
        Array of which of which to find the modes.

    Returns
    -------
    mode : 1D array
        Modes down the first axis. Shape (nrows,)
    """

    X = X.astype(int)
    len_x = len(X)
    mode = np.zeros(len_x)
    for i in range(len_x):
        loc = np.bincount(X[i,:])[X[i,:]].argmax() #reorder before argmax
        mode[i] = X[i,:][loc]
    return mode

def keep_diversity(X, thresh=1.):
    """Returns indices where the columns are not a single class.

    Parameters
    ----------
    X : 2d array of ints
        Array to evaluate for diversity
    thresh : float
        Percent of species that need to be unique.

    Returns
    -------
    keep : 1d boolean array
        Array where true means there is more than one class in that row.

    Examples
    --------

    >>> x = np.array([[1 1 1 1]
    [2 1 2 3]
    [2 2 2 2]
    [3 2 1 4]])
    >>> keep_diversity(x)
    array([F,T,F,T])

    """

    X = X.astype(int)
    mode = quick_mode_axis1(X).reshape(-1,1)

    compare = np.repeat(mode,X.shape[1],axis=1)
    thresh = int(thresh*X.shape[1])
    keep = np.sum(compare==X, axis=1) < X.shape[1]

    return keep
