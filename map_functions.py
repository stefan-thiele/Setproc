def get_coupling():
    """
    This function gives the coupling of the sample to the gate source and drain as weel as the alpha factor given by Cg/Ct .
    One has to give four point, starting with the slope defined by Cg/Cs and then the one defined by Cg / (Cd +Cg). It retunrs the result
    as Cs Cd and alpha.
    """
    temp = ginput(4)
    Cs = np.abs( (temp[0][0] - temp[1][0]) / (temp[0][1] - temp[1][1])) * 1e3
    tp = np.abs( ( temp[2][1] - temp[3][1] )/(temp[2][0] - temp[3][0])) * 1e-3
    Cd = (1 - tp)/ tp
    alp = 1 / (Cs + 1 +Cd)
    return [Cs,Cd,alp]


def get_slope():
    """
    Given two points, give the slope a line
    """
    temp = ginput(2)
    return (temp[0][1] - temp[1][1])/(temp[0][0] - temp[1][0])


def plot_profile_h(im):
    """
    Given a point on the Coulomb Map, this function plot the corresponding profile and returns a array of two columns [V,dI/dV]
    """
    y = ginput()[0][1]
    xm,  Xm = im.get_extent()[0:2]
    ym,  Ym = im.get_extent()[2:4]
    sweep_n = size(im.get_array()) / size(im.get_array()[0])
    nbr =  (1. * sweep_n / abs(Ym - ym)) * (y-ym)
    figure()
    data = im.get_array()
    plot(linspace(xm, Xm, size(im.get_array()[0])) ,  data[nbr])
    return [linspace(xm, Xm, size(im.get_array()[0]))  , data[nbr]]


def plot_profile(im):
    """
    Given a point on the Coulomb Map, this function plot the corresponding profile and returns a array of two columns [V,dI/dV]
    """
    x = ginput()[0][0]
    xm,  Xm = im.get_extent()[0:2]
    ym,  Ym = im.get_extent()[2:4]
    sweep_n = size(im.get_array()[0])
    nbr =  (1. * sweep_n / abs(Xm - xm)) * (x-xm)
    Vg = xm + nbr * (Xm-xm)/sweep_n
    figure()
    data = im.get_array()
    plot( linspace(ym, Ym, size(colarray(data,floor(nbr),0))) ,  colarray(data,floor(nbr),0))
    return [linspace(ym, Ym, size(colarray(data,floor(nbr),0))) ,  colarray(data,floor(nbr),0),Vg]


