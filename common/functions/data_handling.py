from numpy import sign, sin, cos, size

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
