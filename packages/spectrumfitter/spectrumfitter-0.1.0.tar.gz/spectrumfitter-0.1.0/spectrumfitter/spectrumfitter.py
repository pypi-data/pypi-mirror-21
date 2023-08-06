

''' Spectrum_fitter.py : an obect-oriented framework for fitting dielectric spectra. '''
from numpy import *
import matplotlib.pyplot as plt
from scipy import optimize 
from scipy import special as sp

class Lineshape:
    """Class that holds some things common to all Lineshapes""" 
    def __init__(self,params,bounds,name):
        self.p = params
        self.bounds = bounds
        self.name = name

class Debye(Lineshape):
    """Debye lineshape object.
    Note: the wD parameter is assumed to be in units of cm^-1
    """
    def __init__(self,params=[1,1],bounds=[(-float('inf'),+float('inf')),(-float('inf'),+float('inf'))],name="Debye"):
        Lineshape.__init__(self, params, bounds, name)
        self.pnames = ["f", "wD"]
        self.type = "Debye"
    
    def __call__(self, w):
        rp = self.p[0]*self.p[1]**2/(self.p[1]**2 + w**2)     
        cp = rp*w/self.p[1]
        return (rp, cp)
    
    def get_freq(self): 
        return self.p[1]
    
    def get_abs_freq(self):
        return self.p[1]
    
    def print_params(self):
        print(u"%20s f =%7.5f \u03C9 = %6.2f 1/cm (%5.2f ps)" % (self.name, self.p[0], self.p[1], 33.34/(2*3.14159*self.p[1])))
        
    def print_params_latex(self):
        print(u"%20s & %7.5f & %6.2f & %5.2f &   & \\\\" % (self.name, self.p[0], self.p[1], 33.333/(2*3.14159*self.p[1])))
       
       
class DHO(Lineshape):
    """Damped harmonic oscillator object"""
    def __init__(self,params=[1,1,1],bounds=[(-float('inf'),+float('inf')),(-float('inf'),+float('inf'))],name="DHO"):
        Lineshape.__init__(self, params, bounds, name)
        self.pnames = ["f", "w", "gamma"]
        self.type = "DHO"

    def __call__(self, w):
        denom = (self.p[1]**2 - w**2)**2 + w**2*self.p[2]**2
        rp = self.p[0]*(self.p[1]**2)*(self.p[1]**2 - w**2)/denom
        cp = self.p[0]*(self.p[1]**2)*self.p[2]*w/denom
        return (rp, cp)
    
    def get_freq(self):
        return self.p[1]
    
    def get_abs_freq(self):
        return sqrt( self.p[1]**2 + self.p[2]**2 ) 
    
    def print_params(self):
        print(u"%20s f =%7.5f \u03C9 = %6.2f + %6.2f i  (%6.3f ps)" % (self.name, self.p[0], self.p[1], self.p[2],  33.34/(2*3.141*self.p[1])))
        
    def print_params_latex(self):
        print(u"%20s & %7.5f &  %6.2f & %6.3f & %6.2f &  \\\\" % (self.name, self.p[0], self.p[1], 33.34/(2*3.141*self.p[1]), self.p[2] ))

    
