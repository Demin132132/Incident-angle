#!/usr/bin/env python
# Short demo kmpfit (04-03-2012)


import numpy as np
import fitter_3ch
import json
from pylab import *
from scipy.optimize import minimize
from collections import defaultdict
from kapteyn import kmpfit
import function2
import math

TASK1 = open('tk1.txt', 'w')
TASK2 = open('tk2.txt', 'w')

#TEST1 = open('allS1_DS.txt')
#TEST2 = open('allS2_DS.txt')

TABL = open('table_well_loc_.txt')
NOM = open('nominal.txt')


aw = "{:4s} {:8s} {:15s} {:15s} {:15s} {:15s} {:15s} {:15s} {:15s} {:15s} {:15s} {:15s} {:15s} {:15s} {:15s} {:15s}{:15s} {:15s} {:15s} {:15s} {:15s} {:15s} {:15s} {:15s} {:15s} {:15s} {:15s} {:15s} {:15s} {:15s} {:15s} {:15s} {:15s} {:15s} {:15s}\n".format(
   	'  N', '       ', 'ID',  'DETECTOR', 'INSTR','cos_Tetta', "RG1", "erRG1", "RG2", "erRG2", "RG3", "erRG3", "RG2G3", "erRG2G3", "RG1G2", "erRG1G2", "RG1G2G3", "erRG1G2G3", "HRG1G2", "HRG2G3", "RG1nom", "erRG1nom", "RG2nom", "erRG2nom", "RG3nom", "erRG3nom", "RG2G3nom", "erRG2G3nom", "RG1G2nom", "erRG1G2nom", "RG1G2G3nom", "erRG1G2G3nom", "HRG1G2nom", "HRG2G3nom", 'LU')


TASK1.write(str(aw))
TASK2.write(str(aw))





bug = [4772, 387, 1863, 4128, 4499, 2998, 3163, 3253, 4093, 4103, 4111, 4201, 4445, 4594, 4123, 383, 3678, 4524, 4531, 4640]

#bug = [4794, 4795, 4803, 4814, 4808, 4846, 4845, 4834, 4833, 4830, 4826, 4825, 4820, 4819, 4817,  4772, 387, 1863, 4128, 4499, 2998, 3163, 3253, 4093, 4103, 4111, 4201, 4445, 4594, 4123, 383, 3678, 4524, 4531, 4640]
#сюда входят всплески со сбоями, а так же недавно добавленные в базу данных всплески, для которых я не имею значения калибровок
#bad = [1205, 1428 ,3757 ,4122 , 4504, 3493, 3286, 459, 4674,
#  2982 , 3357 ,3570 ,4696 , 2935, 4740,  ]
        
#bug = []  
bad = []   
      
   
bad2=[]
#bad2 = []


#bad=[3310, 4504, 3986, 2800,      3068,      4644,      4662,      4743,      3725,      4333,      4299,    459,      2587,      4129,      3218,      4569,      2938, 3487,      4102,      3974,      3230,      3436,      4028,      3480,      4552,      2010,      2508,      4438,      3755,      3767,      3921,      3210,      4243,      4713,      3535,      3994,      3312,      3095,      4113,      2737,      4314,      3902,      3478,      4124 ,3919, 4115, 3231, 4488, 1163, 3910, 1230, 3758, 3251, 4760, 2668, 4632, 2763, 4119]
      

cos_TettaS1 = dict()
RG2G3S1 = dict()
RG1S1 = dict()
RG2S1 = dict()
RG3S1 = dict()
RG2G3S1 = dict()
RG1G2S1 = dict()
RG1G2G3S1 = dict()


HRG1G2S1 = dict()
HRG2G3S1 = dict()

cos_TettaS2 = dict()
RG2G3S2 = dict()
RG1S2 = dict()
RG2S2 = dict()
RG3S2 = dict()
RG2G3S2 = dict()
RG1G2S2 = dict()
RG1G2G3S2 = dict()


HRG1G2S2 = dict()
HRG2G3S2 = dict()





RG2G3S1nom = dict()
RG1S1nom = dict()
RG2S1nom = dict()
RG3S1nom = dict()
RG2G3S1nom = dict()
RG1G2S1nom = dict()
RG1G2G3S1nom = dict()


RG2G3S2nom = dict()
RG1S2nom = dict()
RG2S2nom = dict()
RG3S2nom = dict()
RG2G3S2nom = dict()
RG1G2S2nom = dict()
RG1G2G3S2nom = dict()

erorG1S1_ = dict()
erorG2S1_ = dict()
erorG3S1_ = dict()

erorG2G3S1_ = dict()
erorG1G2G3S1_ = dict()
erorG1G2S1_ = dict()


erorG1S2_ = dict()
erorG2S2_ = dict()
erorG3S2_ = dict()

erorG2G3S2_ = dict()
erorG1G2G3S2_ = dict()
erorG1G2S2_ = dict()

erorG1S1_nom = dict()
erorG2S1_nom = dict()
erorG3S1_nom = dict()

erorG2G3S1_nom = dict()
erorG1G2G3S1_nom = dict()
erorG1G2S1_nom = dict()


erorG1S2_nom = dict()
erorG2S2_nom = dict()
erorG3S2_nom = dict()

erorG2G3S2_nom = dict()
erorG1G2G3S2_nom = dict()
erorG1G2S2_nom = dict()


HRG1G2S1nom = dict()
HRG2G3S1nom = dict()

LUM_S1_t = dict()
LUM_S2_t = dict()

HRG1G2S1_t = dict()
HRG1G2S2_t = dict()

HRG1G2S1nom_t = dict()
HRG1G2S2nom_t = dict()

HRG1G2S2nom = dict()
HRG2G3S2nom = dict()

IDS1 = dict()
IDS2 = dict()

LUM_S1 = dict()
LUM_S2 = dict()

LUM_for_S2 = dict()
LUM_for_S1 = dict()



erorG1S1_=dict()
erorG1S1_2=dict()


er_test1 = dict()


ERRS1 = dict()
ERRS2 = dict()

test1=[]
test2=[]

counter1 = 0
counter2 = 0

a = []
counter_ = 0

for _ in range(1):
	next(TEST1)
for _ in range(1):
	next(TEST2)
for _ in range(1):
	next(TABL)
for _ in range(1):
	next(NOM)	

for line in TEST1:
	line = line.strip()
	line = line.split()
	ID = int(line[0])

	test1.append(ID)

for line in TEST2:
	line = line.strip()
	line = line.split()
	ID = int(line[0])

	test2.append(ID)


