import time #to handle the time checking,
from setproc.common.classes.to_save_object import ToSaveObject
from setproc.common.classes.open_bin import OpenBin #to be able to open json and bin files
from setproc.sweep_set.functions.merge_gb import merge_GB
from setproc.sweep_set.classes.sweep_set import sweep_set_open #to open and manage sweep_set_open objects
from setproc.sweep_set.classes.stat_point import Stat_point
from numpy import size, histogram2d, log10, array, histogram
from matplotlib.pyplot import figure, title, hist, ginput, plot, xlabel, ylabel, xlim, ylim

class cycle_process(ToSaveObject) :
    """
    cycle_process can be used to post-process several traces and retraces files. It will merge the traces and retraces between themselves using the merge function. You can save the extracted data so you do not have anymore to open all the sweeps and therefore you gain time and memory.
    The syntax depends if you have weither or not already extracted data. If it is the case, the syntax is cycle_process("filename"). Otherwise it is cycle_process("trace_filename","retrace_filemane",list of the increment values,and mode (usually "Json")). A sanity_check is performed on each sweep as weel as on the merged ones.
    """

    def __init__(self, trace, retrace = None , interval = None, mode = "Json"):
        ToSaveObject.__init__(self)
        self.filenames_trace = []
        self.filenames_retrace = []

        if(interval == None and retrace ==None) :
            temp = OpenBin(trace)
            for x in temp :
                self[x] = temp[x]
            del(temp)
            self.post_loading()

        else :
            #TRACE
            GB_array1 = []
            #Construct a filename array for loading files
            for i in interval :
                self.filenames_trace.append(str(i)+trace)

            #Load the files of the filename array
            for x in self.filenames_trace :
                print "Loading ", x, " file. Please wait.."
                GB_array1.append(sweep_set_open(x, mode))
                GB_array1[-1].sanity_check()
            print "Merging...."
            #merge all the GB object in a single one and delete the GB array
            self.trace = merge_GB(GB_array1)
            del(GB_array1)

            #RETRACE
            GB_array2 = []
            for i in interval :
                self.filenames_retrace.append(str(i)+retrace)

            for x in self.filenames_retrace :
                print "Loading ", x, " file. Please wait.."
                GB_array2.append(sweep_set_open(x, mode))
                GB_array2[-1].sanity_check()
            print "Merging...."
            self.retrace = merge_GB(GB_array2)
            del(GB_array2)

            #Final checking!!
            print "Finale sanity check once merged"
            print "trace...."
            self.trace.sanity_check()
            print "retrace..."
            self.retrace.sanity_check()
            self["metadata"] = self.trace["metadata"]
            del(self.filenames_trace)
            del(self.filenames_retrace)

    def get_stat(self, i_start, w, power=1, sw=1, mode = "classic", seuil1 = 0, seuil2 = 0, span = 50) :
        """
        get_stat allows to detect the jumps going through all the sweeps. It uses directly the function get_jump_2 of the sweep_set_open object. This data are stored independtly from the trace and retrace file. The syntax is the following get_stat(seuil,i_start,w) where seuil is the threshold of detection, i_start is the number of points to skip from zero, and w is the filter widht (see the filter doc for more information).
        """
        self.reset_calibration()
        if mode == "classic" :
            self["calibration"]["stat"]["mode"] = mode
            self["calibration"]["stat"]["w"] = w
            self["calibration"]["stat"]["sw"] = sw
            self["calibration"]["stat"]["power"] = power
            self["calibration"]["stat"]["i_start"] = i_start

        else:
            self["calibration"]["stat"]["mode"] =  mode
            self["calibration"]["stat"]["seuil1"] = seuil1
            self["calibration"]["stat"]["seuil2"] = seuil2
            self["calibration"]["stat"]["w"] = w
            self["calibration"]["stat"]["sw"] = sw
            self["calibration"]["stat"]["power"] = power
            self["calibration"]["stat"]["i_start"] = i_start
            self["calibration"]["stat"]["span"] = span


        self["detection"] = []
        sweep_number = max(self.trace["sweep_number"], self.retrace["sweep_number"])
        si = size(self.trace["bias"])

        for i in range(sweep_number) :
            if(i%1000 ==0 and i > 0):
                print(str(int(100 * i/sweep_number)) + "%")
            #TRACE STAT
            Down, Up = self.trace.get_jump(i, i_start, w, power, sw, si, mode, seuil1, seuil2, span)
            Down.trace = True
            Up.trace = True

            #check what was detected first
            if( Down.field < Up.field) :
                self["detection"].append(Down)
                self["detection"].append(Up)
            else :
                self["detection"].append(Up)
                self["detection"].append(Down)

            #RETRACE STAT
            Down, Up = self.retrace.get_jump(i, i_start, w, power, sw, si, mode, seuil1, seuil2, span)
            Down.trace = False
            Up.trace = False
            #check what was detected first
            if( Down.field > Up.field) :
                self["detection"].append(Down)
                self["detection"].append(Up)
            else :
                self["detection"].append(Up)
                self["detection"].append(Down)

        return True


    def get_hist(self, points,rge = "None", shift_trace=1):
        seuil1 = self["calibration"]["plot"]["seuil1"]
        seuil2 = self["calibration"]["plot"]["seuil2"]
        shift_B = self["calibration"]["plot"]["offset"]
        trace_range = self["calibration"]["plot"]["range"]
        if rge == "None" :
            rge = [trace_range, trace_range]
        temp = []
        siup = size(self["detection"])
        for i in range(siup) :
            topush = self["detection"][i]
            if(abs(topush.value) > seuil1 and abs(topush.value) < seuil2) :
                if (topush.trace == False) :
                    temp.append(topush.field -shift_B)
                else :
                    temp.append(topush.field)
        siup = size(temp)
        return histogram2d(temp[:siup-shift_trace], temp[shift_trace:siup], points, rge)



    def get_A_R(self) :
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


    def sort_data(self) :
        """
        This function sort the jumps first according to trace and retrace and then according to the kind of transition, either up or done. For more information on the label up and down, please refer to the documentation of get_jump2.
        """
        seuil1 = self["calibration"]["plot"]["seuil1"]
        seuil2 = self["calibration"]["plot"]["seuil2"]

        self["sort"] = dict()
        self["sort"]["trace"] = dict()
        self["sort"]["trace"]["up"] = []
        self["sort"]["trace"]["down"] = []
        self["sort"]["retrace"] = dict()
        self["sort"]["retrace"]["up"] = []
        self["sort"]["retrace"]["down"] = []
        for i in range(size(self["detection"])) :
            topush = self["detection"][i]
            if topush.trace == True and abs(topush.value) > seuil1 and abs(topush.value) < seuil2 :
                if topush.up == False :
                    self["sort"]["trace"]["down"].append(topush.field)
                else :
                    self["sort"]["trace"]["up"].append(topush.field)

            if topush.trace == False and abs(topush.value) > seuil1 and abs(topush.value) < seuil2 :
                if topush.up == False :
                    self["sort"]["retrace"]["down"].append(topush.field)
                else :
                    self["sort"]["retrace"]["up"].append(topush.field)

        return True

    def get_double(self, seuil1, seuil2, offset):
        seuil1 = self["calibration"]["plot"]["seuil1"]
        seuil2 = self["calibration"]["plot"]["seuil2"]
        offset = self["calibration"]["plot"]["offset"]

        self["double"] = dict()
        self["double"]["trace"] = [[], []]
        self["double"]["retrace"] = [[], []]
        tot_size = size(self["detection"])
        itera = int(tot_size/4)

        for i in range(itera) :
            trace1 = self["detection"][4*i]
            trace2 = self["detection"][4*i+1]
            retrace1 = self["detection"][4*i+2]
            retrace2 = self["detection"][4*i+3]
            if(abs(trace1.value) > seuil1 and abs(trace2.value) > seuil1) :
                if(abs(trace1.value) < seuil2 and abs(trace2.value) < seuil2) :
                    self["double"]["trace"][0].append(trace1.field)
                    self["double"]["trace"][1].append(trace2.field)
            if(abs(retrace1.value) > seuil1 and abs(retrace2.value) > seuil1 ):
                if(abs(retrace1.value) < seuil2 and abs(retrace2.value) < seuil2 ):
                    self["double"]["retrace"][0].append(retrace1.field)
                    self["double"]["retrace"][1].append(retrace2.field)


    def get_value_stat(self) :
        self["value_stat"] = [[], []]
        for i in range(size(self["detection"])) :
            topush = abs(self["detection"][i].value)
            towhere = self["detection"][i].trace
            if(towhere) :
                if topush > 0 :
                    self["value_stat"][0].append(topush)
            else :
                if topush > 0 :
                    self["value_stat"][1].append(topush)
        figure()
        title("Trace")
        hist(log10(array(self["value_stat"][0])), 200)
        figure()
        title("Retrace")
        hist(log10(array(self["value_stat"][1])), 200)
        return True

    def get_span_sweep_nbr(self, seuil1, seuil2):

        seuil1 = self["calibration"]["plot"]["seuil1"]
        seuil2 = self["calibration"]["plot"]["seuil2"]


        self["span_swep_nbr"] = [[], []]
        tot_size = size(self["detection"])
        itera = int(tot_size/4)
        for i in range(itera) :
            trace1 = self["detection"][4*i]
            trace2 = self["detection"][4*i+1]
            retrace1 = self["detection"][4*i+2]
            retrace2 = self["detection"][4*i+3]
            addtrace = True
            addretrace = True
            if(abs(trace1.value) > seuil1 and abs(trace1.value) < seuil2) :
                self["span_swep_nbr"][0].append(trace1.sweep_nbr)
                addtrace = False
            if(abs(trace2.value) > seuil1 and abs(trace2.value) < seuil2 and addtrace) :
                self["span_swep_nbr"][0].append(trace2.sweep_nbr)
            if(abs(retrace1.value) > seuil1 and abs(retrace1.value) < seuil2 ):
                self["span_swep_nbr"][1].append(retrace1.sweep_nbr)
                addretrace = False
            if(abs(retrace2.value) > seuil1 and abs(retrace2.value) < seuil2 and addretrace ):
                self["span_swep_nbr"][1].append(retrace2.sweep_nbr)

    def get_hysteresis(self) :
        """
        This function take for each trace and retrace the value of the magnetic field corresponding at the strongest transistion. This statistic is used afterwards to plot the hysteresis cycle.
        """
        self["hysteresis"] = [[], []]
        tot_size = size(self["detection"])
        itera = int(tot_size/4)
        seuil = self["calibration"]["plot"]["seuil1"]
        for i in range(itera):
            trace1 = self["detection"][4*i]
            trace2 = self["detection"][4*i+1]
            retrace1 = self["detection"][4*i+2]
            retrace2 = self["detection"][4*i+3]
            if abs(trace1.value) > abs(trace2.value) and abs(trace1.value) > seuil :
                self["hysteresis"][0].append(trace1.field)
            elif abs(trace2.value) > seuil :
                self["hysteresis"][0].append(trace2.field)

            if abs(retrace1.value) > abs(retrace2.value) and abs(retrace1.value) > seuil :
                self["hysteresis"][1].append(retrace1.field)
            elif abs(retrace2.value) > seuil :
                self["hysteresis"][1].append(retrace2.field)

    def plot_hysteresis(self, xmin, xmax, bins = 200, width = 3, color = ["red","blue"]):
        self.get_hysteresis()
        ht = histogram(self['hysteresis'][0], bins, [xmin, xmax])
        hr = histogram(self['hysteresis'][1], bins, [xmin, xmax])
        vt = ht[1]
        vr = hr[1]
        sum_ht = sum(ht[0])
        sum_hr = sum(hr[0])
        norm_val = max(sum_ht, sum_hr)
        ht = 1.*ht[0]/norm_val
        hr = 1.*hr[0]/norm_val
        size_h = size(ht)
        for i in range(size(ht)) :
            if i > 0 :
                ht[i] = ht[i] + ht[i-1]
                hr[i] = hr[i] + hr[i-1]
        figure()
        plot(vt[:size_h], ht * 2 - 1, linewidth = width, color = color[0])
        plot(vr[:size_h], hr * 2 - 1 + 2.* (norm_val - sum_hr) / norm_val, linewidth = width, color = color[1])
        xlim(xmin, xmax)
        ylim(-1.05, 1.05)
        xlabel("B (T)")
        ylabel(r"$M/M_s$")
        return [vt[:size_h], ht * 2 - 1, vr[:size_h], hr * 2 - 1 + 2.* (norm_val - sum_hr) / norm_val]


    def get_time_stat(self, mode = "retrace-trace") :
        sweep_nbr = size(self["dates"][0])
        if mode == "trace-retrace" :
            result = []
            for i in range(sweep_nbr):
                DT = self["dates"][0][i]
                DR = self["dates"][1][i]
                Tt = time.strptime(DT,"%Y-%m-%dT%H:%M:%S")
                Tr = time.strptime(DR,"%Y-%m-%dT%H:%M:%S")
                tt = time.mktime(Tt)
                tr = time.mktime(Tr)
                result.append(tr-tt)

        elif mode == "retrace-trace" :
            result = []
            for i in range(sweep_nbr-1):
                DT = self["dates"][0][i+1]
                DR = self["dates"][1][i]
                Tt = time.strptime(DT,"%Y-%m-%dT%H:%M:%S")
                Tr = time.strptime(DR,"%Y-%m-%dT%H:%M:%S")
                tt = time.mktime(Tt)
                tr = time.mktime(Tr)
                result.append(tr-tt)

        elif mode == "trace-trace" :
            result = []
            for i in range(sweep_nbr-1):
                DT = self["dates"][0][i+1]
                DR = self["dates"][0][i]
                Tt = time.strptime(DT,"%Y-%m-%dT%H:%M:%S")
                Tr = time.strptime(DR,"%Y-%m-%dT%H:%M:%S")
                tt = time.mktime(Tt)
                tr = time.mktime(Tr)
                result.append(tr-tt)

        elif mode == "retrace-retrace" :
            result = []
            for i in range(sweep_nbr-1):
                DT = self["dates"][1][i+1]
                DR = self["dates"][1][i]
                Tt = time.strptime(DT,"%Y-%m-%dT%H:%M:%S")
                Tr = time.strptime(DR,"%Y-%m-%dT%H:%M:%S")
                tt = time.mktime(Tt)
                tr = time.mktime(Tr)
                result.append(tr-tt)

        return hist(result, 25)


    def get_peaks(self,bins=200):
	"""
	The position and width of the 4 peaks can be selected by mouse click.
	The information is stored in ["calibration"]["plots"]
	The method get_A_R() has to be executed before	
	"""
	figure()
	bound = self["calibration"]["plot"]["range"]
	ht = hist(self["AvsR"][0],bins,bound)
	hr = hist(self["AvsR"][1],bins,bound)
	print("Chose the 4 maxima by left click")	
	#get the position of the 4 peaks	
	max_hist = ginput(4)
	x_pts = map(lambda x: x[0],max_hist)
	y_pts = map(lambda x: x[1],max_hist)
	plot(x_pts,y_pts,"ro")
	print("Select peak width with 2 clicks")
	#get the width of the peak	
	pw_hist = ginput(2)
	pw_x = map(lambda x: x[0],pw_hist)
	pw_y = map(lambda x: x[1],pw_hist)
	pw = abs(pw_x[1]-pw_x[0])	
	plot(pw_x,pw_y,"-o")
	#store information in ["calibration"]["plots"]	
	self["calibration"]["plot"]["peaks"] = []
	for k in range(4):
		self["calibration"]["plot"]["peaks"].append(x_pts[k])

	self["calibration"]["plot"]["peak_width"] = pw

	
    def	get_corr(self,peaknbr=0):
	"""
	The correlation between peaks occuring in 2 subsequent sweeps is plotted.
	The method get_peaks() has to be executed before
	Syntax: get_corr(int1)
	int1 is an integer number between 0 and 3 and corresponds to the peak to which the correlation is calculated.
	"""
	figure()	
	corr = [] # correlation
	x_pts = self["calibration"]["plot"]["peaks"]
	pw = self["calibration"]["plot"]["peak_width"]
	corr_dscr = [0,0,0,0] # discrete correlation
	size_AR = size(self["AvsR"][0])
	for i in range(size_AR):
		if ((self["AvsR"][0][i] > (x_pts[peaknbr]-pw)) and  (self["AvsR"][0][i] < (x_pts[peaknbr]+pw)) ):
			corr.append(self["AvsR"][1][i])
			for j in range(4):
				if ((self["AvsR"][1][i] > (x_pts[j]-pw)) and  (self["AvsR"][1][i] < (x_pts[j]+pw)) ):
					corr_dscr[j] = corr_dscr[j]+1	

	hist(corr,200)
	figure()	
	bar(x_pts,corr_dscr,pw,align="center")
				

	
    def set_plot_calibration(self, args = "None"):
        if args == "None":
            print("to be done")
        else :
            self["calibration"]["plot"]["seuil1"] = args[0]
            self["calibration"]["plot"]["seuil2"] = args[1]
            self["calibration"]["plot"]["range"] = args[2]
            self["calibration"]["plot"]["offset"] = args[3]

    def reset_calibration(self):
        self["calibration"] = dict()
        #parameters used for stat
        self["calibration"]["stat"] = dict()
        self["calibration"]["stat"]["seuil1"] = "None"
        self["calibration"]["stat"]["seuil2"] = "None"
        self["calibration"]["stat"]["w"] = "None"
        self["calibration"]["stat"]["sw"] = "None"
        self["calibration"]["stat"]["power"] = "None"
        self["calibration"]["stat"]["i_start"] = "None"
        #parameter used for plotting
        self["calibration"]["plot"] = dict()
        self["calibration"]["plot"]["seuil1"] = "None"
        self["calibration"]["plot"]["seuil1"] = "None"
        self["calibration"]["plot"]["range"] = "None"
        self["calibration"]["plot"]["offset"] = "None"

    def calibrate_offset(self, kind1 = "up", kind2 = "down"):
        print("Select the trace then the retrace")
        rge = self["calibration"]["plot"]["range"]
        figure()
        hist(self["sort"]["trace"][kind1], 100, rge)
        hist(self["sort"]["retrace"][kind2], 100, rge)
        temp = ginput(2)
        self["calibration"]["plot"]["offset"] = temp[1][0] - temp[0][0]

    ###This part contains the functions allowing some interaction with the object through menu
    ###

    def menu(self) :
        print("Make your choice")
        print("1 ----> Extract statistique")

        #if choice == 1 :
        #    self.menu_stat(self)

        return True


    def menu_stat(self):
        print("Let's proceed to the statistic extraction")
        print("Choose the mode : ")
        print("  1 ----> Classic")
        print("  2 ----> Double threshold")
        return True




    ########################################################
    ###This part is dedicated to saving and loading the data
    ###

    def save_all(self, tracefile, retracefile, whole_experiment) :
        """
        This function allows to save the data in binary format. This make them faster to load. The syntax is as follow : save_all(filename_for_trace,filename_for_retrace,filename_for_data_extracted)
        """
        self.trace.savez(tracefile)
        self.retrace.savez(retracefile)
        self["filenames"] = [tracefile+".npz", retracefile+".npz"]
        self.ready_to_save()
        self.save(whole_experiment)
        self.post_loading()


    def load_sweeps(self, mode="npz") :
        """
        to be documented latter
        """
        self.trace = sweep_set_open(self["filenames"][0], mode)
        self.retrace = sweep_set_open(self["filenames"][1], mode)
        print ("Sanity checks")
        print ("* Trace")
        self.trace.sanity_check()
        print ("* Retrace")
        self.retrace.sanity_check()

    def load_dates(self):
        self["dates"] = [[], []]
        sweep_number = max(self.trace["sweep_number"], self.retrace["sweep_number"])
        for i in range(sweep_number) :
            self["dates"][0].append(self.trace["date"][i])
            self["dates"][1].append(self.retrace["date"][i])


    def ready_to_save(self) :
        i = 0
        for x in self["detection"]  :
            self["detection"][i ] = x.pass_array()
            i = i+1

    def post_loading(self) :
        for i in range(len(self["detection"])) :
            self["detection"][i] = Stat_point(self["detection"][i])

    def reset(self) :
        todelete = self.keys()
        for x in todelete :
            if x == "metadata" or x == "filenames" :
                continue
            else :
                self.pop(x)