class BrendelDHO(Lineshape):
    """"Brendel model for amorphous materials - Gaussian distribution of DHOs. Ref: J. Appl. Phys. 71, 1 (1992)"""
    def __init__(self,params=[1,1,1,1],bounds=[(0,+float('inf')),(0,+float('inf')),(0,+float('inf')),(0,+float('inf'))],name="BrendelDHO"):
        Lineshape.__init__(self, params, bounds, name)
        self.pnames = ["wp**2/w0**2", "wT", "gamma","sigma"]
        self.type = "BrendelDHO"
        self.f = 0 

    def __call__(self, w):
        sigma = self.p[3]
        x0 = self.p[1]
        g = self.p[2]
        a = sqrt(w**2 - 1j*g*w) 
        a = a.real - 1j*a.imag #we want the imaginary part to the root to be positive
        prefac = 1j*sqrt(3.14149)*self.p[0]*x0**2/(sqrt(22)*sigma)
        eps = prefac*exp(-.5)*(1/a)*( sp.erfcx(-1j*(a-x0)/sigma) +  sp.erfcx(-1j*(a+x0)/sigma) )
        #self.f = 2*prefac*exp(-x0**2/(2*sigma**2))*(1 + sp.erf(1j*x0/sigma))
        self.f = eps.real[1]
        return (eps.real, eps.imag)
    
    def get_freq(self):
        return self.p[1]
    
    def get_abs_freq(self):
        return sqrt( self.p[1]**2 + self.p[2]**2 )
    
    def print_params(self):
        print( u"%20s f =%7.5f \u03C9 = %6.2f + %6.2f i  (%5.3f ps) \u03C3 = %6.2f cm^-1" % (self.name, self.p[0], self.p[1], self.p[2],  33.34/self.p[1], self.p[3]))
        
    def print_params_latex(self):
        print( u"%20s & %7.5f & %6.2f & %5.3f & %6.2f  & %6.2f \\\\" % (self.name, self.p[0], self.p[1], 33.34/self.p[1], self.p[2], self.p[3]))
        
class DistributionOfDebye(Lineshape):
    '''Under construction'''
    
    def __init__(self,params=[1,1],bounds=[(0,+float('inf')),(0,+float('inf'))],name="BrendelDHO"):
        Lineshape.__init__(self, params, bounds, name)
        #self.pnames = ["wp**2/w0**2", "wT", "gamma","sigma"]
        #self.type = "BrendelDHO"
        #self.f = 0
        #self.num_tau_pts=10000
        ##self.min_tau=
        ##self.max_tau=
        
        #tau_values = logspace(min_tau, max_tau, num_tau_pts)
    
        #def __call__(self, w):
    
        #for m in xrange(1,num_tau_pts+1):
            #gtau(m)*tau

        #def TikhonovRegularization(self):
        #der1 = gradient(gdist)
        #der2 = gradient(der1)
        #return linalg.norm(der2)**2
    
class StretchedExp(Lineshape):
    """Stretched Exponential lineshape """
    def __init__(self,params=[1,1,1],bounds=[(0,10000),(0,10000),(0,1)],name="Str exp"):
        Lineshape.__init__(self, params, bounds, name)
        self.pnames = ["f", "tau", "beta"]
        self.type = "StretchedExp"

    def __call__(self, w):
        (f, eps_omega) = self.calc_eps(w)
        rp = interp(w,f,real(eps_omega))
        cp = interp(w,f,imag(eps_omega))
        return (rp, cp) 
    
    def calc_eps(self,w):
        deltaeps = self.p[0]
        tau = self.p[1]
        beta = self.p[2]
        timestep = 1/(2*3.141*max(w)) #timestep in ps 
        maxt = 3*tau #length of corr function
        npts = int(maxt/timestep)
        times = array(range(0,npts))*timestep
        corr_fun = exp(-(times/tau)**beta)
        nextpow2 = int(2**ceil(log2(npts)))
        f = (1/(2.99*.01))*array(range(0,npts))/(timestep*nextpow2) #Frequencies (evenly spaced), inverse cm
        tderiv = -diff(corr_fun)/timestep #time derivative of corr fun
        eps_omega = deltaeps*ifft(tderiv,nextpow2) #inverse one-sided fourier 
        return (f, eps_omega[0:npts])
        
    def get_freq(self):
        return self.p[1]
    
    def get_abs_freq(self):
        return sqrt( self.p[1]**2 + self.p[2]**2 ) 
    
    def print_params(self):
        print( u"%20s f =%7.5f \u03C9 %6.2f 1/cm (%5.2f ps) \u03B2 = %6.2f" % (self.name, self.p[0], self.p[1], 33.34/(self.p[1]), self.p[2] ))
    
        