for line, line1 in zip(TABL, NOM):
	line = line.strip()
	line = line.split()

	line1 = line1.strip()
	line1 = line1.split()

	DETECTOR = line[7]
	ID = int(line[1])

	if ID in bug:
		continue

	S1G1 = float(line[16])
	S1G2 = float(line[17])
	S1G3 = float(line[18])
	S1G1er = float(line[19])
	S1G2er = float(line[20])
	S1G3er = float(line[21])
	S2G1 = float(line[22])
	S2G2 = float(line[23])
	S2G3 = float(line[24])
	S2G1er = float(line[25])
	S2G2er = float(line[26])
	S2G3er = float(line[27])


	S1BG1 = float(line[35])
	S1BG2 = float(line[36])
	S1BG3 = float(line[37])
	S2BG1 = float(line[38])
	S2BG2 = float(line[39])
	S2BG3 = float(line[40])


	S1G1nom = float(line1[1])
	S1G2nom = float(line1[2])
	S1G3nom = float(line1[3])
	S2G1nom = float(line1[4])
	S2G2nom = float(line1[5])
	S2G3nom = float(line1[6])


	S1BG1nom = float(line1[7])
	S1BG2nom = float(line1[8])
	S1BG3nom = float(line1[9])
	S2BG1nom = float(line1[10])
	S2BG2nom = float(line1[11])
	S2BG3nom = float(line1[12])


	


	if ID in bad or ID in bad2:
		continue

	A = float(line[30])
	D = float(line[31])
	time = float(line[9])

	if time < 3:
		continue





	if DETECTOR == "S1":

		#if ID not in test1:
		#	continue

		eps = 23.43/57.2958
		sinB = math.cos(eps) * math.sin(D/57.2958) - math.sin(eps) * math.cos(D/57.2958) * math.sin(A/57.2958)
		cos_Tetta = - sinB
		Tetta = math.acos(cos_Tetta) * 57.2958
		
		#counter_
		if Tetta > 90: #or Tetta < 60:
			counter_=counter_+1
			continue

		#if Tetta > 90: 
		#	cos_Tetta = - cos_Tetta		
			

		RG1_ = S2G1/S1G1
		RG2_ = S2G2/S1G2
		RG3_ = S2G3/S1G3
			
		RG2G3_ = (S2G2+S2G3)/(S1G2+S1G3)
		RG1G2_ = (S2G1+S2G2)/(S1G1+S1G2)
		RG1G2G3_ = (S2G1+S2G2+S2G3)/(S1G1+S1G2+S1G3)

		HRG1G2_ = (S1G2)/(S1G1)
		HRG2G3_ = (S1G3)/(S1G2)

		
		RG1_nom = S2G1nom/S1G1nom
		RG2_nom = S2G2nom/S1G2nom
		RG3_nom = S2G3nom/S1G3nom
			
		RG2G3_nom = (S2G2nom+S2G3nom)/(S1G2+S1G3)
		RG1G2_nom = (S2G1nom+S2G2nom)/(S1G1+S1G2)
		RG1G2G3_nom = (S2G1nom+S2G2nom+S2G3nom)/(S1G1nom+S1G2nom+S1G3nom)






		HRG1G2_nom = (S1G2nom)/(S1G1nom)
		HRG2G3_nom = (S1G3nom)/(S1G2nom)

			
			
		LUS1 = (S1G1 + S1G2 + S1G3)
		if LUS1 > 190000000 or LUS1 <= 491.57300000000004:
		#491.57300000000004 295.84900000000005
			continue
		LUM_S1[LUS1] = cos_Tetta
		LUM_S1_t[LUS1]= cos_Tetta
		LUM_for_S1[LUS1] = ID

		IDS1[ID] = DETECTOR	



		cos_TettaS1[ID] = cos_Tetta
		RG1S1[cos_Tetta] = RG1_
		RG2S1[cos_Tetta] = RG2_
		RG3S1[cos_Tetta] = RG3_
		RG2G3S1[cos_Tetta] = RG2G3_
		RG1G2S1[cos_Tetta] = RG1G2_
		RG1G2G3S1[cos_Tetta] = RG1G2G3_
		HRG1G2S1[HRG1G2_] = cos_Tetta
		HRG1G2S1_t[HRG1G2_] = cos_Tetta
		HRG2G3S1[HRG2G3_] = cos_Tetta


		RG2G3S1nom[cos_Tetta] = RG2G3_nom
		RG1S1nom[cos_Tetta] = RG1_nom
		RG2S1nom[cos_Tetta] = RG2_nom
		RG3S1nom[cos_Tetta] = RG3_nom
		RG2G3S1nom[cos_Tetta] = RG2G3_nom
		RG1G2S1nom[cos_Tetta] = RG1G2_nom
		RG1G2G3S1nom[cos_Tetta] = RG1G2G3_nom

		HRG1G2S1nom[HRG1G2_nom] = cos_Tetta
		HRG1G2S1nom_t[HRG1G2_nom] = cos_Tetta
		HRG2G3S1nom[HRG2G3_nom] = cos_Tetta	

		
		#print(er_test1[cos_Tetta], erorG2G3S1_[cos_Tetta] )
		#er_test1[cos_Tetta] = np.sqrt((S2G2er**2 + S2G3er**2)/((S1G2+S1G3)**2) + ((S2G2 + S2G3)**2)*(S1G2er**2 + S1G3er**2)/((S1G2 + S1G3)**4))
		#print(erorG1S1_[cos_Tetta], erorG1S1_2[cos_Tetta])





		erorG1S1_[cos_Tetta] = (((S2G1er/S2G1)**2 + (S1G1er/S1G1)**2)**0.5)*RG1_
		erorG2S1_[cos_Tetta] = (((S2G2er/S2G2)**2 + (S1G2er/S1G2)**2)**0.5)*RG2_
		erorG3S1_[cos_Tetta] = (((S2G3er/S2G3)**2 + (S1G3er/S1G3)**2)**0.5)*RG3_
		erorG2G3S1_[cos_Tetta] = ((S2G2+S2G3)/(S1G2+S1G3))*((((np.sqrt(S2G2er**2 + S2G3er**2))/(S2G2+S2G3))**2 + ((np.sqrt(S1G2er**2 + S1G3er**2))/(S1G2+S1G3))**2)**0.5)
		erorG1G2S1_[cos_Tetta] = ((S2G2+S2G1)/(S1G1+S1G2))*((((np.sqrt(S2G2er**2 + S2G1er**2))/(S2G2+S2G1))**2 + ((np.sqrt(S1G2er**2 + S1G1er**2))/(S1G2+S1G1))**2)**0.5)
		erorG1G2G3S1_[cos_Tetta] = ((S2G2+S2G3+S2G1)/(S1G2+S1G3+S1G1))*((((np.sqrt(S2G2er**2 + S2G3er**2 + S2G1er**2))/(S2G2+S2G3+S2G1))**2 + ((np.sqrt(S1G2er**2 + S1G3er**2 + S1G1er**2))/(S1G2+S1G3+S1G1))**2)**0.5)
		

		
		erorG1S1_nom[cos_Tetta] = RG1_nom*np.sqrt((np.sqrt(S1BG1nom + S1G1nom)/(S1G1nom))**2 + (np.sqrt(S2BG1nom + S2G1nom)/(S2G1nom))**2)
		#erorG1S1_2[cos_Tetta] = np.sqrt((S2BG1nom + S2G1nom)/(S1G1nom**2) + (S2G1nom**2)*(S1BG1nom + S1G1nom)/(S1G1nom**4))
		#print(ID, erorG1S1_nom[cos_Tetta], erorG1S1_2[cos_Tetta])
		#print(S1G1nom, np.sqrt((S1BG1nom + S1G1nom)),  '    ', S2G1nom, np.sqrt((S2BG1nom + S2G1nom)))
		erorG2S1_nom[cos_Tetta] = RG2_nom*np.sqrt((np.sqrt(S1BG2nom + S1G2nom)/(S1G2nom))**2 + (np.sqrt(S2BG2nom + S2G2nom)/(S2G2nom))**2)
		erorG3S1_nom[cos_Tetta] = RG3_nom*np.sqrt((np.sqrt(S1BG3nom + S1G3nom)/(S1G3nom))**2 + (np.sqrt(S2BG3nom + S2G3nom)/(S2G3nom))**2)
		erorG2G3S1_nom[cos_Tetta] = RG2G3_nom*np.sqrt((np.sqrt(S1BG2nom + S1G2nom + S1BG3nom + S1G3nom)/(S1G3nom + S1G2nom))**2 + (np.sqrt(S2BG2nom + S2G2nom + S2BG3 + S2G3nom)/(S2G3nom + S2G2nom))**2)
		erorG1G2S1_nom[cos_Tetta] = RG1G2_nom*np.sqrt((np.sqrt(S1BG2nom + S1G2nom + S1BG1nom + S1G1nom)/(S1G1nom + S1G2nom))**2 + (np.sqrt(S2BG2nom + S2G2nom + S2BG1 + S2G1nom)/(S2G1nom + S2G2nom))**2)
		erorG1G2G3S1_nom[cos_Tetta] = RG1G2G3_nom*np.sqrt((np.sqrt(S1BG2nom + S1G2nom + S1BG1nom + S1G1nom + S1BG3nom + S1G3nom)/(S1G1nom + S1G2nom + S1G3nom))**2 + (np.sqrt(S2BG3nom + S2G3nom + S2BG2nom + S2G2nom + S2BG1nom + S2G1nom)/(S2G3nom + S2G1nom + S2G2nom))**2)

		#if erorG3S1_nom[cos_Tetta] > RG3_nom:
		#	print(LUS1)



		ERRS1[cos_Tetta] = ID	

		counter1 = counter1 + 1

		awwww = "{:3.0f} {:9s} {:15s} {:15s} {:15s} {:4.3f} {:15.3f} {:15.3f} {:15.3f} {:15.3f} {:15.3f} {:15.3f} {:15.3f} {:15.3f} {:15.3f} {:15.3f} {:15.3f} {:15.3f} {:15.3f} {:15.3f} {:15.3f} {:15.3f} {:15.3f} {:15.3f} {:15.3f} {:15.3f} {:15.3f} {:15.3f} {:15.3f} {:15.3f} {:15.3f} {:15.3f} {:15.3f} {:15.3f} {:15.3f}\n".format( 
			counter1, '         ', str(ID), 'S1', line[3], cos_Tetta, RG1_, erorG1S1_[cos_Tetta], RG2_, erorG2S1_[cos_Tetta], RG3_, erorG3S1_[cos_Tetta], RG2G3_, erorG2G3S1_[cos_Tetta], RG1G2_, erorG1G2S1_[cos_Tetta], RG1G2G3_, erorG1G2G3S1_[cos_Tetta], HRG1G2_, HRG2G3_, RG1_nom, erorG1S1_nom[cos_Tetta], RG2_nom, erorG2S1_nom[cos_Tetta], RG3_nom, erorG3S1_nom[cos_Tetta], RG2G3_nom, erorG2G3S1_nom[cos_Tetta], RG1G2_nom, erorG1G2S1_nom[cos_Tetta], RG1G2G3_nom, erorG1G2G3S1_nom[cos_Tetta], HRG1G2_nom, HRG2G3_nom, LUS1)
			
		TASK1.write(str(awwww))

			

			

			
	if DETECTOR == 'S2':
		
		#if ID not in test2:
		#	continue

		eps = 23.43/57.2958
		sinB = math.cos(eps) * math.sin(D/57.2958) - math.sin(eps) * math.cos(D/57.2958) * math.sin(A/57.2958)
		cos_Tetta = sinB
		Tetta = math.acos(cos_Tetta) * 57.2958
		

		if Tetta > 90:# or Tetta < 60: 
			continue
		


		RG1_ = S1G1/S2G1
		RG2_ = S1G2/S2G2
		RG3_ = S1G3/S2G3
			
		RG2G3_ = (S1G2+S1G3)/(S2G2+S2G3)
		RG1G2_ = (S1G1+S1G2)/(S2G1+S2G2)
		RG1G2G3_ = (S1G1+S1G2+S1G3)/(S2G1+S2G2+S2G3)


		HRG1G2_ = (S2G2)/(S2G1)
		HRG2G3_ = (S2G3)/(S2G2)




		RG1_nom = S1G1nom/S2G1nom
		RG2_nom = S1G2nom/S2G2nom
		RG3_nom = S1G3nom/S2G3nom
			
		RG2G3_nom = (S1G2nom+S1G3nom)/(S2G2+S2G3)
		RG1G2_nom = (S1G1nom+S1G2nom)/(S2G1+S2G2)
		RG1G2G3_nom = (S1G1nom+S1G2nom+S1G3nom)/(S2G1nom+S2G2nom+S2G3nom)

		HRG1G2_nom = (S2G2nom)/(S2G1nom)
		HRG2G3_nom = (S2G3nom)/(S2G2nom)



		IDS2[ID] = DETECTOR

		LUS2 = (S2G1 + S2G2 + S2G3)

		if LUS2 > 190000000 or LUS2 <=474.31600000000003  :
		#	a.append(1)#  225.928
			continue
		LUM_S2[LUS2] = cos_Tetta
		LUM_S2_t[LUS2] = cos_Tetta
		LUM_for_S2[LUS2] = ID


		cos_TettaS2[ID] = cos_Tetta
		RG2G3S2[cos_Tetta] = RG2G3_
		RG1S2[cos_Tetta] = RG1_
		RG2S2[cos_Tetta] = RG2_
		RG3S2[cos_Tetta] = RG3_
		RG2G3S2[cos_Tetta] = RG2G3_
		RG1G2S2[cos_Tetta] = RG1G2_
		RG1G2G3S2[cos_Tetta] = RG1G2G3_
		HRG1G2S2[HRG1G2_] = cos_Tetta
		HRG1G2S2_t[HRG1G2_] = cos_Tetta
		HRG2G3S2[HRG2G3_] = cos_Tetta

		RG2G3S2nom[cos_Tetta] = RG2G3_nom
		RG1S2nom[cos_Tetta] = RG1_nom
		RG2S2nom[cos_Tetta] = RG2_nom
		RG3S2nom[cos_Tetta] = RG3_nom
		RG2G3S2nom[cos_Tetta] = RG2G3_nom
		RG1G2S2nom[cos_Tetta] = RG1G2_nom
		RG1G2G3S2nom[cos_Tetta] = RG1G2G3_nom

		HRG1G2S2nom[HRG1G2_nom] = cos_Tetta
		HRG1G2S2nom_t[HRG1G2_nom] = cos_Tetta
		HRG2G3S2nom[HRG2G3_nom] = cos_Tetta
			
			
		erorG1S2_[cos_Tetta] = RG1_*((S2G1er/S2G1)**2 + (S1G1er/S1G1)**2)**0.5
		erorG2S2_[cos_Tetta] = RG2_*((S2G2er/S2G2)**2 + (S1G2er/S1G2)**2)**0.5
		erorG3S2_[cos_Tetta] = RG3_*((S2G3er/S2G3)**2 + (S1G3er/S1G3)**2)**0.5
		erorG2G3S2_[cos_Tetta] = (S1G2+S1G3)/(S2G2+S2G3)*((((np.sqrt(S2G2er**2 + S2G3er**2))/(S2G2+S2G3))**2 + ((np.sqrt(S1G2er**2 + S1G3er**2))/(S1G2+S1G3))**2)**0.5)
		erorG1G2S2_[cos_Tetta] = (S1G1+S1G2)/(S2G1+S2G2)*((((np.sqrt(S2G2er**2 + S2G1er**2))/(S2G2+S2G1))**2 + ((np.sqrt(S1G2er**2 + S1G1er**2))/(S1G2+S1G1))**2)**0.5)
		erorG1G2G3S2_[cos_Tetta] = (S1G2+S1G3+S1G1)/(S2G2+S2G3+S2G1)*((((np.sqrt(S2G2er**2 + S2G3er**2 + S2G1er**2))/(S2G2+S2G3+S2G1))**2 + ((np.sqrt(S1G2er**2 + S1G3er**2 + S1G1er**2))/(S1G2+S1G3+S1G1))**2)**0.5)
		ERRS2[cos_Tetta] = ID	
		

		erorG1S2_nom[cos_Tetta] = RG1_nom*np.sqrt((np.sqrt(S1BG1nom + S1G1nom)/(S1G1nom))**2 + (np.sqrt(S2BG1nom + S2G1nom)/(S2G1nom))**2)
		erorG2S2_nom[cos_Tetta] = RG2_nom*np.sqrt((np.sqrt(S1BG2nom + S1G2nom)/(S1G2nom))**2 + (np.sqrt(S2BG2nom + S2G2nom)/(S2G2nom))**2)
		erorG3S2_nom[cos_Tetta] = RG3_nom*np.sqrt((np.sqrt(S1BG3nom + S1G3nom)/(S1G3nom))**2 + (np.sqrt(S2BG3nom + S2G3nom)/(S2G3nom))**2)
		erorG2G3S2_nom[cos_Tetta] = RG2G3_nom*np.sqrt((np.sqrt(S1BG2nom + S1G2nom + S1BG3nom + S1G3nom)/(S1G3nom + S1G2nom))**2 + (np.sqrt(S2BG2nom + S2G2nom + S2BG3nom + S2G3nom)/(S2G3nom + S2G2nom))**2)
		erorG1G2S2_nom[cos_Tetta] = RG1G2_nom*np.sqrt((np.sqrt(S1BG2nom + S1G2nom + S1BG1nom + S1G1nom)/(S1G1nom + S1G2nom))**2 + (np.sqrt(S2BG2nom + S2G2nom + S2BG1nom + S2G1nom)/(S2G1nom + S2G2nom))**2)
		erorG1G2G3S2_nom[cos_Tetta] = RG1G2G3_nom*np.sqrt((np.sqrt(S1BG2nom + S1G2nom + S1BG1nom + S1G1nom + S1BG3nom + S1G3nom)/(S1G1nom + S1G2nom +  S1G3nom))**2 + (np.sqrt(S2BG3nom + S2G3nom + S2BG2nom + S2G2nom + S2BG1nom + S2G1nom)/(S2G3nom + S2G1nom + S2G2nom))**2)



		counter2 = counter2+1

		awwww = "{:3.0f} {:9s} {:15s} {:15s} {:15s} {:4.3f} {:15.3f} {:15.3f} {:15.3f} {:15.3f} {:15.3f} {:15.3f} {:15.3f} {:15.3f} {:15.3f} {:15.3f} {:15.3f} {:15.3f} {:15.3f} {:15.3f} {:15.3f} {:15.3f} {:15.3f} {:15.3f} {:15.3f} {:15.3f} {:15.3f} {:15.3f} {:15.3f} {:15.3f} {:15.3f} {:15.3f} {:15.3f} {:15.3f} {:15.3f}\n".format( 
		counter2, '         ', str(ID), 'S2', line[3], cos_Tetta, RG1_, erorG1S2_[cos_Tetta], RG2_, erorG2S2_[cos_Tetta], RG3_, erorG3S2_[cos_Tetta], RG2G3_, erorG2G3S2_[cos_Tetta], RG1G2_, erorG1G2S2_[cos_Tetta], RG1G2G3_, erorG1G2G3S2_[cos_Tetta], HRG1G2_, HRG2G3_, RG1_nom, erorG1S2_nom[cos_Tetta], RG2_nom, erorG2S2_nom[cos_Tetta], RG3_nom, erorG3S2_nom[cos_Tetta], RG2G3_nom, erorG2G3S2_nom[cos_Tetta], RG1G2_nom, erorG1G2S2_nom[cos_Tetta], RG1G2G3_nom, erorG1G2G3S2_nom[cos_Tetta], HRG1G2_nom, HRG2G3_nom, LUS2)
		
		TASK2.write(str(awwww))


