from numpy import sign, sin, cos, size, array
from scipy import integrate
from pylab import plot, ginput, figure

def colarray(data, colnum, rem):
    """
    This function give back the column of an array given the array and the column number to be extracted.
    The third parameter allow to get ride of the first terms of the column.
    """
    temp = []
    for i in range( len(data) - rem):
        temp.append(data[i+rem][colnum-1])
    return temp


def colarray_pol(data, A, B, theta):
    """
    This function is dedicated to the polarplot in oder to take into account the signe of the magnetic field in the trace - retrace pot
    """
    temp = []
    for i in range( len(data)):
        temp.append(data[i][1] * sign(data[i][0]) - A*abs(sin(theta)) - B*abs(cos(theta)))
    return temp


def co_above(data, seuil):
    data.sort(reverse = True)
    for i in range(size(data)):
        if data[i] < seuil :
            result = i
            break
    return result


def sum_over(data) :
    result = []
    for i in range(len(data)) :
        result.append(sum(data[0:i+1]))
    return result


def plotdata(data, x, y):
    """
    This function plot a 2D curve given a json data and the column number of x and y axis.
    """
    plot(colarray(data, x, 0), colarray(data, y, 0))
    return True


def plot_int(data):
    """
    Given a array of data in the form [V, dI/dV], it comutes and plot the integral. This fonction can be used together with plot_profile
    to evaluate the gamma parameters of the sample.
    """
    result = []
    for i in range(len(data[0])+1):
        if i > 0 :
            result.append(integrate.simps(data[0][0:i], data[1][0:i]))
    f = figure()
    result.reverse()
    vd =  array(data[1])
    vd = vd.tolist()
    vd.reverse()
    plot(vd, result)
    x = ginput()
    for i in range(len(result)) :
        result[i] = result[i] -x[0][1]
    f.clear()
    plot(vd, result)
    return result
