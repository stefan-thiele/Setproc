from numpy import size


def extract_stat(sweep, seuil1, seuil2, span) :
    #hold final min value
    in_min = 0
    in_min_arg = -1
    in_min_write = True
    #hold the temp min value
    temp_min = 0
    temp_min_arg = -1
    # hold the final max value
    in_max = 0
    in_max_arg = -1
    in_max_write = True
    #hold the temp max value
    temp_max = 0
    temp_max_arg = -1

    sweep_size = size(sweep)
    for i in range(sweep_size) :
        value = sweep[i]
        #check if we are below the threshold, if yes, next point
        if abs(value) < seuil1 :
            if in_max_write == False :
                in_max_write = True
                if temp_max < in_max :
                    temp_max = in_max
                    temp_max_arg = in_max_arg
            if in_min_write == False :
                in_min_write = True
                if temp_min > in_min :
                    temp_min = in_min
                    temp_min_arg = in_min_arg
            continue
        #if we are in beetween the two threshold
        if abs(value) > seuil1 and abs(value) < seuil2 :
            if value < in_min and in_min_write :
                in_min = value
                in_min_arg = i
            if value > in_max and in_max_write :
                in_max = value
                in_max_arg = i
        #if we are above the threshold
        if abs(value) > seuil2 :
            #Make sure than min and max cannot be accessed before going back below seuil1
            if value < - seuil2 :
                in_min_write = False
                if(in_min_arg + span > i) :
                    in_min = 0
                    in_min_arg = -1
            if value > seuil2 :
                in_max_write = False
                if(in_max_arg + span > i) :
                    in_max = 0
                    in_max_arg = -1

    if in_min > temp_min :
        in_min = temp_min
        in_min_arg = temp_min_arg

    if in_max < temp_max :
        in_max = temp_min
        in_max_arg = temp_max_arg

    return in_min, in_min_arg, in_max, in_max_arg

