wr2 = "{:10s} {:10s} {:10s} {:10s} {:10s} {:10s} {:10s} {:10s}\n".format(
			 'chi2r', 'delta', 'dof', 'a', 'b', 'c', 'd', 'Canal') 

"""
parametrS1_2 = open('parametrs_S1.txt', 'w')
parametrS1_2.write(str(wr2))
parametrS1_2.close()	
parametrS2_2 = open('parametrs_S2.txt', 'w')
parametrS2_2.write(str(wr2))
parametrS2_2.close()		
"""
function2.graf(RG2G3S1, erorG2G3S1_, ERRS1, [1],  0.95,  'cos_Tetta', 'RG2G3_S1', A = 0, B = 1)


hr1=dict()
hr2=dict()
for k, v in HRG1G2S1.items():
	hr1[v]=k
for k, v in HRG1G2S2.items():
	hr2[v]=k

hr1_nom=dict()
hr2_nom=dict()
for k, v in HRG1G2S1nom.items():
	hr1_nom[v]=k
for k, v in HRG1G2S2nom.items():
	hr2_nom[v]=k


#HRG1G2S1_t = dict()
#HRG1G2S2_t = dict()




lu1=dict()
lu2=dict()
for k, v in LUM_S1.items():
	lu1[v]=k
for k, v in LUM_S2.items():
	lu2[v]=k
"""
parametrS1 = open('P_S1.txt', 'w')
parametrS1.close()

parametrS2 = open('P_S2.txt', 'w')
parametrS2.close()

function2.build(RG2S1nom,  LUM_S1, erorG2S1_nom, ERRS1, [1,2], 0.68, 2,'cos_Tetta', 'RG2_S1_LU_nom')
function2.build(RG2S2nom,  LUM_S2, erorG2S2_nom, ERRS2, [1,2], 0.68, 2, 'cos_Tetta', 'RG2_S2_LU_nom')

function2.build(RG2G3S1nom,  LUM_S1, erorG2G3S1_nom, ERRS1, [1,2], 0.68, 2, 'cos_Tetta', 'RG2G3_S1_LU_nom')
function2.build(RG2G3S2nom,  LUM_S2, erorG2G3S2_nom, ERRS2, [1,2], 0.68, 2, 'cos_Tetta', 'RG2G3_S2_LU_nom')



#function2.build(RG2S1nom, HRG2G3S1nom, erorG2S1_nom, ERRS1, [1,2,3], 0.68, 3,'cos_Tetta', 'RG2_S1_HR_nom')
#function2.build(RG2S2nom, HRG2G3S2nom, erorG2S2_nom, ERRS2, [1,2,3], 0.68, 3, 'cos_Tetta', 'RG2_S2_HR_nom')

function2.graf(RG2G3S1nom, HRG2G3S1nom, erorG2G3S1_nom, ERRS1, [1], 0.68, 1, 'cos_Tetta', 'RG2G3_S1_HR_nom')
function2.graf(RG2G3S2nom, HRG2G3S2nom, erorG2G3S2_nom, ERRS2, [1], 0.68, 1, 'cos_Tetta', 'RG2G3_S2_HR_nom')

"""



#LUM_S1_t=LUM_S1
#LUM_S2_t=LUM_S2	
"""
del RG1S1[cos_TettaS1[1428]] , RG1S1[cos_TettaS1[4122]], RG1S1[cos_TettaS1[3757]], RG1S1[cos_TettaS1[4504]], RG1S1[cos_TettaS1[1205]]
del RG1S2[cos_TettaS2[4740]], RG1S2[cos_TettaS2[2982]], RG1S2[cos_TettaS2[2935]]
del RG1G2S1[cos_TettaS1[1428]], RG1G2S1[cos_TettaS1[4122]], RG1G2S1[cos_TettaS1[3757]], RG1G2S1[cos_TettaS1[4504]], RG1G2S1[cos_TettaS1[1205]]
del RG1G2S2[cos_TettaS2[4740]], RG1G2S2[cos_TettaS2[2982]], RG1G2S2[cos_TettaS2[2935]]


del HRG1G2S1_t[hr1[cos_TettaS1[1428]]], HRG1G2S1_t[hr1[cos_TettaS1[4122]]], HRG1G2S1_t[hr1[cos_TettaS1[3757]]], HRG1G2S1_t[hr1[cos_TettaS1[4504]]], HRG1G2S1_t[hr1[cos_TettaS1[1205]]]
del HRG1G2S2_t[hr2[cos_TettaS2[4740]]], HRG1G2S2_t[hr2[cos_TettaS2[2982]]], HRG1G2S2_t[hr2[cos_TettaS2[2935]]]

del LUM_S1_t[lu1[cos_TettaS1[1428]]], LUM_S1_t[lu1[cos_TettaS1[4122]]], LUM_S1_t[lu1[cos_TettaS1[3757]]], LUM_S1_t[lu1[cos_TettaS1[4504]]], LUM_S1_t[lu1[cos_TettaS1[1205]]]
del LUM_S2_t[lu2[cos_TettaS2[4740]]], LUM_S2_t[lu2[cos_TettaS2[2982]]], LUM_S2_t[lu2[cos_TettaS2[2935]]]

"""
"""

function2.graf(RG1S1, erorG1S1_, ERRS1, [1],  0.95,  'cos_Tetta', 'RG1_S1', A = 0, B = 0.55)
function2.graf(RG2S1, erorG2S1_, ERRS1, [1],  0.95,  'cos_Tetta', 'RG2_S1', A = 0, B = 0.55)
function2.graf(RG1G2S1, erorG1G2S1_, ERRS1, [1],  0.95,  'cos_Tetta', 'RG1G2_S1', A = 0, B = 0.55)
function2.graf(RG2G3S1, erorG2G3S1_, ERRS1, [1],  0.95,  'cos_Tetta', 'RG2G3_S1', A = 0, B = 0.55)
function2.graf(RG1G2G3S1, erorG1G2G3S1_, ERRS1, [1],  0.95,  'cos_Tetta', 'RG1G2G3_G1G2G3S1', A = 0, B = 0.55)


function2.graf(RG1S2, erorG1S2_, ERRS2, [1],  0.95,  'cos_Tetta', 'RG1_S2', A = 0, B = 0.55)
function2.graf(RG2S2, erorG2S2_, ERRS2, [1],  0.95,  'cos_Tetta', 'RG2_S2', A = 0, B = 0.55)
function2.graf(RG1G2S2, erorG1G2S2_, ERRS2, [1],  0.95,  'cos_Tetta', 'RG1G2_S2', A = 0, B = 0.55)
function2.graf(RG2G3S2, erorG2G3S2_, ERRS2, [1],  0.95,  'cos_Tetta', 'RG2G3_S2', A = 0, B = 0.55)
function2.graf(RG1G2G3S2, erorG1G2G3S2_, ERRS2, [1],  0.95,  'cos_Tetta', 'RG1G2G3_G1G2G3S2', A = 0, B = 0.55)
function2.print_chi('G3')











function2.build(RG2S1, HRG1G2S1, erorG2S1_, ERRS1, [1,2,3], 0.95, 3, 'cos_Tetta', 'RG2_S1_HR')
function2.build(RG2S2, HRG1G2S2, erorG2S2_, ERRS2, [1,2,3], 0.95, 3, 'cos_Tetta', 'RG2_S2_HR')

function2.build(RG1G2S1, HRG1G2S1_t, erorG1G2S1_, ERRS1, [1,2,3], 0.95, 3, 'cos_Tetta', 'RG1G2_S1_HR')
function2.build(RG1G2S2, HRG1G2S2_t, erorG1G2S2_, ERRS2, [1,2,3], 0.95, 3, 'cos_Tetta', 'RG1G2_S2_HR')

function2.build(RG2G3S1, HRG1G2S1, erorG2G3S1_, ERRS1, [1,2,3], 0.95, 3, 'cos_Tetta', 'RG2G3_S1_HR')
function2.build(RG2G3S2, HRG1G2S2, erorG2G3S2_, ERRS2, [1,2,3], 0.95, 3, 'cos_Tetta', 'RG2G3_S2_HR')




function2.build(RG2S1, LUM_S1, erorG2S1_, ERRS1, [1,2,3],  0.95, 3, 'cos_Tetta', 'RG2_S1_LU')
function2.build(RG2S2, LUM_S2, erorG2S2_, ERRS2, [1,2,3],  0.95, 3, 'cos_Tetta', 'RG2_S2_LU')

function2.build(RG1G2S1, LUM_S1_t, erorG1G2S1_, ERRS1, [1,2,3],  0.95, 3, 'cos_Tetta', 'RG1G2_S1_LU')
function2.build(RG1G2S2, LUM_S2_t, erorG1G2S2_, ERRS2, [1,2,3],  0.95, 3, 'cos_Tetta', 'RG1G2_S2_LU')

function2.build(RG2G3S1, LUM_S1, erorG2G3S1_, ERRS1, [1,2,3],  0.95, 3, 'cos_Tetta', 'RG2G3_S1_LU')

function2.build(RG2G3S2, LUM_S2, erorG2G3S2_, ERRS2, [1,2,3],  0.95, 3, 'cos_Tetta', 'RG2G3_S2_LU')



"""