class PowerLawDebye(Lineshape):
    """Debye lineshape with additional "power law" wing. 
    See J. Phys. Chem. B, 2005, 109 (12), pp 6031-6035 
    
    Note: the wD parameter is assumed to be in units of cm^-1
    """
    def __init__(self,params=[1,1],bounds=[(0,+float('inf')),(0,+float('inf')),(0,+float('inf')),(1,10)],name="unnamed"):
        Lineshape.__init__(self, params, bounds, name)
        self.pnames = ["f", "wD","A","q"]
        self.type = "PowerLawDebye"
        self.convfac = 1.0#/(2*3.141*2.99*.01)
    
    def __call__(self, w):
        A = self.p[2]
        q = self.p[3]
        tau = self.convfac/self.p[1]
        numomegas = len(w)
        start  = numomegas - len(w[w[:] > self.p[1]])
        HighFreqOmegas = w#0.0*array(w)
        #HighFreqOmegas[start:numomegas] = w[start:numomegas]
        TheWing = 1 + A*(HighFreqOmegas*tau)**q
        rp = TheWing*self.p[0]/(1 + (tau*w)**2)    
        cp = TheWing*self.p[0]*w*tau/(1 + (tau*w)**2)
        return (rp, cp)
    
    def get_freq(self): 
        return self.p[1]
    
    def get_abs_freq(self):
        return self.p[1]
    
    def print_params(self):
        print(u"%20s f =%7.5f \u03C9 %6.2f 1/cm (%5.2f ps) A = %6.2f q = %6.2f" % (self.name, self.p[0], self.p[1], 33.34/self.p[1], self.p[2], self.p[3] ))
        
class ColeCole(Lineshape):
    """Cole-Cole lineshape object.
    
    Note: the wD parameter is assumed to be in units of cm^-1
    """
    def __init__(self,params=[1,1,1],bounds=[(0,+float('inf')),(0,+float('inf')),(0,2)],name="unnamed"):
        Lineshape.__init__(self, params, bounds, name)
        self.pnames = ["f", "wD","alpha"]
        self.type = "Debye"
    
    def __call__(self, w):
        rp = self.p[0]*self.p[1]**2/(self.p[1]**2 + w**2)     
        cp = rp*w/self.p[1]
        return (rp, cp)
    
    def get_freq(self): 
        return self.p[1]
    
    def get_abs_freq(self):
        return self.p[1]
    
    def print_params(self):
        print( u"%20s f =%7.5f \u03C9 %6.2f 1/cm (%5.2f ps) \u03B1 %6.2f" % (self.name, self.p[0], self.p[1], 33.34/self.p[1], self.p[2] ))

class VanVleck(Lineshape):
    """Van Vleck and Weisskopf lineshape Rev. Mod. Phys., 17:227 236, Apr 1945."""
    def __init__(self,params=[1,1,1],bounds=[(-float('inf'),+float('inf')),(-float('inf'),+float('inf'))],name="VanVleck"):
        Lineshape.__init__(self, params, bounds, name)
        self.pnames = ["f", "wT","gamma"]
        self.type = "VanVleck"
        
    #the real part has not been tested or checked to see if it is mathematically correct!!!
    def __call__(self, w):
        rp = .5*self.p[0]*(self.p[1]**2 + self.p[2]**2)( 1/((self.p[1] - w)**2 + self.p[2]**2)  + 1.00/((self.p[1] + w)**2 +  self.p[2]**2) )          
        cp = .5*self.p[0]*self.p[2]*w*( 1/((self.p[1] - w)**2 + self.p[2]**2)  + 1.00/((self.p[1] + w)**2 +  self.p[2]**2) ) 
        return (rp, cp)

    def get_freq(self):
        return self.p[1]
    
    def get_abs_freq(self):
        return sqrt( self.p[1]**2 + self.p[2]**2 ) 

    def print_params(self):
        print( u"%20s f =%7.5f \u03C9= %6.2f + %6.2f i  %6.3f ps" % (self.name, self.p[0], self.p[1], self.p[2],  33.34/(2*3.141*self.p[2]))    )


