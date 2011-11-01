def filter(sweep,width,power,width2):
    """
        This function apply the filter described below. The return array size is ( size(sweep)- 2 * (width +1) - swidth +1 .
        This function detects the pic. The working principle is the following :
                                                            _
                        _            |---- (step1)^2 -- _| |_ ---(step2)--|
    --(sweep)->  _| |_ -(step1)-|       _                           (-) ----> result
                                    |-----_| |_ --(step3)-- (step3)^2 ---|
        First Part          |              Second Part           |
    The width in argument is the one of the gate function
    """
    moving_average = mva.moving_average_c
    size_sweep = np.size(sweep)

    step1 = moving_average(sweep,width)
    step3 = moving_average(step1,width)
    step1 = np.square(step1)
    step2 = moving_average(step1,width)
    step3 = np.square(step3)
    D = np.diff(moving_average(sweep,2*width-2))
    result = D * (step2 - step3)
    result = result ** power

    return moving_average(result,width2)
