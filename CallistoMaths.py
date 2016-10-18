# -*-coding=utf-8 -*
import numpy as np

class CallistoMaths:
    """ Static class providing a few mathematical methods to work with Callisto's data """
    
    
    def coreMedianeTime(cali):
        """This method computes the median of the temporal serie
        
@param cali : CallistoFITS Object
@return : A vector containing the median of the temporal serie of each frequency

"""
        return np.asarray(np.median(cali.data,1),np.int16)
    
    
    def medianeTime(cali):
        """ This method remove the temporal median in each frequency
        
@param cali : CallistoFITS Object
@return : Source data where the temporal median in each frequency has removed.

"""
        return np.asarray(cali.data -np.asmatrix(CallistoMaths.coreMedianeTime(cali)).T*
        np.ones((1,cali.time.size),np.int16),np.int16)
        
    
    def medianeRelative(cali):
        """ This method compute the relative temporal median in each frequency

@param cali : CallistoFITS Object
@return : Source data where the temporal median in each frequency has removed, then divided by itself to be reduced to a range from 0 to 1.
          Output data are coded over float of 32 signed bits.
"""

        med = np.asmatrix(CallistoMaths.coreMedianeTime(cali)).T * \
        np.ones((1,cali.time.size),np.int16)
        
        return np.asarray((cali.data-med)/med,np.float32)
        
    def flattenFreq(cali):
        """ This method performs a crushing over frequency.
            This computation is done in summing the signal into each frequency

@param cali : CallistoFITS Object
@return : A 1D array

""" 
        return np.sum(cali.data,0)
        
    
    medianeTime = staticmethod(medianeTime)
    coreMedianeTime = staticmethod(coreMedianeTime)
    flattenFreq = staticmethod(flattenFreq)
    medianeRelative = staticmethod(medianeRelative)
    