"""
if 1428 in cos_TettaS1.keys():
	del RG1S1nom[cos_TettaS1[1428]]
	del RG1G2S1nom[cos_TettaS1[1428]]
	del HRG1G2S1nom_t[hr1_nom[cos_TettaS1[1428]]]
	del LUM_S1_t[lu1[cos_TettaS1[1428]]]

if 4122 in cos_TettaS1.keys():
	del RG1S1nom[cos_TettaS1[4122]]
	del RG1G2S1nom[cos_TettaS1[4122]]
	del HRG1G2S1nom_t[hr1_nom[cos_TettaS1[4122]]]
	del LUM_S1_t[lu1[cos_TettaS1[4122]]]

if 3757 in cos_TettaS1.keys():
	del RG1S1nom[cos_TettaS1[3757]]
	del RG1G2S1nom[cos_TettaS1[3757]]
	del HRG1G2S1nom_t[hr1_nom[cos_TettaS1[3757]]]
	del LUM_S1_t[lu1[cos_TettaS1[3757]]]

if 4504 in cos_TettaS1.keys():
	del RG1S1nom[cos_TettaS1[4504]]
	del RG1G2S1nom[cos_TettaS1[4504]]
	del HRG1G2S1nom_t[hr1_nom[cos_TettaS1[4504]]]
	del LUM_S1_t[lu1[cos_TettaS1[4504]]]

if 1205 in cos_TettaS1.keys():
	del RG1S1nom[cos_TettaS1[1205]]
	del RG1G2S1nom[cos_TettaS1[1205]]
	del HRG1G2S1nom_t[hr1_nom[cos_TettaS1[1205]]]
	del LUM_S1_t[lu1[cos_TettaS1[1205]]]





if 4740 in cos_TettaS2.keys():
	del RG1S2nom[cos_TettaS2[4740]]
	del RG1G2S2nom[cos_TettaS2[4740]]
	del HRG1G2S2nom_t[hr2_nom[cos_TettaS2[4740]]]
	del LUM_S2_t[lu1[cos_TettaS1[4740]]]

if 2982 in cos_TettaS1.keys():
	del RG1S2nom[cos_TettaS2[2982]]
	del RG1G2S2nom[cos_TettaS2[2982]]
	del HRG1G2S2nom_t[hr2_nom[cos_TettaS2[2982]]]
	del LUM_S2_t[lu1[cos_TettaS1[2982]]]

if 2935 in cos_TettaS1.keys():
	del RG1S2nom[cos_TettaS2[2935]]
	del RG1G2S2nom[cos_TettaS2[2935]]
	del HRG1G2S2nom_t[hr2_nom[cos_TettaS2[2935]]]
	del LUM_S2_t[lu1[cos_TettaS1[2935]]]




function2.build(RG2S1nom,  LUM_S1, erorG2S1_nom, ERRS1, [1,2,3], 0.95, 3,'cos_Tetta', 'RG2_S1_LU_nom')
function2.build(RG2S2nom,  LUM_S2, erorG2S2_nom, ERRS2, [1,2,3], 0.95, 3, 'cos_Tetta', 'RG2_S2_LU_nom')

function2.build(RG1G2S1nom,  LUM_S1_t, erorG1G2S1_nom, ERRS1, [1,2,3], 0.95, 3,'cos_Tetta', 'RG1G2_S1_LU_nom')
function2.build(RG1G2S2nom,  LUM_S2_t, erorG1G2S2_nom, ERRS2, [1,2,3], 0.95, 3,'cos_Tetta', 'RG1G2_S2_LU_nom')

function2.build(RG2G3S1nom,  LUM_S1, erorG2G3S1_nom, ERRS1, [1,2,3], 0.95, 3, 'cos_Tetta', 'RG2G3_S1_LU_nom')
function2.build(RG2G3S2nom,  LUM_S2, erorG2G3S2_nom, ERRS2, [1,2,3], 0.95, 3, 'cos_Tetta', 'RG2G3_S2_LU_nom')



function2.build(RG2S1nom, HRG1G2S1nom, erorG2S1_nom, ERRS1, [1,2,3], 0.95, 3,'cos_Tetta', 'RG2_S1_HR_nom')
function2.build(RG2S2nom, HRG1G2S2nom, erorG2S2_nom, ERRS2, [1,2,3], 0.95, 3, 'cos_Tetta', 'RG2_S2_HR_nom')

function2.build(RG1G2S1nom, HRG1G2S1nom_t, erorG1G2S1_nom, ERRS1, [1,2,3], 0.95, 3,'cos_Tetta', 'RG1G2_S1_HR_nom')
function2.build(RG1G2S2nom, HRG1G2S2nom_t, erorG1G2S2_nom, ERRS2, [1,2,3], 0.95, 3,'cos_Tetta', 'RG1G2_S2_HR_nom')

function2.build(RG2G3S1nom, HRG1G2S1nom, erorG2G3S1_nom, ERRS1, [1,2,3], 0.95,3, 'cos_Tetta', 'RG2G3_S1_HR_nom')
function2.build(RG2G3S2nom, HRG1G2S2nom, erorG2G3S2_nom, ERRS2, [1,2,3], 0.95, 3, 'cos_Tetta', 'RG2G3_S2_HR_nom')







function2.build(RG1S1nom,  LUM_S1_t, erorG1S1_nom, ERRS1, [1,2,3], 0.95, 3, 'cos_Tetta', 'RG1_S1_LU_nom')
function2.build(RG2S1nom,  LUM_S1, erorG2S1_nom, ERRS1, [1,2,3], 0.95, 3,'cos_Tetta', 'RG2_S1_LU_nom')
function2.build(RG3S1nom,  LUM_S1, erorG3S1_nom, ERRS1, [1,2,3], 0.95, 3, 'cos_Tetta', 'RG3_S1_LU_nom')
function2.build(RG1G2S1nom,  LUM_S1_t, erorG1G2S1_nom, ERRS1, [1,2,3], 0.95, 3,'cos_Tetta', 'RG1G2_S1_LU_nom')
function2.build(RG2G3S1nom,  LUM_S1, erorG2G3S1_nom, ERRS1, [1,2,3], 0.95, 3, 'cos_Tetta', 'RG2G3_S1_LU_nom')
function2.build(RG1G2G3S1nom,  LUM_S1, erorG1G2G3S1_nom, ERRS1, [1,2,3], 0.95, 3,'cos_Tetta', 'RG1G2G3_S1_LU_nom')



function2.build(RG1S2nom,  LUM_S2_t, erorG1S2_nom, ERRS2, [1,2,3], 0.95, 3, 'cos_Tetta', 'RG1_S2_LU_nom')
function2.build(RG2S2nom,  LUM_S2, erorG2S2_nom, ERRS2, [1,2,3], 0.95, 3, 'cos_Tetta', 'RG2_S2_LU_nom')
function2.build(RG3S2nom,  LUM_S2, erorG3S2_nom, ERRS2, [1,2,3], 0.95, 3, 'cos_Tetta', 'RG3_S2_LU_nom')
function2.build(RG1G2S2nom,  LUM_S2_t, erorG1G2S2_nom, ERRS2, [1,2,3], 0.95, 3,'cos_Tetta', 'RG1G2_S2_LU_nom')
function2.build(RG2G3S2nom,  LUM_S2, erorG2G3S2_nom, ERRS2, [1,2,3], 0.95, 3, 'cos_Tetta', 'RG2G3_S2_LU_nom')
function2.build(RG1G2G3S2nom,  LUM_S2, erorG1G2G3S2_nom, ERRS2, [1,2,3], 0.95, 3, 'cos_Tetta', 'RG1G2G3_S2_LU_nom')
function2.print_chi('G1', 'G3')



function2.build(RG1S1nom, HRG1G2S1nom_t, erorG1S1_nom, ERRS1, [1,2,3], 0.95, 3, 'cos_Tetta', 'RG1_S1_HR_nom')
function2.build(RG2S1nom, HRG1G2S1nom, erorG2S1_nom, ERRS1, [1,2,3], 0.95, 3,'cos_Tetta', 'RG2_S1_HR_nom')
function2.build(RG3S1nom, HRG1G2S1nom, erorG3S1_nom, ERRS1, [1,2,3], 0.95,3, 'cos_Tetta', 'RG3_S1_HR_nom')
function2.build(RG1G2S1nom, HRG1G2S1nom_t, erorG1G2S1_nom, ERRS1, [1,2,3], 0.95, 3,'cos_Tetta', 'RG1G2_S1_HR_nom')
function2.build(RG2G3S1nom, HRG1G2S1nom, erorG2G3S1_nom, ERRS1, [1,2,3], 0.95,3, 'cos_Tetta', 'RG2G3_S1_HR_nom')
function2.build(RG1G2G3S1nom, HRG1G2S1nom, erorG1G2G3S1_nom, ERRS1, [1,2,3], 0.95, 3,'cos_Tetta', 'RG1G2G3_S1_HR_nom')




function2.build(RG1S2nom, HRG1G2S2nom_t, erorG1S2_nom, ERRS2, [1,2,3], 0.95, 3, 'cos_Tetta', 'RG1_S2_HR_nom')
function2.build(RG2S2nom, HRG1G2S2nom, erorG2S2_nom, ERRS2, [1,2,3], 0.95, 3, 'cos_Tetta', 'RG2_S2_HR_nom')
function2.build(RG3S2nom, HRG1G2S2nom, erorG3S2_nom, ERRS2, [1,2,3], 0.95, 3, 'cos_Tetta', 'RG3_S2_HR_nom')
function2.build(RG1G2S2nom, HRG1G2S2nom_t, erorG1G2S2_nom, ERRS2, [1,2,3], 0.95, 3,'cos_Tetta', 'RG1G2_S2_HR_nom')
function2.build(RG2G3S2nom, HRG1G2S2nom, erorG2G3S2_nom, ERRS2, [1,2,3], 0.95, 3, 'cos_Tetta', 'RG2G3_S2_HR_nom')
function2.build(RG1G2G3S2nom, HRG1G2S2nom, erorG1G2G3S2_nom, ERRS2, [1,2,3], 0.95, 3, 'cos_Tetta', 'RG1G2G3_S2_HR_nom')
function2.print_chi('G1', 'G3')

function2.build(RG1S1, HRG1G2S1_t, erorG1S1_, ERRS1, [1,2,3], 0.95, 3, 'cos_Tetta', 'RG1_S1_HR')
function2.build(RG2S1, HRG1G2S1, erorG2S1_, ERRS1, [1,2,3], 0.95, 3, 'cos_Tetta', 'RG2_S1_HR')
function2.build(RG3S1, HRG1G2S1, erorG3S1_, ERRS1, [1,2,3], 0.95, 3,'cos_Tetta', 'RG3_S1_HR')
function2.build(RG1G2S1, HRG1G2S1_t, erorG1G2S1_, ERRS1, [1,2,3], 0.95, 3, 'cos_Tetta', 'RG1G2_S1_HR')
function2.build(RG2G3S1, HRG1G2S1, erorG2G3S1_, ERRS1, [1,2,3], 0.95, 3, 'cos_Tetta', 'RG2G3_S1_HR')
function2.build(RG1G2G3S1, HRG1G2S1, erorG1G2G3S1_, ERRS1, [1,2,3], 0.95, 3, 'cos_Tetta', 'RG1G2G3_S1_HR')


function2.build(RG1S2, HRG1G2S2_t, erorG1S2_, ERRS2, [1,2,3], 0.95, 3, 'cos_Tetta', 'RG1_S2_HR')
function2.build(RG2S2, HRG1G2S2, erorG2S2_, ERRS2, [1,2,3], 0.95, 3, 'cos_Tetta', 'RG2_S2_HR')
function2.build(RG3S2, HRG1G2S2, erorG3S2_, ERRS2, [1,2,3], 0.95, 3, 'cos_Tetta', 'RG3_S2_HR')
function2.build(RG1G2S2, HRG1G2S2_t, erorG1G2S2_, ERRS2, [1,2,3], 0.95, 3, 'cos_Tetta', 'RG1G2_S2_HR')
function2.build(RG2G3S2, HRG1G2S2, erorG2G3S2_, ERRS2, [1,2,3], 0.95, 3, 'cos_Tetta', 'RG2G3_S2_HR')
function2.build(RG1G2G3S2, HRG1G2S2, erorG1G2G3S2_, ERRS2, [1,2,3], 0.95, 3, 'cos_Tetta', 'RG1G2G3_S2_HR')
function2.print_chi('G1', 'G3')






function2.build(RG1S1, LUM_S1_t, erorG1S1_, ERRS1, [1,2,3],  0.95, 3, 'cos_Tetta', 'RG1_S1_LU')
function2.build(RG2S1, LUM_S1, erorG2S1_, ERRS1, [1,2,3],  0.95, 3, 'cos_Tetta', 'RG2_S1_LU')
function2.build(RG3S1, LUM_S1, erorG3S1_, ERRS1, [1,2,3],  0.95, 3, 'cos_Tetta', 'RG3_S1_LU')
function2.build(RG1G2S1, LUM_S1_t, erorG1G2S1_, ERRS1, [1,2,3],  0.95, 3, 'cos_Tetta', 'RG1G2_S1_LU')
function2.build(RG2G3S1, LUM_S1, erorG2G3S1_, ERRS1, [1,2,3],  0.95, 3, 'cos_Tetta', 'RG2G3_S1_LU')
function2.build(RG1G2G3S1, LUM_S1, erorG1G2G3S1_, ERRS1, [1,2,3],  0.95, 3, 'cos_Tetta', 'RG1G2G3_S1_LU')







function2.build(RG1S2, LUM_S2_t, erorG1S2_, ERRS2, [1,2,3],  0.95, 3, 'cos_Tetta', 'RG1_S2_LU')
function2.build(RG2S2, LUM_S2, erorG2S2_, ERRS2, [1,2,3],  0.95, 3, 'cos_Tetta', 'RG2_S2_LU')
function2.build(RG3S2, LUM_S2, erorG3S2_, ERRS2, [1,2,3],  0.95, 3, 'cos_Tetta', 'RG3_S2_LU')
function2.build(RG1G2S2, LUM_S2_t, erorG1G2S2_, ERRS2, [1,2,3],  0.95, 3, 'cos_Tetta', 'RG1G2_S2_LU')
function2.build(RG2G3S2, LUM_S2, erorG2G3S2_, ERRS2, [1,2,3],  0.95, 3, 'cos_Tetta', 'RG2G3_S2_LU')
function2.build(RG1G2G3S2, LUM_S2, erorG1G2G3S2_, ERRS2, [1,2,3],  0.95, 3, 'cos_Tetta', 'RG1G2G3_S2_LU')
function2.print_chi('G1', 'G3')






function2.graf(RG1S1, erorG1S1_, ERRS1, [1],  0.95,  'cos_Tetta', 'RG1_S1', A = 0, B = 0.55)
function2.graf(RG2S1, erorG2S1_, ERRS1, [1],  0.95,  'cos_Tetta', 'RG2_S1', A = 0, B = 0.55)
function2.graf(RG1G2S1, erorG1G2S1_, ERRS1, [1],  0.95,  'cos_Tetta', 'RG1G2_S1', A = 0, B = 0.55)
function2.graf(RG2G3S1, erorG2G3S1_, ERRS1, [1],  0.95,  'cos_Tetta', 'RG2G3_S1', A = 0, B = 0.55)
function2.graf(RG1G2G3S1, erorG1G2G3S1_, ERRS1, [1],  0.95,  'cos_Tetta', 'RG1G2G3_G1G2G3S1', A = 0, B = 0.55)


function2.graf(RG1S2, erorG1S2_, ERRS2, [1],  0.95,  'cos_Tetta', 'RG1_S2', A = 0, B = 0.55)
function2.graf(RG2S2, erorG2S2_, ERRS2, [1],  0.95,  'cos_Tetta', 'RG2_S2', A = 0, B = 0.55)
function2.graf(RG1G2S2, erorG1G2S2_, ERRS2, [1],  0.95,  'cos_Tetta', 'RG1G2_S2', A = 0, B = 0.55)
function2.graf(RG2G3S2, erorG2G3S2_, ERRS2, [1],  0.95,  'cos_Tetta', 'RG2G3_S2', A = 0, B = 0.55)
function2.graf(RG1G2G3S2, erorG1G2G3S2_, ERRS2, [1],  0.95,  'cos_Tetta', 'RG1G2G3_G1G2G3S2', A = 0, B = 0.55)
function2.print_chi('G3')

function2.graf(RG1S1nom, erorG1S1_nom, ERRS1, [1],  0.95,  'cos_Tetta', 'RG1_S1_nom', A = 0, B = 0.55)
function2.graf(RG2S1nom, erorG2S1_nom, ERRS1, [1],  0.95,  'cos_Tetta', 'RG2_S1_nom', A = 0, B = 0.55)
function2.graf(RG1G2S1nom, erorG1G2S1_nom, ERRS1, [1],  0.95,  'cos_Tetta', 'RG1G2_S1_nom', A = 0, B = 0.55)
function2.graf(RG2G3S1nom, erorG2G3S1_nom, ERRS1, [1],  0.95,  'cos_Tetta', 'RG2G3_S1_nom', A = 0, B = 0.55)
function2.graf(RG1G2G3S1nom, erorG1G2G3S1_nom, ERRS1, [1],  0.95,  'cos_Tetta', 'RG1G2G3_S1_nom', A = 0, B = 0.55)


function2.graf(RG1S2nom, erorG1S2_nom, ERRS2, [1],  0.95,  'cos_Tetta', 'RG1_S2_nom', A = 0, B = 0.55)
function2.graf(RG2S2nom, erorG2S2_nom, ERRS2, [1],  0.95,  'cos_Tetta', 'RG2_S2_nom', A = 0, B = 0.55)
function2.graf(RG1G2S2nom, erorG1G2S2_nom, ERRS2, [1],  0.95,  'cos_Tetta', 'RG1G2_S2_nom', A = 0, B = 0.55)
function2.graf(RG2G3S2nom, erorG2G3S2_nom, ERRS2, [1],  0.95,  'cos_Tetta', 'RG2G3_S2_nom', A = 0, B = 0.55)
function2.graf(RG1G2G3S2nom, erorG1G2G3S2_nom, ERRS2, [1],  0.95,  'cos_Tetta', 'RG1G2G3_G1G2G3S2_nom', A = 0, B = 0.55)
function2.print_chi()
























"""



