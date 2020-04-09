from sympy.solvers import solve
from sympy import Symbol
import pandas as pd
import math
import numpy as np
import fitter_3ch



def read_par(canal, det):

	par_ = open('P_' + det + '.txt')
	
	for line in par_: 
		line = line.strip()
		line = line.split()
		if canal in line[0]:
			a = float(line[5])
			b = float(line[6])
			c = float(line[7])
			d = float(line[8])
			delta = float(line[3])
			chi2 = line[1]
			dof = line[4]
			par_.close()
			return [a, b, c, d, delta, chi2, dof]




def read_data():
		
	TABL = open('tablet_GRB.txt')	

	tabl = pd.DataFrame(columns = ['DATA', 'DETECTOR', 'S1G1', 'S1G2', 'S1G3', 'S1G1er', 'S1G2er', 'S1G3er', 'S2G1', 'S2G2', 'S2G3', 'S2G1er', 'S2G2er', 'S2G3er'])
	tabl.index.name = 'ID'

	for _ in range(1):
		next(TABL)

	for line in	TABL:

		line = line.strip()
		line = line.split()	

		tabl.loc[line[1], :] = [line[5], line[7], float(line[16]), float(line[17]), float(line[18]), float(line[19]),
		 float(line[20]), float(line[21]), float(line[22]), float(line[23]), float(line[24]), float(line[25]), float(line[26]), float(line[27])]

	TABL.close()
	return tabl


def read_cal(det):
	CAL = dict()
	CAL_ = open('cal_' + det + '_fixed_man.txt')

	for _ in range(1):
		next(CAL_)

	for line in CAL_:
		if line.isspace() == True:
			continue
		line = line.strip()
		line = line.split()
		ID = line[0]
		cal = float(line[11])
		CAL[int(ID)] = cal

	CAL_.close()
	return CAL



def calc_cal_HR_fit(ID, cal, det, counts_and_er):
	#функция для перевода из исходых в номинальные
	kw_cuts = np.array([13.125, 50.0, 200.0, 750.0])

	#print(counts_and_er)

	fcal = get_fcal(ID, cal, det)

	counts = list(counts_and_er[0:3])
	counts_err = list(counts_and_er[3:6])


	cuts_cur = kw_cuts * fcal
	cuts_nom = kw_cuts
 
	fitter = fitter_3ch.Fitter(fitter_3ch.model('CPL'), cuts_cur, counts, counts_err)
	result, chi2 = fitter.fit()

       
	fitted_counts = fitter.model.int_func(result, cuts_nom[0:3], cuts_nom[1:4])
 
	return fitted_counts



def get_fcal(ID, cal, det):

	if int(ID) not in cal.keys():
		if det == 'S1':
			fcal = 2.061
		if det == 'S2':
			fcal = 1.637
	else:
		fcal = cal[int(ID)]	
	return fcal	



def get_R(Str, Sntr):
	R = (Sntr[1])/(Str[1])
	return R


def get_Incident_Angle(ID, R, parametrs, DATA):

	rad = 57.295779513082
	x = Symbol('x')
	x1 = solve(parametrs[0]*x**3 + parametrs[1]*x**2 + parametrs[2]*x + parametrs[3] - R, x)
	x2 = solve(parametrs[0]*x**3 + parametrs[1]*x**2 + parametrs[2]*x + parametrs[3] + parametrs[4] - R, x)
	x3 = solve(parametrs[0]*x**3 + parametrs[1]*x**2 + parametrs[2]*x + parametrs[3] - parametrs[4] - R, x)

	if x1[0] > 1:
		x1[0] = 1
	if x2[0] > 1:
		x2[0] = 1
	if x3[0] > 1:
		x3[0] = 1			

	with open('TASK_Incident_Angle.txt', 'a') as TASK:
		wr ="{:10s} {:10s} {:10.3f} {:10.3f} {:10.3f}\n".format(
			ID, DATA, math.acos(x1[0])*rad, math.acos(x2[0])*rad, math.acos(x3[0])*rad)
		TASK.write(str(wr))
	
	return #Incident_Angle




def main():
	canal = 'G2_'
	tabl = read_data()
	cal_S1 = read_cal('S1')
	cal_S2 = read_cal('S2')
	par_S1 = read_par('RG2G3_S1_LU_nom_1', 'S1')
	par_S2 = read_par('RG2G3_S2_LU_nom_1', 'S2')

	with open('TASK_Incident_Angle.txt', 'w') as TASK:
		wr = "{:10s} {:10s} {:10s} {:10s} {:10s}\n".format('ID', 'DATA', "real", "68up", "68doun")
		TASK.write(str(wr))

	ID_ = tabl.index.values

	for ID in ID_:

		if tabl.loc[ID, 'DETECTOR'] == 'S1':
			fitted_counts_tr = calc_cal_HR_fit(ID, cal_S1, tabl.loc[ID, 'DETECTOR'], tabl.loc[ID, ['S1G1', 'S1G2', 'S1G3', 'S1G1er', 'S1G2er', 'S1G3er']])
			fitted_counts_ntr = calc_cal_HR_fit(ID, cal_S1, tabl.loc[ID, 'DETECTOR'], tabl.loc[ID, ['S2G1', 'S2G2', 'S2G3', 'S2G1er', 'S2G2er', 'S2G3er']])
			parametrs = par_S1
		

		if tabl.loc[ID, 'DETECTOR'] == 'S2':
			fitted_counts_tr = calc_cal_HR_fit(ID, cal_S2, tabl.loc[ID, 'DETECTOR'], tabl.loc[ID, ['S2G1', 'S2G2', 'S2G3', 'S2G1er', 'S2G2er', 'S2G3er']])
			fitted_counts_ntr = calc_cal_HR_fit(ID, cal_S2, tabl.loc[ID, 'DETECTOR'], tabl.loc[ID, ['S1G1', 'S1G2', 'S1G3', 'S1G1er', 'S1G2er', 'S1G3er']])
			parametrs = par_S2

		R = get_R(fitted_counts_tr, fitted_counts_ntr)
		Incident_Angle = get_Incident_Angle(ID, R, parametrs, tabl.loc[ID, 'DATA'])

main()