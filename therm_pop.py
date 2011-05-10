def Temp_Pop(T,E) :
	E2 = E[1] - E[0]
	E3 = E[2] - E[0]
	E4 = E[3] - E[0]
	P2 = 0.25 * exp(-E2/T)
	P3 = 0.25 * exp(-E3/T)
	P4 = 0.25 * exp(-E4/T)
	P1 = 1 - P4 - P2 -P3
	return [P1,P2,P3,P4]