"""


#function2.graf(RG3S1, erorG3S1_, ERRS1, [1],  0.95,  'cos_Tetta', 'RG3_S1')



function2.graf(RG1S1, erorG1S1_, ERRS1, [1],  0.95,  'cos_Tetta', 'RG1_S1')
function2.graf(RG2S1, erorG2S1_, ERRS1, [1],  0.95,  'cos_Tetta', 'RG2_S1')
function2.graf(RG1G2S1, erorG1G2S1_, ERRS1, [1],  0.95,  'cos_Tetta', 'RG1G2_S1')
function2.graf(RG2G3S1, erorG2G3S1_, ERRS1, [1],  0.95,  'cos_Tetta', 'RG2G3_S1')
function2.graf(RG1G2G3S1, erorG1G2G3S1_, ERRS1, [1],  0.95,  'cos_Tetta', 'RG1G2G3_G1G2G3S1')


function2.graf(RG1S2, erorG1S2_, ERRS2, [1],  0.95,  'cos_Tetta', 'RG1_S2')
function2.graf(RG2S2, erorG2S2_, ERRS2, [1],  0.95,  'cos_Tetta', 'RG2_S2')
function2.graf(RG1G2S2, erorG1G2S2_, ERRS2, [1],  0.95,  'cos_Tetta', 'RG1G2_S2')
function2.graf(RG2G3S2, erorG2G3S2_, ERRS2, [1],  0.95,  'cos_Tetta', 'RG2G3_S2')
function2.graf(RG1G2G3S2, erorG1G2G3S2_, ERRS2, [1],  0.95,  'cos_Tetta', 'RG1G2G3_G1G2G3S2')






#del RG1S1[cos_TettaS1[1205]],  RG1S1[cos_TettaS1[1428]], RG1S1[cos_TettaS1[4122]], RG1S1[cos_TettaS1[3757]], RG1S1[cos_TettaS1[4504]]
#del RG1G2S1[cos_TettaS1[1205]],  RG1G2S1[cos_TettaS1[1428]], RG1G2S1[cos_TettaS1[4122]], RG1G2S1[cos_TettaS1[3757]], RG1G2S1[cos_TettaS1[4504]]
#del RG1S2[cos_TettaS2[4740]], RG1S2[cos_TettaS2[2982]], RG1S2[cos_TettaS2[2935]], RG1S2[cos_TettaS2[3357]]
#del RG1G2S2[cos_TettaS2[4740]], RG1G2S2[cos_TettaS2[2982]], RG1G2S2[cos_TettaS2[2935]], RG1G2S2[cos_TettaS2[3357]]

#del HRG1G2S1_t[hr1[cos_TettaS1[1205]]], HRG1G2S1_t[hr1[cos_TettaS1[1428]]], HRG1G2S1_t[hr1[cos_TettaS1[4122]]], HRG1G2S1_t[hr1[cos_TettaS1[3757]]], HRG1G2S1_t[hr1[cos_TettaS1[4504]]]
#del HRG1G2S2_t[hr2[cos_TettaS2[4740]]], HRG1G2S2_t[hr2[cos_TettaS2[2982]]], HRG1G2S2_t[hr2[cos_TettaS2[2935]]], HRG1G2S2_t[hr2[cos_TettaS2[3357]]]


"""


