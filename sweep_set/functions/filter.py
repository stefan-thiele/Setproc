from setproc.common.cfunctions import moving_average as mva
from numpy import square, diff

def filter(sweep, width, power, width2):
    """
    This function apply the filter described below. The return array size is ( size(sweep)- 2 * (width +1) - swidth +1 .
    This function detects the pic. The width in argument is the one of the gate function
    """
    moving_average = mva.moving_average_c

    step1 = moving_average(sweep, width)
    step3 = moving_average(step1, width)
    step1 = square(step1)
    step2 = moving_average(step1, width)
    step3 = square(step3)
    D = diff(moving_average(sweep, 2*width-2))
    result = D * (step2 - step3)
    result = result ** power

    return moving_average(result, width2)