class Gaussian(Lineshape):
    """Gaussian peak in the imaginary part, ie. inertial absorption or homogenous broadening"""
    def __init__(self,params=[1,1,1],bounds=[(-float('inf'),+float('inf')),(-float('inf'),+float('inf'))],name="Gaussian"):
        Lineshape.__init__(self, params, bounds, name)
        self.pnames = ["f", "wT","gamma"]
        self.type = "BRO"
        
    def __call__(self, w):
        # sp.dawsn
        rp = .5*self.p[0]*(self.p[1]**2 + self.p[2]**2)( 1/((self.p[1] - w)**2 + self.p[2]**2)  + 1.00/((self.p[1] + w)**2 +  self.p[2]**2) )          
        cp = .5*self.p[0]*self.p[2]*w*( 1/((self.p[1] - w)**2 + self.p[2]**2)  + 1.00/((self.p[1] + w)**2 +  self.p[2]**2) ) 
        return (rp, cp)

    def get_freq(self):
        return self.p[1]
    
    def get_abs_freq(self):
        return sqrt( self.p[1]**2 + self.p[2]**2 ) 

    def print_params(self):
        print( u"%20s f =%7.5f \u03C9= %6.2f + %6.2f i  %6.3f" % (self.name, self.p[0], self.p[1], self.p[2],  33.34/(2*3.141*self.p[2])))

    
class constant(Lineshape):
    """this "lineshape" object is merely a constant term"""
    def __init__(self,params=[1],bounds=[(0,100)],name="constant"):
        Lineshape.__init__(self, params, bounds, name)
        self.pnames = ["Eps float('inf')."]
        self.type = "Constant"
    
    def __call__(self,w):
        rp = 0*w + self.p[0]
        cp = 0*w
        return (rp, cp)
    
    def print_params(self):
        print("%20s f =%7.5f" % (self.name, self.p[0]))
    
    def print_params_latex(self):
        print("%20s & %7.5f & & & & \\\\" % (self.name, self.p[0]))