"""




function2.build(RG1S1, HRG1G2S1, erorG1S1_, ERRS1, [1,2,3], 0.95, 3, 'cos_Tetta', 'RG1_S1_HR')
function2.build(RG2S1, HRG1G2S1, erorG2S1_, ERRS1, [1,2,3], 0.95, 3, 'cos_Tetta', 'RG2_S1_HR')
function2.build(RG3S1, HRG1G2S1, erorG3S1_, ERRS1, [1,2,3], 0.95, 3,'cos_Tetta', 'RG3_S1_HR')
function2.build(RG1G2S1, HRG1G2S1, erorG1G2S1_, ERRS1, [1,2,3], 0.95, 3, 'cos_Tetta', 'RG1G2_S1_HR')
function2.build(RG2G3S1, HRG1G2S1, erorG2G3S1_, ERRS1, [1,2,3], 0.95, 3, 'cos_Tetta', 'RG2G3_S1_HR')
function2.build(RG1G2G3S1, HRG1G2S1, erorG1G2G3S1_, ERRS1, [1,2,3], 0.95, 3, 'cos_Tetta', 'RG1G2G3_S1_HR')


function2.build(RG1S2, HRG1G2S2, erorG1S2_, ERRS2, [1,2,3], 0.95, 3, 'cos_Tetta', 'RG1_S2_HR')
function2.build(RG2S2, HRG1G2S2, erorG2S2_, ERRS2, [1,2,3], 0.95, 3, 'cos_Tetta', 'RG2_S2_HR')
function2.build(RG3S2, HRG1G2S2, erorG3S2_, ERRS2, [1,2,3], 0.95, 3, 'cos_Tetta', 'RG3_S2_HR')
function2.build(RG1G2S2, HRG1G2S2, erorG1G2S2_, ERRS2, [1,2,3], 0.95, 3, 'cos_Tetta', 'RG1G2_S2_HR')
function2.build(RG2G3S2, HRG1G2S2, erorG2G3S2_, ERRS2, [1,2,3], 0.95, 3, 'cos_Tetta', 'RG2G3_S2_HR')
function2.build(RG1G2G3S2, HRG1G2S2, erorG1G2G3S2_, ERRS2, [1,2,3], 0.95, 3, 'cos_Tetta', 'RG1G2G3_S2_HR')

function2.graf(RG1S1nom, erorG1S1_nom, ERRS1, [1],  0.95,  'cos_Tetta', 'RG1_S1_nom')
function2.graf(RG2S1nom, erorG2S1_nom, ERRS1, [1],  0.95,  'cos_Tetta', 'RG2_S1_nom')
function2.graf(RG1G2S1nom, erorG1G2S1_nom, ERRS1, [1],  0.95,  'cos_Tetta', 'RG1G2_S1_nom')
function2.graf(RG2G3S1nom, erorG2G3S1_nom, ERRS1, [1],  0.95,  'cos_Tetta', 'RG2G3_S1_nom')
function2.graf(RG1G2G3S1nom, erorG1G2G3S1_nom, ERRS1, [1],  0.95,  'cos_Tetta', 'RG1G2G3_S1_nom')


function2.graf(RG1S2nom, erorG1S2_nom, ERRS2, [1],  0.95,  'cos_Tetta', 'RG1_S2_nom')
function2.graf(RG2S2nom, erorG2S2_nom, ERRS2, [1],  0.95,  'cos_Tetta', 'RG2_S2_nom')
function2.graf(RG1G2S2nom, erorG1G2S2_nom, ERRS2, [1],  0.95,  'cos_Tetta', 'RG1G2_S2_nom')
function2.graf(RG2G3S2nom, erorG2G3S2_nom, ERRS2, [1],  0.95,  'cos_Tetta', 'RG2G3_S2_nom')
function2.graf(RG1G2G3S2nom, erorG1G2G3S2_nom, ERRS2, [1],  0.95,  'cos_Tetta', 'RG1G2G3_G1G2G3S2_nom')


function2.graf(RG1S1, erorG1S1_, ERRS1, [1],  0.95,  'cos_Tetta', 'RG1_S1')
function2.graf(RG2S1, erorG2S1_, ERRS1, [1],  0.95,  'cos_Tetta', 'RG2_S1')
function2.graf(RG1G2S1, erorG1G2S1_, ERRS1, [1],  0.95,  'cos_Tetta', 'RG1G2_S1')
function2.graf(RG2G3S1, erorG2G3S1_, ERRS1, [1],  0.95,  'cos_Tetta', 'RG2G3_S1')
function2.graf(RG1G2G3S1, erorG1G2G3S1_, ERRS1, [1],  0.95,  'cos_Tetta', 'RG1G2G3_S1')


function2.graf(RG1S2, erorG1S2_, ERRS2, [1],  0.95,  'cos_Tetta', 'RG1_S2')
function2.graf(RG2S2, erorG2S2_, ERRS2, [1],  0.95,  'cos_Tetta', 'RG2_S2')
function2.graf(RG1G2S2, erorG1G2S2_, ERRS2, [1],  0.95,  'cos_Tetta', 'RG1G2_S2')
function2.graf(RG2G3S2, erorG2G3S2_, ERRS2, [1],  0.95,  'cos_Tetta', 'RG2G3_S2')
function2.graf(RG1G2G3S2, erorG1G2G3S2_, ERRS2, [1],  0.95,  'cos_Tetta', 'RG1G2G3_G1G2G3S2')



function2.graf(RG1S1, erorG1S1_, ERRS1, [1],  0.95,  'cos_Tetta', '60-90_G1S1', 0,0.55)
function2.graf(RG2S1, erorG2S1_, ERRS1, [1],  0.95,  'cos_Tetta', '60-90_G2S1',0,0.55)
function2.graf(RG1G2S1, erorG1G2S1_, ERRS1, [1],  0.95,  'cos_Tetta', '60-90_G1G2S1',0,0.55)
function2.graf(RG2G3S1, erorG2G3S1_, ERRS1, [1],  0.95,  'cos_Tetta', '60-90_G2G3S1',0,0.55)
function2.graf(RG1G2G3S1, erorG1G2G3S1_, ERRS1, [1],  0.95,  'cos_Tetta', '60-90_G1G2G3S1',0,0.55)


function2.graf(RG1S1, erorG1S1_, ERRS1, [1],  0.95,  'cos_Tetta', '60-90_G1S1', 0,0.55)
function2.graf(RG2S1, erorG2S1_, ERRS1, [1],  0.95,  'cos_Tetta', '60-90_G2S1',0,0.55)
function2.graf(RG1G2S1, erorG1G2S1_, ERRS1, [1],  0.95,  'cos_Tetta', '60-90_G1G2S1',0,0.55)
function2.graf(RG2G3S1, erorG2G3S1_, ERRS1, [1],  0.95,  'cos_Tetta', '60-90_G2G3S1',0,0.55)
function2.graf(RG1G2G3S1, erorG1G2G3S1_, ERRS1, [1],  0.95,  'cos_Tetta', '60-90_G1G2G3S1',0,0.55)







function2.build(RG2S1, HRG1G2S1, erorG2S1_, ERRS1, [1,2,3], 0.95, 3, 'cos_Tetta', 'RG2_S1_HR')
function2.build(RG1G2S1, HRG1G2S1, erorG1G2S1_, ERRS1, [1,2,3], 0.95, 3, 'cos_Tetta', 'RG1G2_S1_HR')
function2.build(RG2G3S1, HRG1G2S1, erorG2G3S1_, ERRS1, [1,2,3], 0.95, 3, 'cos_Tetta', 'RG2G3_S1_HR')


function2.graf(RG2G3S2, erorG2G3S2_, ERRS2, [1],  0.95,  'cos_Tetta', 'RG2G3_S2_test_ID', -0.3, 1, 1)
function2.graf(RG2G3S1, erorG2G3S1_, ERRS1, [1],  0.95,  'cos_Tetta', 'RG2G3_S1_test_ID', -0.3, 1, 1)



function2.build(RG1S1, HRG1G2S1, erorG1S1_, ERRS1, [1,2,3], 0.95, 3, 'cos_Tetta', 'RG1_S1_HR')

function2.graf(RG1S1nom, erorG1S1_nom, ERRS1, [1],  0.95,  'cos_Tetta', 'RG1_S1_LU')
function2.graf(RG2S1nom,  erorG2S1_nom, ERRS1, [1],  0.95,  'cos_Tetta', 'RG2_S1_LU')
function2.graf(RG3S1nom,  erorG3S1_nom, ERRS1, [1],  0.95,  'cos_Tetta', 'RG3_S1_LU')
function2.graf(RG1G2S1nom,  erorG1G2S1_nom, ERRS1, [1],  0.95,  'cos_Tetta', 'RG1G2_S1_LU')
function2.graf(RG2G3S1nom,  erorG2G3S1_nom, ERRS1, [1],  0.95,  'cos_Tetta', 'RG2G3_S1_LU')
function2.graf(RG1G2G3S1nom,  erorG1G2G3S1_nom, ERRS1, [1],  0.95,  'cos_Tetta', 'RG1G2G3_S1_LU')


function2.graf(RG2S1, erorG2S1_, ERRS1, [1],  0.95,  'cos_Tetta', 'RG2_test')
function2.graf(RG2S2, erorG2S2_, ERRS2, [1],  0.95,  'cos_Tetta', 'RG2_test')

function2.graf(RG2G3S1, erorG2G3S1_, ERRS1, [1],  0.95,  'cos_Tetta', 'RG2G3_S1_test')
function2.graf(RG2G3S2, erorG2G3S2_, ERRS2, [1],  0.95,  'cos_Tetta', 'RG2G3_S2_test')




function2.graf(RG1S2nom,  erorG1S2_nom, ERRS2, [1],  0.95,  'cos_Tetta', 'RG1_S2_LU')
function2.graf(RG2S2nom,  erorG2S2_nom, ERRS2, [1],  0.95, 'cos_Tetta', 'RG2_S2_LU')
function2.graf(RG3S2nom,  erorG3S2_nom, ERRS2, [1],  0.95,  'cos_Tetta', 'RG3_S2_LU')
function2.graf(RG1G2S2nom,  erorG1G2S2_nom, ERRS2, [1],  0.95, 'cos_Tetta', 'RG1G2_S2_LU')
function2.graf(RG2G3S2nom,  erorG2G3S2_nom, ERRS2, [1],  0.95,  'cos_Tetta', 'RG2G3_S2_LU')
function2.graf(RG1G2G3S2nom,  erorG1G2G3S2_nom, ERRS2, [1],  0.95, 'cos_Tetta', 'RG1G2G3_S2_LU')
function2.print_chi()

function2.build(RG1S1, HRG1G2S1, erorG1S1_, ERRS1, [1,2,3], 0.95, 3, 'cos_Tetta', 'RG1_S1_HR')
function2.build(RG2S1, HRG1G2S1, erorG2S1_, ERRS1, [1,2,3], 0.95, 3, 'cos_Tetta', 'RG2_S1_HR')
function2.build(RG3S1, HRG1G2S1, erorG3S1_, ERRS1, [1,2,3], 0.95, 3,'cos_Tetta', 'RG3_S1_HR')
function2.build(RG1G2S1, HRG1G2S1, erorG1G2S1_, ERRS1, [1,2,3], 0.95, 3, 'cos_Tetta', 'RG1G2_S1_HR')
function2.build(RG2G3S1, HRG1G2S1, erorG2G3S1_, ERRS1, [1,2,3], 0.95, 3, 'cos_Tetta', 'RG2G3_S1_HR')
function2.build(RG1G2G3S1, HRG1G2S1, erorG1G2G3S1_, ERRS1, [1,2,3], 0.95, 3, 'cos_Tetta', 'RG1G2G3_S1_HR')


function2.build(RG1S2, HRG1G2S2, erorG1S2_, ERRS2, [1,2,3], 0.95, 3, 'cos_Tetta', 'RG1_S2_HR')
function2.build(RG2S2, HRG1G2S2, erorG2S2_, ERRS2, [1,2,3], 0.95, 3, 'cos_Tetta', 'RG2_S2_HR')
function2.build(RG3S2, HRG1G2S2, erorG3S2_, ERRS2, [1,2,3], 0.95, 3, 'cos_Tetta', 'RG3_S2_HR')
function2.build(RG1G2S2, HRG1G2S2, erorG1G2S2_, ERRS2, [1,2,3], 0.95, 3, 'cos_Tetta', 'RG1G2_S2_HR')
function2.build(RG2G3S2, HRG1G2S2, erorG2G3S2_, ERRS2, [1,2,3], 0.95, 3, 'cos_Tetta', 'RG2G3_S2_HR')
function2.build(RG1G2G3S2, HRG1G2S2, erorG1G2G3S2_, ERRS2, [1,2,3], 0.95, 3, 'cos_Tetta', 'RG1G2G3_S2_HR')
function2.print_chi()




function2.build(RG1S1nom, HRG1G2S1nom, erorG1S1_nom, ERRS1, [1,2,3], 0.95, 3, 'cos_Tetta', 'RG1_S1_HR_nom')
function2.build(RG2S1nom, HRG1G2S1nom, erorG2S1_nom, ERRS1, [1,2,3], 0.95, 3,'cos_Tetta', 'RG2_S1_HR_nom')
function2.build(RG3S1nom, HRG1G2S1nom, erorG3S1_nom, ERRS1, [1,2,3], 0.95,3, 'cos_Tetta', 'RG3_S1_HR_nom')
function2.build(RG1G2S1nom, HRG1G2S1nom, erorG1G2S1_nom, ERRS1, [1,2,3], 0.95, 3,'cos_Tetta', 'RG1G2_S1_HR_nom')
function2.build(RG2G3S1nom, HRG1G2S1nom, erorG2G3S1_nom, ERRS1, [1,2,3], 0.95,3, 'cos_Tetta', 'RG2G3_S1_HR_nom')
function2.build(RG1G2G3S1nom, HRG1G2S1nom, erorG1G2G3S1_nom, ERRS1, [1,2,3], 0.95, 3,'cos_Tetta', 'RG1G2G3_S1_HR_nom')




function2.build(RG1S2nom, HRG1G2S2nom, erorG1S2_nom, ERRS2, [1,2,3], 0.95, 3, 'cos_Tetta', 'RG1_S2_HR_nom')
function2.build(RG2S2nom, HRG1G2S2nom, erorG2S2_nom, ERRS2, [1,2,3], 0.95, 3, 'cos_Tetta', 'RG2_S2_HR_nom')
function2.build(RG3S2nom, HRG1G2S2nom, erorG3S2_nom, ERRS2, [1,2,3], 0.95, 3, 'cos_Tetta', 'RG3_S2_HR_nom')
function2.build(RG1G2S2nom, HRG1G2S2nom, erorG1G2S2_nom, ERRS2, [1,2,3], 0.95, 3,'cos_Tetta', 'RG1G2_S2_HR_nom')
function2.build(RG2G3S2nom, HRG1G2S2nom, erorG2G3S2_nom, ERRS2, [1,2,3], 0.95, 3, 'cos_Tetta', 'RG2G3_S2_HR_nom')
function2.build(RG1G2G3S2nom, HRG1G2S2nom, erorG1G2G3S2_nom, ERRS2, [1,2,3], 0.95, 3, 'cos_Tetta', 'RG1G2G3_S2_HR_nom')
function2.print_chi('G1')


function2.build(RG1S1, LUM_S1, erorG1S1_, ERRS1, [1,2,3,4],  0.95, 4, 'cos_Tetta', 'RG1_S1_LU')
function2.build(RG2S1, LUM_S1, erorG2S1_, ERRS1, [1,2,3,4],  0.95, 4, 'cos_Tetta', 'RG2_S1_LU')
function2.build(RG3S1, LUM_S1, erorG3S1_, ERRS1, [1,2,3,4],  0.95, 4, 'cos_Tetta', 'RG3_S1_LU')
function2.build(RG1G2S1, LUM_S1, erorG1G2S1_, ERRS1, [1,2,3,4],  0.95, 4, 'cos_Tetta', 'RG1G2_S1_LU')
function2.build(RG2G3S1, LUM_S1, erorG2G3S1_, ERRS1, [1,2,3,4],  0.95, 4, 'cos_Tetta', 'RG2G3_S1_LU')
function2.build(RG1G2G3S1, LUM_S1, erorG1G2G3S1_, ERRS1, [1,2,3,4],  0.95, 4, 'cos_Tetta', 'RG1G2G3_S1_LU')







function2.build(RG1S2, LUM_S2, erorG1S2_, ERRS2, [1,2,3,4],  0.95, 4, 'cos_Tetta', 'RG1_S2_LU')
function2.build(RG2S2, LUM_S2, erorG2S2_, ERRS2, [1,2,3,4],  0.95, 4, 'cos_Tetta', 'RG2_S2_LU')
function2.build(RG3S2, LUM_S2, erorG3S2_, ERRS2, [1,2,3,4],  0.95, 4, 'cos_Tetta', 'RG3_S2_LU')
function2.build(RG1G2S2, LUM_S2, erorG1G2S2_, ERRS2, [1,2,3,4],  0.95, 4, 'cos_Tetta', 'RG1G2_S2_LU')
function2.build(RG2G3S2, LUM_S2, erorG2G3S2_, ERRS2, [1,2,3,4],  0.95, 4, 'cos_Tetta', 'RG2G3_S2_LU')
function2.build(RG1G2G3S2, LUM_S2, erorG1G2G3S2_, ERRS2, [1,2,3,4],  0.95, 4, 'cos_Tetta', 'RG1G2G3_S2_LU')
function2.print_chi('G3')


function2.print_chi('G3')
function2.build(RG1S1, HRG1G2S1, erorG1S1_, ERRS1, [1,2,3], 0.95, 3, 'cos_Tetta', 'RG1_S1_HR')
function2.build(RG2S1, HRG1G2S1, erorG2S1_, ERRS1, [1,2,3], 0.95, 3, 'cos_Tetta', 'RG2_S1_HR')
function2.build(RG3S1, HRG1G2S1, erorG3S1_, ERRS1, [1,2,3], 0.95, 3,'cos_Tetta', 'RG3_S1_HR')
function2.build(RG1G2S1, HRG1G2S1, erorG1G2S1_, ERRS1, [1,2,3], 0.95, 3, 'cos_Tetta', 'RG1G2_S1_HR')
function2.build(RG2G3S1, HRG1G2S1, erorG2G3S1_, ERRS1, [1,2,3], 0.95, 3, 'cos_Tetta', 'RG2G3_S1_HR')
function2.build(RG1G2G3S1, HRG1G2S1, erorG1G2G3S1_, ERRS1, [1,2,3], 0.95, 3, 'cos_Tetta', 'RG1G2G3_S1_HR')


function2.build(RG1S2, HRG1G2S2, erorG1S2_, ERRS2, [1,2,3], 0.95, 3, 'cos_Tetta', 'RG1_S2_HR')
function2.build(RG2S2, HRG1G2S2, erorG2S2_, ERRS2, [1,2,3], 0.95, 3, 'cos_Tetta', 'RG2_S2_HR')
function2.build(RG3S2, HRG1G2S2, erorG3S2_, ERRS2, [1,2,3], 0.95, 3, 'cos_Tetta', 'RG3_S2_HR')
function2.build(RG1G2S2, HRG1G2S2, erorG1G2S2_, ERRS2, [1,2,3], 0.95, 3, 'cos_Tetta', 'RG1G2_S2_HR')
function2.build(RG2G3S2, HRG1G2S2, erorG2G3S2_, ERRS2, [1,2,3], 0.95, 3, 'cos_Tetta', 'RG2G3_S2_HR')
function2.build(RG1G2G3S2, HRG1G2S2, erorG1G2G3S2_, ERRS2, [1,2,3], 0.95, 3, 'cos_Tetta', 'RG1G2G3_S2_HR')
function2.print_chi('G3')










function2.build(RG1S1, HRG1G2S1, erorG1S1_, ERRS1, [1,2,3], 0.95, 3, 'cos_Tetta', 'RG1_S1_HR')
function2.build(RG2S1, HRG1G2S1, erorG2S1_, ERRS1, [1,2,3], 0.95, 3, 'cos_Tetta', 'RG2_S1_HR')
function2.build(RG3S1, HRG1G2S1, erorG3S1_, ERRS1, [1,2,3], 0.95, 3,'cos_Tetta', 'RG3_S1_HR')
function2.build(RG1G2S1, HRG1G2S1, erorG1G2S1_, ERRS1, [1,2,3], 0.95, 3, 'cos_Tetta', 'RG1G2_S1_HR')
function2.build(RG2G3S1, HRG1G2S1, erorG2G3S1_, ERRS1, [1,2,3], 0.95, 3, 'cos_Tetta', 'RG2G3_S1_HR')
function2.build(RG1G2G3S1, HRG1G2S1, erorG1G2G3S1_, ERRS1, [1,2,3], 0.95, 3, 'cos_Tetta', 'RG1G2G3_S1_HR')


function2.build(RG1S2, HRG1G2S2, erorG1S2_, ERRS2, [1,2,3], 0.95, 3, 'cos_Tetta', 'RG1_S2_HR')
function2.build(RG2S2, HRG1G2S2, erorG2S2_, ERRS2, [1,2,3], 0.95, 3, 'cos_Tetta', 'RG2_S2_HR')
function2.build(RG3S2, HRG1G2S2, erorG3S2_, ERRS2, [1,2,3], 0.95, 3, 'cos_Tetta', 'RG3_S2_HR')
function2.build(RG1G2S2, HRG1G2S2, erorG1G2S2_, ERRS2, [1,2,3], 0.95, 3, 'cos_Tetta', 'RG1G2_S2_HR')
function2.build(RG2G3S2, HRG1G2S2, erorG2G3S2_, ERRS2, [1,2,3], 0.95, 3, 'cos_Tetta', 'RG2G3_S2_HR')
function2.build(RG1G2G3S2, HRG1G2S2, erorG1G2G3S2_, ERRS2, [1,2,3], 0.95, 3, 'cos_Tetta', 'RG1G2G3_S2_HR')

function2.print_chi('G3')



print( sort(list(LUM_S1.keys()))[int(len(list(LUM_S1.keys()))/4)] )
print( sort(list(LUM_S2.keys()))[int(len(list(LUM_S2.keys()))/4)] )
print(len(RG1S1), len(RG1S2))

"""


