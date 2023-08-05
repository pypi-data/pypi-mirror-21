"""Peak detection algorithms."""

import warnings

import numpy as np
from scipy import optimize
from scipy.integrate import simps

eps = np.finfo(float).eps

def indexes(y, thres=0.3, min_dist=1):
    """Peak detection routine.

    Finds the numeric index of the peaks in *y* by taking its first order difference. By using
    *thres* and *min_dist* parameters, it is possible to reduce the number of
    detected peaks. *y* must be signed.

    Parameters
    ----------
    y : ndarray (signed)
        1D amplitude data to search for peaks.
    thres : float between [0., 1.]
        Normalized threshold. Only the peaks with amplitude higher than the
        threshold will be detected.
    min_dist : int
        Minimum distance between each detected peak. The peak with the highest
        amplitude is preferred to satisfy this constraint.

    Returns
    -------
    ndarray
        Array containing the numeric indexes of the peaks that were detected
    """
    if isinstance(y, np.ndarray) and np.issubdtype(y.dtype, np.unsignedinteger):
        raise ValueError("y must be signed")

    thres = thres * (np.max(y) - np.min(y)) + np.min(y)
    min_dist = int(min_dist)

    # compute first order difference
    dy = np.diff(y)

    # propagate left and right values successively to fill all plateau pixels (0-value)
    zeros,=np.where(dy == 0)
    
    while len(zeros):
        # add pixels 2 by 2 to propagate left and right value onto the zero-value pixel
        zerosr = np.hstack([dy[1:], 0.])
        zerosl = np.hstack([0., dy[:-1]])

        # replace 0 with right value if non zero
        dy[zeros]=zerosr[zeros]
        zeros,=np.where(dy == 0)

        # replace 0 with left value if non zero
        dy[zeros]=zerosl[zeros]
        zeros,=np.where(dy == 0)

    # find the peaks by using the first order difference
    peaks = np.where((np.hstack([dy, 0.]) < 0.)
                     & (np.hstack([0., dy]) > 0.)
                     & (y > thres))[0]

    if peaks.size > 1 and min_dist > 1:
        highest = peaks[np.argsort(y[peaks])][::-1]
        rem = np.ones(y.size, dtype=bool)
        rem[peaks] = False

        for peak in highest:
            if not rem[peak]:
                sl = slice(max(0, peak - min_dist), peak + min_dist + 1)
                rem[sl] = True
                rem[peak] = False

        peaks = np.arange(y.size)[~rem]

    return peaks


def centroid(x, y):
    """Computes the centroid for the specified data.
    Refer to centroid2 for a more complete, albeit slower version.

    Parameters
    ----------
    x : ndarray
        Data on the x axis.
    y : ndarray
        Data on the y axis.

    Returns
    -------
    float
        Centroid of the data.
    """
    return np.sum(x * y) / np.sum(y)

def centroid2(y, x=None, dx=1.):
    """Computes the centroid for the specified data.
    Not intended to be used

    Parameters
    ----------
    y : array_like
        Array whose centroid is to be calculated.
    x : array_like, optional
        The points at which y is sampled.
    Returns
    -------
    (centroid, sd)
        Centroid and standard deviation of the data.
    """
    yt = np.array(y)

    if x is None:
        x = np.arange(yt.size, dtype='float') * dx

    normaliser = simps(yt, x)
    centroid = simps(x * yt, x) / normaliser
    var = simps((x - centroid) ** 2 * yt, x) / normaliser
    return centroid, np.sqrt(var)

def gaussian(x, ampl, center, dev):
    """Computes the Gaussian function.

    Parameters
    ----------
    x : number
        Point to evaluate the Gaussian for.
    a : number
        Amplitude.
    b : number
        Center.
    c : number
        Width.

    Returns
    -------
    float
        Value of the specified Gaussian at *x*
    """
    return ampl * np.exp(-(x - float(center)) ** 2 / (2.0 * dev ** 2 + eps))

def gaussian_fit(x, y, center_only=True):
    """Performs a Gaussian fitting of the specified data.

    Parameters
    ----------
    x : ndarray
        Data on the x axis.
    y : ndarray
        Data on the y axis.
    center_only: bool
        If True, returns only the center of the Gaussian for `interpolate` compatibility

    Returns
    -------
    ndarray or float
        If center_only is `False`, returns the parameters of the Gaussian that fits the specified data
        If center_only is `True`, returns the center position of the Gaussian
    """
    if len(x) < 3:
        # used RuntimeError to match errors raised in scipy.optimize
        raise RuntimeError("At least 3 points required for Gaussian fitting")

    initial = [np.max(y), x[0], (x[1] - x[0]) * 5]
    params, pcov = optimize.curve_fit(gaussian, x, y, initial)

    if center_only:
        return params[1]
    else:
        return params


def interpolate(x, y, ind=None, width=10, func=gaussian_fit):
    """Tries to enhance the resolution of the peak detection by using
    Gaussian fitting, centroid computation or an arbitrary function on the
    neighborhood of each previously detected peak index.
    
    RuntimeErrors raised in the fitting function will be converted to warnings, with the peak
    being mantained as the original one (in the ind array).

    Parameters
    ----------
    x : ndarray
        Data on the x dimension.
    y : ndarray
        Data on the y dimension.
    ind : ndarray
        Indexes of the previously detected peaks. If None, indexes() will be
        called with the default parameters.
    width : int
        Number of points (before and after) each peak index to pass to *func*
        in order to increase the resolution in *x*.
    func : function(x,y)
        Function that will be called to detect an unique peak in the x,y data.

    Returns
    -------
    ndarray :
        Array with the adjusted peak positions (in *x*)
    """
    assert x.shape == y.shape
    
    if ind is None:
        ind = indexes(y)

    out = []
    
    for i in ind:
        slice_ = slice(i - width, i + width + 1)
        
        try:
            best_idx = func(x[slice_], y[slice_])
        except RuntimeError as e:
            warnings.warn(str(e))
            best_idx = i

        out.append(best_idx)

    return np.array(out)
