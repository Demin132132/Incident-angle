import numpy as np
import fitter_3ch
import json
from pylab import *
from scipy.optimize import minimize



kw_cuts = np.array([13.125, 50.0, 200.0, 750.0])

def calc_cal_HR_fit(counts, counts_err, fcal):
 
	cuts_cur = kw_cuts * fcal
	cuts_nom = kw_cuts
 
	fitter = fitter_3ch.Fitter(fitter_3ch.model('CPL'), cuts_cur, counts, counts_err)
	result, chi2 = fitter.fit()

       
	fitted_counts = fitter.model.int_func(result, cuts_nom[0:3], cuts_nom[1:4])
	#print ("inp counts: "), counts
	#print ("out counts: "), fitted_counts
 
	return fitted_counts, result, chi2


TASK1 = open('tknom.txt', 'w')
table = open('table.txt')
cal = open('CAL.txt')

counter2 = 0
counter = 0
counter1 = 0


CAL1 = dict()
CAL2 = dict()


for line1 in cal:
	line1 = line1.strip()
	DETECTOR1, ID1, CAL_G1_S1, CAL_G2_S1, DETECTOR2, ID2, CAL_G1_S2, CAL_G2_S2 = [float(j) for j in line1.split(" ",8)]
		
	
	CAL1[ID1] = CAL_G1_S1
	CAL2[ID2] = CAL_G1_S2

	counter = counter + 1


global IND, fitted_countsS1, parS1, chi2S1, fitted_countsS2, parS2, chi2S2, cos_Tetta, Tetta, detec



