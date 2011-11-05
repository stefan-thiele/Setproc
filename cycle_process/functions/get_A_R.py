from numpy import size

def get_A_R(Cyc) :
    """
    This function parse the data and store all the sweep for which there was a jump both for the trace and retrace. They are store in ["AvsR"], the first element ["AvsR"][0] being the trace and the second the retrace.
    """
    seuil1 = Cyc["calibration"]["plot"]["seuil1"]
    seuil2 = Cyc["calibration"]["plot"]["seuil2"]
    Cyc["AvsR"] = [[], []]
    size_detect = size(Cyc["detection"])
    itera = size_detect/4
    for i in range(itera-4) :
        traceok = False
        retraceok = False
        trace1 = Cyc["detection"][4*i+4] #The +4 is due to the fact that the waiting time is done during trace
        trace2 = Cyc["detection"][4*i+1+4]
        retrace1 = Cyc["detection"][4*i+2]
        retrace2 = Cyc["detection"][4*i+3]
        #FOR TRACE
        if trace1.in_between(seuil1, seuil2) and trace2.in_between(seuil1, seuil2) : #check if the two values are in the range
            #if yes, take the higher value
            trace_push = min(trace1.field, trace2.field) #I want the position of the FIRST jump
            traceok = True

        elif trace1.in_between(seuil1, seuil2) :
            trace_push = trace1.field
            traceok = True

        elif trace2.in_between(seuil1, seuil2) :
            trace_push = trace2.field
            traceok = True

        if(traceok): #only do the check if a trace is valid
            if retrace1.in_between(seuil1, seuil2) and retrace2.in_between(seuil1, seuil2) : #check if the two values are in the range
                #if yes, take the higher value
                retrace_push = min(retrace1.field, retrace2.field) #I want the position of the LAST jump
                retraceok = True
            elif retrace1.in_between(seuil1, seuil2) :
                retrace_push = retrace1.field
                retraceok = True
            elif retrace2.in_between(seuil1, seuil2) :
                retrace_push = retrace2.field
                retraceok = True


        if(traceok and retraceok):
            Cyc["AvsR"][0].append(trace_push)
            Cyc["AvsR"][1].append(retrace_push)
