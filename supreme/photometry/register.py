import numpy as np

def photometric_adjust(source, target):
    """Adjust the intensity of source to look like target.

    Parameters
    ----------
    source, target : ndarray
        Source and target images.

    Returns
    -------
    a, b : float
        Adjustment factors so that ``source * a + b`` approximates
        target.

    """
    mask = (source > 10) & (target > 10) & (source < 210) & (target < 210)

    mu_s = np.mean(source[mask])
    std_s = np.std(source[mask])
    mu_t = np.mean(target[mask])
    std_t = np.std(target[mask])

    a = std_t / std_s
    b = (mu_t * std_s - mu_s * std_t)/std_s

    return a, b

def histogram_adjust(source, target):
    """Transform the histogram of the source so that it is similar
    to that of the target.

    Parameters
    ----------
    source, target = ndarray
        Source and target images.

    Returns
    -------
    source_adj : callable, f(x)
        When applied to the source image, an image with similar response
        to target is generated.

    """
    s_hist, s_edges = np.histogram(source, bins=256)
    t_hist, t_edges = np.histogram(target, bins=256)

    s_edges = s_edges[:-1]
    t_edges = t_edges[:-1]

    s_cum = np.cumsum(s_hist)
    t_cum = np.cumsum(t_hist)

    mapping = np.argmin(np.abs(t_cum - s_cum[:, None]), axis=1)

#    import matplotlib.pyplot as plt
#    plt.plot(mapping)
#    plt.show()

    def tf(source):
        sshape = source.shape
        source = source.flat
        source = source/np.max(source) * (len(s_edges) - 1)
        source = np.clip(np.round(source), 0, len(s_edges) - 1).astype(int)

        return t_edges[mapping[source]].reshape(sshape) + \
               (t_edges[1] - t_edges[0])/2.

    return tf