for line in table:
	line = line.strip()
	DETECTOR, ID, S1G1, S1G2, S1G3, S1G1er, S1G2er, S1G3er, S2G1, S2G2, S2G3, S2G1er, S2G2er, S2G3er, SUM_S1, SUM_S2 = [float(l) for l in line.split(" ",16)]
	
	
	counts_cal1 = np.array([S1G1, S1G2, S1G3])
	counts_cal_err1 = np.array([S1G1er, S1G2er, S1G3er])

	counts_cal2 = np.array([S2G1, S2G2, S2G3])
	counts_cal_err2 = np.array([S2G1er, S2G2er, S2G3er])


	if ID in CAL1.keys():
		fitted_countsS1, parS1, chi2S1 = calc_cal_HR_fit(counts_cal1, counts_cal_err1, CAL1[ID])
		fitted_countsS2, parS2, chi2S2 = calc_cal_HR_fit(counts_cal2, counts_cal_err2, CAL1[ID])
		detec = 1

	if ID in CAL2.keys():
		fitted_countsS1, parS1, chi2S1 = calc_cal_HR_fit(counts_cal1, counts_cal_err1, CAL2[ID])
		fitted_countsS2, parS2, chi2S2 = calc_cal_HR_fit(counts_cal2, counts_cal_err2, CAL2[ID])
		detec = 2




	if ID == 4760:
		hhh = 2.050
		fitted_countsS1, parS1, chi2S1 = calc_cal_HR_fit(counts_cal1, counts_cal_err1, hhh)
		fitted_countsS2, parS2, chi2S2 = calc_cal_HR_fit(counts_cal2, counts_cal_err2, hhh)
		detec = 1

	if ID == 4761:
		hhh = 2.039
		fitted_countsS1, parS1, chi2S1 = calc_cal_HR_fit(counts_cal1, counts_cal_err1, hhh)
		fitted_countsS2, parS2, chi2S2 = calc_cal_HR_fit(counts_cal2, counts_cal_err2, hhh)
		detec = 1

	if ID == 4769:
		hhh = 2.043
		fitted_countsS1, parS1, chi2S1 = calc_cal_HR_fit(counts_cal1, counts_cal_err1, hhh)
		fitted_countsS2, parS2, chi2S2 = calc_cal_HR_fit(counts_cal2, counts_cal_err2, hhh)
		detec = 1

	if ID == 4771:
		hhh = 1.647
		fitted_countsS1, parS1, chi2S1 = calc_cal_HR_fit(counts_cal1, counts_cal_err1, hhh)
		fitted_countsS2, parS2, chi2S2 = calc_cal_HR_fit(counts_cal2, counts_cal_err2, hhh)
		detec = 2

	if ID == 4779:
		hhh = 2.033
		fitted_countsS1, parS1, chi2S1 = calc_cal_HR_fit(counts_cal1, counts_cal_err1, hhh)
		fitted_countsS2, parS2, chi2S2 = calc_cal_HR_fit(counts_cal2, counts_cal_err2, hhh)
		detec = 1


	if ID == 4782:
		hhh = 1.650
		fitted_countsS1, parS1, chi2S1 = calc_cal_HR_fit(counts_cal1, counts_cal_err1, hhh)
		fitted_countsS2, parS2, chi2S2 = calc_cal_HR_fit(counts_cal2, counts_cal_err2, hhh)
		detec = 2


	if ID == 4784:
		hhh = 1.656
		fitted_countsS1, parS1, chi2S1 = calc_cal_HR_fit(counts_cal1, counts_cal_err1, hhh)
		fitted_countsS2, parS2, chi2S2 = calc_cal_HR_fit(counts_cal2, counts_cal_err2, hhh)
		detec = 2


	if ID == 4787:
		hhh = 2.031
		fitted_countsS1, parS1, chi2S1 = calc_cal_HR_fit(counts_cal1, counts_cal_err1, hhh)
		fitted_countsS2, parS2, chi2S2 = calc_cal_HR_fit(counts_cal2, counts_cal_err2, hhh)
		detec = 1

	if ID == 4789:
		hhh = 2.038
		fitted_countsS1, parS1, chi2S1 = calc_cal_HR_fit(counts_cal1, counts_cal_err1, hhh)
		fitted_countsS2, parS2, chi2S2 = calc_cal_HR_fit(counts_cal2, counts_cal_err2, hhh)
		detec = 1


	if ID == 4791:
		hhh = 1.661
		fitted_countsS1, parS1, chi2S1 = calc_cal_HR_fit(counts_cal1, counts_cal_err1, hhh)
		fitted_countsS2, parS2, chi2S2 = calc_cal_HR_fit(counts_cal2, counts_cal_err2, hhh)
		detec = 2


	if ID == 4792:
		hhh = 2.040
		fitted_countsS1, parS1, chi2S1 = calc_cal_HR_fit(counts_cal1, counts_cal_err1, hhh)
		fitted_countsS2, parS2, chi2S2 = calc_cal_HR_fit(counts_cal2, counts_cal_err2, hhh)
		detec = 1

	if ID == 4797:
		hhh = 1.672
		fitted_countsS1, parS1, chi2S1 = calc_cal_HR_fit(counts_cal1, counts_cal_err1, hhh)
		fitted_countsS2, parS2, chi2S2 = calc_cal_HR_fit(counts_cal2, counts_cal_err2, hhh)
		detec = 2

	if ID == 4798:
		hhh = 1.669
		fitted_countsS1, parS1, chi2S1 = calc_cal_HR_fit(counts_cal1, counts_cal_err1, hhh)
		fitted_countsS2, parS2, chi2S2 = calc_cal_HR_fit(counts_cal2, counts_cal_err2, hhh)
		detec = 2

	if ID == 4801:
		hhh = 1.649
		fitted_countsS1, parS1, chi2S1 = calc_cal_HR_fit(counts_cal1, counts_cal_err1, hhh)
		fitted_countsS2, parS2, chi2S2 = calc_cal_HR_fit(counts_cal2, counts_cal_err2, hhh)
		detec = 2

	if ID == 4804:
		hhh = 1.664
		fitted_countsS1, parS1, chi2S1 = calc_cal_HR_fit(counts_cal1, counts_cal_err1, hhh)
		fitted_countsS2, parS2, chi2S2 = calc_cal_HR_fit(counts_cal2, counts_cal_err2, hhh)
		detec = 2


	if ID == 4807:
		hhh = 1.654
		fitted_countsS1, parS1, chi2S1 = calc_cal_HR_fit(counts_cal1, counts_cal_err1, hhh)
		fitted_countsS2, parS2, chi2S2 = calc_cal_HR_fit(counts_cal2, counts_cal_err2, hhh)
		detec = 2

	if ID == 4812:
		hhh = 2.074
		fitted_countsS1, parS1, chi2S1 = calc_cal_HR_fit(counts_cal1, counts_cal_err1, hhh)
		fitted_countsS2, parS2, chi2S2 = calc_cal_HR_fit(counts_cal2, counts_cal_err2, hhh)
		detec = 1


	if ID == 4813:
		hhh = 2.059
		fitted_countsS1, parS1, chi2S1 = calc_cal_HR_fit(counts_cal1, counts_cal_err1, hhh)
		fitted_countsS2, parS2, chi2S2 = calc_cal_HR_fit(counts_cal2, counts_cal_err2, hhh)
		detec = 1

	if ID == 4819:
		hhh = 2.097
		fitted_countsS1, parS1, chi2S1 = calc_cal_HR_fit(counts_cal1, counts_cal_err1, hhh)
		fitted_countsS2, parS2, chi2S2 = calc_cal_HR_fit(counts_cal2, counts_cal_err2, hhh)
		detec = 1

	if ID == 4820:
		hhh = 2.060
		fitted_countsS1, parS1, chi2S1 = calc_cal_HR_fit(counts_cal1, counts_cal_err1, hhh)
		fitted_countsS2, parS2, chi2S2 = calc_cal_HR_fit(counts_cal2, counts_cal_err2, hhh)
		detec = 1


	sum1 = fitted_countsS1[0] + fitted_countsS1[1] + fitted_countsS1[2]
	sum2 = fitted_countsS2[0] + fitted_countsS2[1] + fitted_countsS2[2]

	d1 = sum1 - SUM_S1
	d2 = sum2 - SUM_S2

	
	awwww = "{:3.0f} {:15.0f} {:15.3f} {:15.3f} {:15.3f}  {:15.3f} {:15.3f} {:15.3f} {:15.3f} {:15.3f} {:15.3f} {:15.3f} {:15.3f} {:15.3f} {:15.3f}\n".format( 
	counter1, ID, fitted_countsS1[0], fitted_countsS1[1], fitted_countsS1[2], fitted_countsS2[0], fitted_countsS2[1], fitted_countsS2[2], SUM_S1, SUM_S2, sum1, sum2, d1, d2,  detec)
	"""
	awwww = "{:3.0f} {:15.0f} {:15.4f} {:15.3f} {:15.3f} {:15.3f} {:15.3f} {:15.3f} {:15.3f} \n".format( 
	 SUM_S1, SUM_S2, sum1, sum2, d1, d2, d1/sum1, d2/sum2, detec)
		
	"""	



	TASK1.write(str(awwww))



TASK1.close()
cal.close()
table.close()


	