"""



function2.build(RG1S1, LUM_S1, erorG1S1_, ERRS1, [1,2,3,4],  0.95, 4, 'cos_Tetta', 'RG1_S1_LU')
function2.build(RG2S1, LUM_S1, erorG2S1_, ERRS1, [1,2,3,4],  0.95, 4, 'cos_Tetta', 'RG2_S1_LU')
function2.build(RG3S1, LUM_S1, erorG3S1_, ERRS1, [1,2,3,4],  0.95, 4, 'cos_Tetta', 'RG3_S1_LU')
function2.build(RG1G2S1, LUM_S1, erorG1G2S1_, ERRS1, [1,2,3,4],  0.95, 4, 'cos_Tetta', 'RG1G2_S1_LU')
function2.build(RG2G3S1, LUM_S1, erorG2G3S1_, ERRS1, [1,2,3,4],  0.95, 4, 'cos_Tetta', 'RG2G3_S1_LU')
function2.build(RG1G2G3S1, LUM_S1, erorG1G2G3S1_, ERRS1, [1,2,3,4],  0.95, 4, 'cos_Tetta', 'RG1G2G3_S1_LU')







function2.build(RG1S2, LUM_S2, erorG1S2_, ERRS2, [1,2,3,4],  0.95, 4, 'cos_Tetta', 'RG1_S2_LU')
function2.build(RG2S2, LUM_S2, erorG2S2_, ERRS2, [1,2,3,4],  0.95, 4, 'cos_Tetta', 'RG2_S2_LU')
function2.build(RG3S2, LUM_S2, erorG3S2_, ERRS2, [1,2,3,4],  0.95, 4, 'cos_Tetta', 'RG3_S2_LU')
function2.build(RG1G2S2, LUM_S2, erorG1G2S2_, ERRS2, [1,2,3,4],  0.95, 4, 'cos_Tetta', 'RG1G2_S2_LU')
function2.build(RG2G3S2, LUM_S2, erorG2G3S2_, ERRS2, [1,2,3,4],  0.95, 4, 'cos_Tetta', 'RG2G3_S2_LU')
function2.build(RG1G2G3S2, LUM_S2, erorG1G2G3S2_, ERRS2, [1,2,3,4],  0.95, 4, 'cos_Tetta', 'RG1G2G3_S2_LU')
#function2.print_chi()











function2.build(RG1S1, HRG2G3S1, erorG1S1_, ERRS1, [1,2,3], 0.95, 3, 'cos_Tetta', 'RG1_S1_HR')
function2.build(RG2S1, HRG2G3S1, erorG2S1_, ERRS1, [1,2,3], 0.95, 3, 'cos_Tetta', 'RG2_S1_HR')
function2.build(RG3S1, HRG2G3S1, erorG3S1_, ERRS1, [1,2,3], 0.95, 3,'cos_Tetta', 'RG3_S1_HR')
function2.build(RG1G2S1, HRG2G3S1, erorG1G2S1_, ERRS1, [1,2,3], 0.95, 3, 'cos_Tetta', 'RG1G2_S1_HR')
function2.build(RG2G3S1, HRG2G3S1, erorG2G3S1_, ERRS1, [1,2,3], 0.95, 3, 'cos_Tetta', 'RG2G3_S1_HR')
function2.build(RG1G2G3S1, HRG2G3S1, erorG1G2G3S1_, ERRS1, [1,2,3], 0.95, 3, 'cos_Tetta', 'RG1G2G3_S1_HR')



function2.build(RG1S1nom, HRG2G3S1nom, erorG1S1_nom, ERRS1, [1,2,3], 0.95, 3, 'cos_Tetta', 'RG1_S1_HR_nom')
function2.build(RG2S1nom, HRG2G3S1nom, erorG2S1_nom, ERRS1, [1,2,3], 0.95, 3,'cos_Tetta', 'RG2_S1_HR_nom')
function2.build(RG3S1nom, HRG2G3S1nom, erorG3S1_nom, ERRS1, [1,2,3], 0.95,3, 'cos_Tetta', 'RG3_S1_HR_nom')
function2.build(RG1G2S1nom, HRG2G3S1nom, erorG1G2S1_nom, ERRS1, [1,2,3], 0.95, 3,'cos_Tetta', 'RG1G2_S1_HR_nom')
function2.build(RG2G3S1nom, HRG2G3S1nom, erorG2G3S1_nom, ERRS1, [1,2,3], 0.95,3, 'cos_Tetta', 'RG2G3_S1_HR_nom')



function2.build(RG1S2nom,  LUM_S2, erorG1S2_nom, ERRS2, [3,4], 0.95, 4, 'cos_Tetta', 'RG1_S2_LU_nom')
function2.build(RG2S2nom,  LUM_S2, erorG2S2_nom, ERRS2, [3,4], 0.95, 4, 'cos_Tetta', 'RG2_S2_LU_nom')
function2.build(RG3S2nom,  LUM_S2, erorG3S2_nom, ERRS2, [3,4], 0.95, 4, 'cos_Tetta', 'RG3_S2_LU_nom')
function2.build(RG1G2S2nom,  LUM_S2, erorG1G2S2_nom, ERRS2, [3,4], 0.95, 4,'cos_Tetta', 'RG1G2_S2_LU_nom')
function2.build(RG2G3S2nom,  LUM_S2, erorG2G3S2_nom, ERRS2, [3,4], 0.95, 4, 'cos_Tetta', 'RG2G3_S2_LU_nom')
function2.build(RG1G2G3S2nom,  LUM_S2, erorG1G2G3S2_nom, ERRS2, [3,4], 0.95, 4, 'cos_Tetta', 'RG1G2G3_S2_LU_nom')


"""
#function2.graf(RG1S1, erorG1S1_, ERRS1, [1], 0.95,  'cos_Tetta', 'RG1_S1_HRG1G2')
#function2.graf(RG2S1, erorG2S1_, ERRS1, [1], 0.95,  'cos_Tetta', 'RG2_S1_HRG1G2')










