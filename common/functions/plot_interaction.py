from pylab import ginput
from numpy import array, abs, floor, sum, size

def extract_pop(histo, nbr_pic, width) :
    result = []
    X = ginput(nbr_pic)
    size_hist = size(histo[1])
    Xmin = histo[1][0]
    Xmax = histo[1][-1]
    step = 1.0 * abs(Xmax-Xmin)/size_hist
    for i in range(nbr_pic) :
        center = floor(abs(X[i][0] - Xmin)/step)
        result.append(sum(histo[0][center-width:center+width]))
    return [result, 1.0*array(result) / sum(result)]