#-----------------------------------------------------------------------------------------------------------
def fit_model_gLST_constraint(modelL, modelT, dataX, Tdatarp, Tdatacp):
        ''' fit both the transverse and longitudinal models at the same time with the gLST constraint  '''

        Ldatarp = 1.0 - Tdatarp/(Tdatarp**2 + Tdatacp**2)
        Ldatacp = Tdatacp/(Tdatarp**2 + Tdatacp**2)
        
        def diffsq(paramsL, paramsT):
            
            modelL.setparams(paramsL)
            modelT.setparams(paramsT)

            (Lrp, Lcp) = modelL(dataX)
            (Trp, Tcp) = modelT(dataX)

            Ldiff = (Ldatarp - Lrp)/Ldatarp + (Ldatacp - Lcp)/Ldatacp 
            Tdiff = (Tdatarp - Trp)/Tdatarp + (Tdatacp - Tcp)/Tdatacp 

            err = dot(Tdiff, Tdiff) + dot(Ldiff, Ldiff)
                        
            return err

        def costfun(params):
            """Wrapper function needed for differential_evolution()

            Args: 
                params: a list of parameters for the model
            Returns: 
                The cost function
            """
            
            paramsL = params[0:len(params)//2]
            paramsT = params[len(params)//2:]
            
            eps0    = Tdatarp[0]
            eps_inf = Tdatarp[-1]
            
            fsumpenalty = ( ( eps0 - modelT.fsum())/Tdatarp[0] )**2
            
            gLST_RHS = eps0/eps_inf
                        
            gLSTpenalty = ( gLST_LHS(modelL, modelT) - gLST_RHS )**2
            
            #print(diffsq(paramsL, paramsT) , gLSTpenalty , 100*fsumpenalty)
            
            return diffsq(paramsL, paramsT)  + 100*fsumpenalty + gLSTpenalty 

        Lparams = modelL.getparams()
        Tparams = modelT.getparams()
        
        params = Lparams + Tparams

        boundsL = modelL.getbounds()
        boundsT = modelT.getbounds()
        
        bounds = boundsL + boundsT
        
        assert len(boundsL) == len(boundsT)
        assert len(params) == len(bounds)
    
        resultobject = optimize.minimize(costfun, x0=params, bounds=bounds, method='TNC')
        print("number of iterations = ", resultobject.nit)
        
        resultobject = optimize.minimize(costfun, x0=params, bounds=bounds, method='SLSQP')
        print("number of iterations = ", resultobject.nit)

        
        #optimize.fmin_l_bfgs_b(costfun, bounds=bounds)
        #optimize.differential_evolution(costfun, bounds)  
    
        Lparams = modelL.getparams()
        Tparams = modelT.getparams()
        
        print("RMS error = ",sqrt(diffsq(Lparams, Tparams)))

#----------------------------------------------------------------------------------------------------
def print_gLST_ratios(modelL, modelT):
    '''try to print out the ratios for different modes. Note this may not be very accurate as the ordering of modes in the longitudinal and transverse model
        may not be the same'''
    
    ratios = ones(modelL.numlineshapes)
    
    if (modelL.numlineshapes == modelT.numlineshapes): 
    
        for i in range(modelL.numlineshapes):
            if modelL.lineshapes[i].type == "Debye":
                ratios[i] = modelL.lineshapes[i].p[1]/modelT.lineshapes[i].p[1]

            if (modelL.lineshapes[i].type == "DHO") or (modelL.lineshapes[i].type == "VanVleck") or (modelL.lineshapes[i].type == "BrendelDHO"):             
                ratios[i] = (modelL.lineshapes[i].p[1]**2 + modelL.lineshapes[i].p[2]**2)/modelT.lineshapes[i].p[1]**2

        set_printoptions(precision=2)
        print("LST Ratios = ", ratios)
        print("Prod of ratios =", prod(ratios))
    else:
        print("Can't compute gLST ratios, number of lineshapes in transverse not equal to number in longitudinal")
    
#----------------------------------------------------------------------------------------------------    
def gLST_LHS(modelL,modelT):
    '''calculate the left hand side of the GLST equation'''

    numerator   = ones(modelL.numlineshapes)
    denominator = ones(modelT.numlineshapes)
    
    for i in range(modelL.numlineshapes):
        if modelL.lineshapes[i].type == "Debye":
            numerator[i] = modelL.lineshapes[i].p[1]

        if (modelL.lineshapes[i].type == "DHO") or (modelL.lineshapes[i].type == "VanVleck") or (modelL.lineshapes[i].type == "BrendelDHO"):             
            numerator[i] = (modelL.lineshapes[i].p[1]**2 + modelL.lineshapes[i].p[2]**2)
            
    for i in range(modelT.numlineshapes):
        if modelT.lineshapes[i].type == "Debye":
            denominator[i] = modelT.lineshapes[i].p[1]

        if (modelT.lineshapes[i].type == "DHO") or (modelT.lineshapes[i].type == "VanVleck") or (modelT.lineshapes[i].type == "BrendelDHO"):             
            denominator[i] = modelT.lineshapes[i].p[1]**2
            
    return prod(numerator)/prod(denominator)
    

##----------------------------------------------------------------------------------
##----- Printout all frequencies in system and left side of gLST equation  --------
##----------------------------------------------------------------------------------
def print_gLST_LHS_stuff(modelL, modelT, Tdatarp, Tdatacp):

    print("longitudinal model:")
    modelL.print_model()
    print("transverse model:")
    modelT.print_model()    

    print_gLST_ratios(modelL, modelT)    
    
    eps0    = Tdatarp[0]
    eps_inf = Tdatarp[-1]
    gLST_RHS = eps0/eps_inf
                
    print("LST LHS = %6.2f" % gLST_LHS(modelL,modelT))
    print("LST RHS = %6.2f" %  gLST_RHS)

    
#-------------------------------------------------------------------------------------------------------------
def plot_model(model,dataX,dataYrp,dataYcp,Myhandle,xmin=None,xmax=None,xscale='linear',yscale='log',ymin=None,ymax=None,show=False,Block=True,longitudinal=False,title='',peaks=[]):
    """displays a pretty plot of the real and complex parts of the model and data using matplotlib

    args: 
        model: a spectral_model object
        dataX: a numpy array giving the experimental x-data
        dataYrp: a numpy array giving the real part of the experimental y-data
        dataYcp: a numpy array giving the complex part of the experimental y-data
        handle: an integer giving the plot window number 
        xmin: scalar, minimum frequency to plot 
        xmax: scalar, maximum frequency to plot
        xscale: string, xscale type 'linear' or 'log'
        yscale: string, yscale type 'linear' or 'log' 
        show: logical, option to display plot
        blockoption: logical, option to block further processing after displaying window (Default True, False is experimental) 
        """
    if (xmin == None):
        xmin = min(dataX)
    if (xmax == None):
        xmax = max(dataX)
    if (ymin == None):
        ymin = min(dataYrp)/600
    if (ymax == None):
        ymax = max(dataYrp)
    if (xscale == 'log'):
        plotomegas = logspace(log10(xmin), log10(xmax), 10000)
    else: 
        plotomegas = linspace(xmin, xmax, 10000)
    
    #if (longitudinal == True):
    #    (rp, cp) = model.longeps(plotomegas)
    #    denom = dataYrp**2 + dataYcp**2     
    #    (dataYrp,dataYcp) = (dataYrp/denom, dataYcp/denom)
    #    (xmin,xmax) = (min(dataX),max(dataX))
    #    (ymin,ymax) = (min(dataYrp),max(dataYrp))
    #else:
    (rp, cp) = model(plotomegas)
    
    # Two subplots, unpack the axes array immediately
    f, (ax1, ax2) = plt.subplots(nrows=2, sharex=True, sharey=False )
    
    ax1.plot(dataX, dataYrp, "g", plotomegas, rp,'b')
    #ax1.set_title('Real part')

    ax2.plot(dataX, dataYcp, "g", plotomegas, cp,'b')
    #ax2.set_title('Complex part')

    #plot all of the components
    for lineshape in model.lineshapes: 
        (rpPart, cpPart) = lineshape(plotomegas)
        ax1.plot(plotomegas, rpPart ,'b--',linewidth=1)
        ax2.plot(plotomegas, cpPart ,'b--',linewidth=1)

    ax1.set_xscale(xscale)
    ax1.set_xlim([xmin,xmax])
    ax1.set_yscale(yscale)
    ax1.set_ylim([ymin,ymax])

    ax2.set_xscale(xscale)
    ax2.set_xlim([xmin,xmax])
    ax2.set_yscale(yscale)
    ax2.set_ylim([ymin,ymax])
    
    ax1.set_xlabel(r"$\omega$ (cm$^{-1}$)")
    ax2.set_xlabel(r"$\omega$ (cm$^{-1}$)")
    
    
    if (longitudinal == True):
        ax1.set_ylabel(r"Re$\lbrace\frac{1}{\varepsilon(\omega)}\rbrace$")
        ax2.set_ylabel(r"Im$\lbrace\frac{1}{\varepsilon(\omega)}\rbrace$")
    else:
        ax1.set_ylabel(r"Re$\lbrace\varepsilon(\omega)\rbrace$")
        ax2.set_ylabel(r"Im$\lbrace\varepsilon(\omega)\rbrace$")
    
    ax1.set_title(title)
    
    

   #ax.annotate('local max', xy=(3, 1),  xycoords='data')

   
#-----------------------------------------------------------------------
# Function to find the maxima of a dataset by looking where the sign of the slope changes
#-----------------------------------------------------------------------
def find_peaks(dataset,omegas):
    #Smooth dataset
    smoothing_length = 5
    dataset = np.convolve(dataset, np.ones(smoothing_length)/smoothing_length)
    
   # lowess = sm.nonparametric.lowess(dataset, omegas, frac=0.5)
    #dataset = lowess[:,1]

    npoints = len(dataset)
    data_shift = np.r_[0, dataset]
    diff = data_shift[0:npoints] - dataset
    peaks = []
    npoints = len(omegas) -1 
    for i in range(0, npoints):
        if np.sign(diff[i]) != np.sign(diff[i+1]):
            #check if in useful range
            if ( 580 <= omegas[i] <= 1000 ) | ( 3000 <= omegas[i] <= 3500 ): #(1500 <= omegas[i] <= 1700)
                peaks =  peaks + [(omegas[i] + omegas[i+1])/2]
    return peaks
