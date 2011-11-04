class Stat_point() :
    """
    This object is used to store the result of get_jump method of sweep_set_open
    """
    def __init__(self, A = "None") :
        if(A == "None") :
            self.value = "None"
            self.field = "None"
            self.up = "None"
            self.trace = "None"
            self.sweep_nbr = "None"
        else :
            self.value = A[0]
            self.field = A[1]
            self.up = A[2]
            self.trace = A[3]
            self.sweep_nbr = A[4]

    def pass_array(self):
        return [self.value, self.field, self.up, self.trace, self.sweep_nbr ]
