#############
###This file gather all the function used specifically by the map class
####



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


def check_merge_map(map1,map2):
    meta1 = map1["metadata"]
    meta2 = map2["metadata"]
    x1 = meta1.keys()
    x2 = meta2.keys()
    if size(x1) != size(x2) :
        print( "the two objects have not the same metadata")
    print("here are the differences")
    compare_dict(meta1,meta2)

def compare_dict(dic1,dic2,string = ""):
    str = string
    if isinstance(dic1,dict):
        for x in dic1.keys() :
            str_tp = str+"-->"+x
            compare_dict(dic1[x],dic2[x],str_tp)
    else:
        if dic1 != dic2 :
            print(" ------------>!!!!!!DIFF !!!!!!! ---------------->")
            print(str)
            print(dic1)
            print("different from")
            print(dic2)
            return False
        else:
            return True

    return True

def map_merge(map1,map2):
    extent1 = map1["extent"]
    X1min = extent1[0]
    X1max = extent1[1]
    extent2 = map2["extent"]
    X2min = extent2[0]
    X2max = extent2[1]
    point_nbr1 = size(map1["data"])/size(map1["data"][0])
    point_nbr2 = size(map2["data"])/size(map2["data"][0])


    if extent1[2] != extent2[2] or extent1[3] !=  extent2[3] :
        print("not the same bias.. cannot merge")
        return 0
    elif point_nbr1 != point_nbr2 :
        print("not the same point number.... aborted")
    else :
        if X1min > X2min :
            map1["extent"] = [X2min,X1max,extent1[2],extent1[3]]

            map1["data"] = matrix(map2["data"]).transpose().tolist()+matrix(map1["data"]).transpose().tolist()
            map1["data"] = matrix(map1["data"]).transpose().tolist()
        if X2min > X1min :
            map1["extent"] = [X1min,X2max,extent1[2],extent1[3]]
            map1["data"] = matrix(map1["data"]).transpose().tolist()+matrix(map2["data"]).transpose().tolist()
            map1["data"] = matrix(map1["data"]).transpose().tolist()

    return True


