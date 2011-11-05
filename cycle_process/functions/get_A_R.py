


def get_A_R(Cyc) :
"""
This function parse the data and store all the sweep for which there was a jump both for the trace and retrace. They are store in ["AvsR"], the first element ["AvsR"][0] being the trace and the second the retrace.
"""
seuil1 = self["calibration"]["plot"]["seuil1"]
seuil2 = self["calibration"]["plot"]["seuil2"]
self["AvsR"] = [[], []]
size_detect = size(self["detection"])
itera = size_detect/4
for i in range(itera-4) :
	traceok = False
	retraceok = False
	trace1 = self["detection"][4*i+4] #The +4 is due to the fact that the waiting time is done during trace
	trace2 = self["detection"][4*i+1+4]
	retrace1 = self["detection"][4*i+2]
	retrace2 = self["detection"][4*i+3]
	#check first which trace has to be taken
	if(abs(trace1.value) > seuil1 and abs(trace2.value) > seuil1) :
	if(abs(trace1.value) < seuil2 and abs(trace2.value) < seuil2) :
		if abs(trace1.value) > abs(trace2.value) :
		trace_push = trace1.field
		traceok = True
		else :
		trace_push = trace2.field
		traceok = True
	elif abs(trace1.value) < seuil2 :
		trace_push = trace1.field
		traceok = True
	elif abs(trace2.value) < seuil2 :
		trace_push = trace2.field
		traceok = True
	elif abs(trace1.value) > seuil1 and abs(trace1.value) < seuil2 :
	trace_push = trace1.field
	traceok = True
	elif abs(trace2.value) > seuil1 and abs(trace2.value) < seuil2 :
	trace_push = trace2.field
	traceok = True
	if(traceok) :
	if(abs(retrace1.value) > seuil1 and abs(retrace2.value) > seuil1) :
		if(abs(retrace1.value) < seuil2 and abs(retrace2.value) < seuil2) :
		if abs(retrace1.value) > abs(retrace2.value) :
			retrace_push = retrace1.field
			retraceok = True
		else :
			retrace_push = retrace2.field
			retraceok = True
		elif abs(retrace1.value) < seuil2 :
		retrace_push = retrace1.field
		retraceok = True
		elif abs(retrace2.value) < seuil2 :
		retrace_push = retrace2.field
		retraceok = True
	elif abs(retrace1.value) > seuil1 and abs(retrace1.value) < seuil2 :
		retrace_push = retrace1.field
		retraceok = True
	elif abs(retrace2.value) > seuil1 and abs(retrace2.value) < seuil2 :
		retrace_push = retrace2.field
		retraceok = True

	if(traceok and retraceok):
	self["AvsR"][0].append(trace_push)
	self["AvsR"][1].append(retrace_push)
