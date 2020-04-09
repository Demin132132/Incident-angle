'''
Description of the classes used to fit 3 channel spectrum 
'''
import numpy as np
from scipy.integrate import quad
from scipy.optimize import leastsq
 
class model:
    def __init__(self, model_name):
        if(model_name == 'Band'):
            self.n_par = 3
            self.func = self.Band_fix_beta 
            self.fit_par_init = np.array([1.0, -1, 20])
        elif(model_name == 'CPL'):
            self.n_par = 3
            self.fit_par_init = np.array([10.0, -1, 200])
            self.func = self.CPL
        elif(model_name == 'PL'):
            self.n_par = 2
            self.func = self.PL
            self.fit_par_init = np.array([100.0, -1.0])
        elif(model_name == 'Parabola'):
            self.n_par = 3
            self.func = self.poly2
            self.fit_par_init = np.array([10.0, 1.0, 10.0])
        else:
            raise 
         
        self.model_name = model_name
        self.Epiv = 100.0 # keV        
         
    def get_number_of_parameters(self):
        return self.n_par
     
    def CPL(self, x, p):
        return p[0]*np.power(x/self.Epiv, p[1])*np.exp(- x/p[2])
     
    def PL(self, x, p):
        return p[0]*np.power(x/self.Epiv, p[1])
     
    def poly2(self, x, p):
        return p[0]*x*x + p[1]*x + p[2]
     
    def Band_fix_beta(self, x, p):
        '''Band with beta = -2.5 '''
        par = [p[0], p[1], -2.5, p[2]]
        return self.Band(x, par)
     
    def Band(self, x , p):
        '''Band function 
        p[0] - amplitude
        p[1] - alpha
        p[2] - beta
        p[3] - Ep
        '''
        Eb = p[3] * (p[1] - p[2])/(p[1] + 2.0)
        if(x < Eb):
            return p[0] * np.power(x/self.Epiv, p[1]) * np.exp(- x/p[3] * (p[1]+2.0))
        else:
            return p[0] * np.power(x/self.Epiv, p[2]) * np.exp(p[2] - p[1]) * np.power(Eb / self.Epiv, p[1] - p[2])
     
    def int_func(self, p, E1, E2):
        result = np.zeros((3,), dtype = float)
        for i in range(0, E1.size):
            integr = quad(self.func, E1[i], E2[i], args=(p,))
            result[i] = integr[0]
#            result[i] =self.func((E1[i]+E2[i])/2.0, p)*(E2[i]-E1[i])           
        return result
     
    def residuals (self, p, x1, x2, y, y_err):
        #print x1, x2, y
        #print 'model:' , self.int_func(p, x1, x2) 
        #print 'chi2 = %9.4f' % ( sum(((self.int_func(p, x1, x2) - y) / y_err)**2),)
        k = 1
        if p[2] <1.0:
            k =10
        return (self.int_func(p, x1, x2) - y) / y_err  #* k
     
    def get_counts_in_channels(self, par, arr_cuts):
        low_cuts = arr_cuts.size - 1
        high_cuts = arr_cuts.size
        return self.int_func(par, arr_cuts[0:low_cuts], arr_cuts[1:high_cuts])
 
class Fitter:
    def __init__(self, model, cuts, counts, counts_err):
        self.arr_cuts = cuts     # array of 4 channel cuts
        self.arr_counts = counts # array of 3 number of counts
        self.arr_counts_err = counts_err # array of 3 errors of number of counts
        self.model = model       # the model object
         
        model_counts_init = model.int_func(model.fit_par_init, cuts[0:3], cuts[1:4])
        model.fit_par_init[0] = counts[1] / model_counts_init[1]
         
    def fit(self):
        low_cuts = self.arr_cuts.size - 1
        high_cuts = self.arr_cuts.size
        fit_par_result, covar_matrix, dict_out, mesg, n_iter = leastsq(self.model.residuals,\
                         self.model.fit_par_init, \
                         args=(self.arr_cuts[0:low_cuts], self.arr_cuts[1:high_cuts], self.arr_counts, self.arr_counts_err),\
                         full_output=1, maxfev = 1000)
 
#       print self.arr_cuts[0:low_cuts], self.arr_cuts[1:high_cuts], self.arr_counts, self.arr_counts_err
#       print mesg, n_iter
        chi2 =sum(((self.model.int_func(fit_par_result, self.arr_cuts[0:low_cuts], self.arr_cuts[1:high_cuts]) - self.arr_counts) / \
                   self.arr_counts_err)**2)
        return fit_par_result, chi2