"""
function2.build(RG1S1nom, HRG1G2S1nom, erorG1S1_nom, ERRS1, [1,2,3], 0.95, 3, 'cos_Tetta', 'RG1_S1_HR_nom')
function2.build(RG2S1nom, HRG1G2S1nom, erorG2S1_nom, ERRS1, [1,2,3], 0.95, 3,'cos_Tetta', 'RG2_S1_HR_nom')
function2.build(RG3S1nom, HRG1G2S1nom, erorG3S1_nom, ERRS1, [1,2,3], 0.95,3, 'cos_Tetta', 'RG3_S1_HR_nom')
function2.build(RG1G2S1nom, HRG1G2S1nom, erorG1G2S1_nom, ERRS1, [1,2,3], 0.95, 3,'cos_Tetta', 'RG1G2_S1_HR_nom')
function2.build(RG2G3S1nom, HRG1G2S1nom, erorG2G3S1_nom, ERRS1, [1,2,3], 0.95,3, 'cos_Tetta', 'RG2G3_S1_HR_nom')
function2.build(RG1G2G3S1nom, HRG1G2S1nom, erorG1G2G3S1_nom, ERRS1, [1,2,3], 0.95, 3,'cos_Tetta', 'RG1G2G3_S1_HR_nom')




function2.build(RG1S2nom, HRG1G2S2nom, erorG1S2_nom, ERRS2, [1,2,3], 0.95, 3, 'cos_Tetta', 'RG1_S2_HR_nom')
function2.build(RG2S2nom, HRG1G2S2nom, erorG2S2_nom, ERRS2, [1,2,3], 0.95, 3, 'cos_Tetta', 'RG2_S2_HR_nom')
function2.build(RG3S2nom, HRG1G2S2nom, erorG3S2_nom, ERRS2, [1,2,3], 0.95, 3, 'cos_Tetta', 'RG3_S2_HR_nom')
function2.build(RG1G2S2nom, HRG1G2S2nom, erorG1G2S2_nom, ERRS2, [1,2,3], 0.95, 3,'cos_Tetta', 'RG1G2_S2_HR_nom')
function2.build(RG2G3S2nom, HRG1G2S2nom, erorG2G3S2_nom, ERRS2, [1,2,3], 0.95, 3, 'cos_Tetta', 'RG2G3_S2_HR_nom')
function2.build(RG1G2G3S2nom, HRG1G2S2nom, erorG1G2G3S2_nom, ERRS2, [1,2,3], 0.95, 3, 'cos_Tetta', 'RG1G2G3_S2_HR_nom')
function2.print_chi()







function2.graf(RG1S1nom, erorG1S1_nom, ERRS1, [1], 0.95, 'cos_Tetta', 'RG1S1_HRG1G2_nom')
function2.graf(RG2S1nom, erorG2S1_nom, ERRS1, [1], 0.95, 'cos_Tetta', 'RG2S1_HRG1G2_nom')

function2.graf(RG3S1nom, erorG3S1_nom, ERRS1, [1], 0.95, 'cos_Tetta', 'RG3S1_HRG1G2_nom')
"""
#function2.build(RG1S1, HRG1G2S1, erorG1S1_, ERRS1, [1, 2, 3], 0.95, 'cos_Tetta', 'RG1S1_HRG1G2')
#function2.graf(RG1S1nom, erorG1S1_2, ERRS1, [1], 0.95, 'cos_Tetta', 'RG1S1_HRG1G2_nom')
#function2.print_er()
"""

function2.build(RG1S1nom, HRG1G2S1nom, erorG1S1_nom, ERRS1, [1,2,3], 0.95, 'cos_Tetta', 'RG1S1_HRG1G2_nom')
function2.build(RG2S1nom, HRG1G2S1nom, erorG2S1_nom, ERRS1, [1,2,3], 0.95, 'cos_Tetta', 'RG2S1_HRG1G2_nom')

function2.build(RG3S1nom, HRG1G2S1nom, erorG3S1_nom, ERRS1, [1,2,3], 0.95, 'cos_Tetta', 'RG3S1_HRG1G2_nom')

function2.build(RG1S1, HRG1G2S1, erorG1S1_, ERRS1, [1,2,3], 0.95, 'cos_Tetta', 'RG1S1_HRG1G2_nom')

function2.build(RG2S1, HRG1G2S1, erorG2S1_, ERRS1, [1,2,3], 0.95, 'cos_Tetta', 'RG2S1_HRG1G2_nom')

function2.build(RG3S1, HRG1G2S1, erorG3S1_, ERRS1, [1,2,3], 0.95, 'cos_Tetta', 'RG3S1_HRG1G2_nom')




#print(sort(list(LUM_S1.keys())))
"""
"""


"""
#function2.graf(RG1S1, erorG1S1_, ERRS1, [1], 0.95, 'cos_Tetta', 'RG1S1_HRG1G2_')
#function2.graf(RG2S1, erorG2S1_, ERRS1, [1], 0.95, 'cos_Tetta', 'RG2S1_HRG1G2_')

#function2.graf(RG3S1, erorG3S1_, ERRS1, [1], 0.95, 'cos_Tetta', 'RG3S1_HRG1G2_')



"""





function2.build(RG1S1, HRG1G2S1, erorG1S1_, ERRS1, [3], 0.95, 'cos_Tetta', 'RG1S1_HRG1G2')

function2.build(RG3S1, HRG1G2S1, erorG3S1_, ERRS1, [1], 0.95, 'cos_Tetta', 'RG3S1_HRG1G2')
function2.build(RG1G2S1, HRG1G2S1, erorG1G2S1_, ERRS1, [2], 0.95, 'cos_Tetta', 'RG1G2S1_HRG1G2')


#function2.build(RG1G2S1, HRG1G2S1, erorG1G2S1_, ERRS1, [1,2,3], 0.95, 'cos_Tetta', 'RG1G2S1_HRG1G2')
#function2.build(RG2G3S1, HRG1G2S1, erorG2G3S1_, ERRS1, [1,2,3], 0.95, 'cos_Tetta', 'RG2G3S1_HRG1G2')

#function2.build(RG1G2S1nom, HRG1G2S1nom, erorG1G2S1_nom, ERRS1, [1,2,3], 0.95, 'cos_Tetta', 'RG1G2S1_HRG1G2')
#function2.build(RG2G3S1nom, HRG1G2S1nom, erorG2G3S1_nom, ERRS1, [1,2,3], 0.95, 'cos_Tetta', 'RG2G3S1_HRG1G2')


#function2.build(RG1S1, HRG1G2S1, erorG1S1_, ERRS1, [1,2,3], 0.95, 'cos_Tetta', 'RG1S1_HRG1G2')

#function2.graf([RG1S1], erorG1S1_, ERRS1, [1], 0.95, 'cos_Tetta', 'RG1S1_HRG1G2')






"""
"""

function2.build(RG1S2nom, LUM_S2, erorG1S2_nom, ERRS2, [1,2,3,4,5],  0.95, 5, 'cos_Tetta', 'RG1S2_HRG1G2')
function2.build(RG2S2nom, LUM_S2, erorG2S2_nom, ERRS2, [1,2,3,4,5],  0.95, 5, 'cos_Tetta', 'RG2S2_HRG1G2')

function2.build(RG3S2nom, LUM_S2, erorG3S2_nom, ERRS2, [1,2,3,4,5],  0.95, 5, 'cos_Tetta', 'RG3S2_HRG1G2')



#function2.build(RG1S1, LUM_S1, erorG1S1_, ERRS1, [1,2,3,4],  0.95, 4, 'cos_Tetta', 'RG1S1_HRG1G2')


"""


#function2.graf(RG1S2, erorG1S2_, ERRS2, [1], 0.95, 'cos_Tetta', 'RG1S1_HRG1G2')
#function2.graf(RG2S2, erorG2S2_, ERRS2, [1], 0.95, 'cos_Tetta', 'RG1S1_HRG1G2')
#function2.graf(RG1S1, erorG1S1_, ERRS1, [1], 0.95, 'cos_Tetta', 'RG1S1_HRG1G2')
#function2.graf(RG2S1, erorG2S1_, ERRS1, [1], 0.95, 'cos_Tetta', 'RG1S1_HRG1G2')
#function2.graf(RG3S1, erorG3S1_, ERRS1, [1], 0.95, 'cos_Tetta', 'RG1S1_HRG1G2')


#function2.graf(RG1S2, erorG1S2_, ERRS2, [1], 0.95, 'cos_Tetta', 'RG1S2_HRG1G2')
#function2.graf(RG2S2, erorG2S2_, ERRS2, [1], 0.95, 'cos_Tetta', 'RG1S2_HRG1G2')
#function2.graf(RG3S2, erorG3S2_, ERRS2, [1], 0.95, 'cos_Tetta', 'RG1S2_HRG1G2')
"""


"""



#function2.build(RG2S1nom, LUM_S1, erorG2S1_nom, ERRS1, [1, 2, 3],  0.95, 3, 'cos_Tetta', 'RG1S2_HRG1G2')



print(len(a))

"""



function2.build(RG2S2nom, HRG1G2S2nom, erorG2S2_nom, ERRS2, [1,2,3], 0.95, 3, 'cos_Tetta', 'RG2S2_HRG1G2')


function2.build(RG1G2S2nom, HRG1G2S2nom, erorG1G2S2_nom, ERRS2, [1,2,3], 0.95, 3,'cos_Tetta', 'RG1G2S2_HRG1G2')

"""


#function2.print_er()


#function2.build(RG1S2, LUM_S2, erorG1S2_, ERRS2, [1,2,3,4,5],  0.95, 5, 'cos_Tetta', 'RG1S2_HRG1G2')




"""
function2.build(RG1S2, LUM_S2, erorG1S2_, ERRS2, [1,2,3,4],  0.95, 4, 'cos_Tetta', 'RG1S2_LU')
function2.build(RG2S2, LUM_S2, erorG2S2_, ERRS2, [1,2,3,4],  0.95, 4, 'cos_Tetta', 'RG2S2_LU')

function2.build(RG3S2, LUM_S2, erorG3S2_, ERRS2, [1,2,3,4],  0.95, 4, 'cos_Tetta', 'RG3S2_LU')
function2.build(RG1G2S2, LUM_S2, erorG1G2S2_, ERRS2, [1,2,3,4],  0.95, 4, 'cos_Tetta', 'RG1G2S2_LU')
function2.build(RG2G3S2, LUM_S2, erorG2G3S2_, ERRS2, [1,2,3,4],  0.95, 4, 'cos_Tetta', 'RG2G3S2_LU')
function2.build(RG1G2G3S2, LUM_S2, erorG1G2G3S2_, ERRS2, [1,2,3,4],  0.95, 4, 'cos_Tetta', 'RG1G2G3S2_LU')


function2.build(RG1S2, LUM_S2, erorG1S2_, ERRS2, [1,2,3,4],  0.95, 4, 'cos_Tetta', 'RG1S2_LU')
function2.build(RG2S2, LUM_S2, erorG2S2_, ERRS2, [1],  0.95, 4, 'cos_Tetta', 'RG2S2_LU')
function2.build(RG2G3S2, LUM_S2, erorG2G3S2_, ERRS2, [1],  0.95, 4, 'cos_Tetta', 'RG2G3S2_LU')




function2.build(RG2S1, LUM_S1, erorG2S1_, ERRS1, [1,2,3,4],  0.95, 4, 'cos_Tetta', 'RG2S1_LU')

function2.build(RG3S1, LUM_S1, erorG3S1_, ERRS1, [1,2,3,4],  0.95, 4, 'cos_Tetta', 'RG3S1_LU')
function2.build(RG1G2S1, LUM_S1, erorG1G2S1_, ERRS1, [1,2,3,4],  0.95, 4, 'cos_Tetta', 'RG1G2S1_LU')
function2.build(RG2G3S1, LUM_S1, erorG2G3S1_, ERRS1, [1,2,3,4],  0.95, 4, 'cos_Tetta', 'RG2G3S1_LU')
function2.build(RG1G2G3S1, LUM_S1, erorG1G2G3S1_, ERRS1, [1,2,3,4],  0.95, 4, 'cos_Tetta', 'RG1G2G3S1_LU')
"""



#function2.build(RG1S1, LUM_S1, erorG1S1_, ERRS1, [1,2,3,4],  0.95, 4, 'cos_Tetta', 'RG1S1_LU')




TASK1.close()
TASK2.close()
TABL.close()