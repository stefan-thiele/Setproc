from numpy import size
from copy import deepcopy

def merge_GB(GB_array) :
    GB_temp = deepcopy(GB_array[0])
    GB_nbr = size(GB_array)
    GB_order = range(1, GB_nbr, 1)
    if( GB_nbr >1 ) :
        for i in GB_order :
            whole_size = size(GB_array[i]["data"])
            sweep_size = size(GB_array[i]["data"][1])
            current_array_size = whole_size/sweep_size
            for j in range(current_array_size) :
                GB_temp["data"].append(GB_array[i]["data"][j])
                GB_temp["date"].append(GB_array[i]["date"][j])
    GB_temp["sweep_number"] = len(GB_temp["data"])
    return GB_temp
