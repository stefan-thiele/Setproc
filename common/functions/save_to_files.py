import os
from numpy import savetxt, matrix

def save_obj_txt(filename, obj) :
    stream = open(filename,"w")
    stream.write(str(obj))
    stream.close()
    return True

def cyc_save_fig(filename, fig, cyc, file_format = "png"):
    os.mkdir(filename)
    figfile = filename+"/"+filename + "." + file_format
    fig.savefig(figfile)
    txtfile = filename+"/"+filename+".txt"
    save_obj_txt(txtfile, cyc["calibration"])
    txtfile = filename+"/"+filename+"_metadata.txt"
    save_obj_txt(txtfile, cyc["metadata"])
    return True


def export_data(filename, data):
    savetxt(filename, matrix(data).transpose(), delimiter = " , ")
    return True
