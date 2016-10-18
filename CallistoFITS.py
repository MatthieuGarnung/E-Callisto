# -*-coding=utf-8 -*
import numpy as np
import pyfits
import h5py as h5
import hashlib

class CallistoFITS:
    """This Class provides a higl-level access to FITS from E-Callisto instrument"""
    
    def __init__(self,filename=''):
        """ Constructor of the class"
        
@param filename : Filename of FITS file
@return : An object CallistoFITS

"""
        self.filename = filename
        self.time = None
        self.freq = None
        self.data = None
        self.checksum = None
        self.snr = None
        
        if self.filename!='':
            self._extractData(self.filename)
            self._calculSNR()
            self._checkSum()

    

    def __eq__(self,otherCallisto):
        """ Surcharge of the operator == in the aim to test the egality between twos E-Callisto files.
            The test of th egality is based on the comparaison of the checksum between files.
            The hash algorithm used is the SHA-256

@param otherCallisto : Another Callisto object
@return : True if files are identical otherwise, False.

"""
        if self.checksum == otherCallisto.checksum:
            return True
        else:
            return False
            
    def _checkSum(self):
        """ This method computes the SHA-256 of a file

"""
        fid = open(self.filename,'rb')
        tmp = fid.readline()
        fid.close()
        
        self.checksum = hashlib.sha256(tmp).hexdigest()
        
    
    def _calculSNR(self):
        """ This methods computes the SNR (Signal to Noise Ratio)

The computation of the SNR is based on the follow equation : SNR = \frac{\<data\>}{\sigma} where \sigma is the standard deviation.
In case of a \sigma equal to zero, the method returns a NaN.

"""
        try:
            self.snr = self.data.mean() / self.data.std()
        except RuntimeWarning:
            self.snr = np.nan
             
    def _extractData(self,filename):
        """ This methodes allow to extract data from a FITS file.
            
@param filename : Filename
@return : Time, Frequency and Data on 8 unsigned bits.
@note : This method can throws a exception if a problem occurs with the FITS file

"""
        
        self.data = pyfits.getdata(filename)
        tmp = pyfits.getdata(filename,1)
        self.time = tmp[0][0]
        self.freq = tmp[0][1]
        
        self._correctionDatas()
            
 
    def loadFile(self,filename):
        """ This method permits to load a file, that mean it affects a filename to the object itself.
Moreover, it computes the checksum of the file. However, this method does not get data, use _extractData
        
@param filename : Filename

"""
        
        self.filename = filename
        self._checkSum()
    

    def loadData(self):
        """ This method permits to extract a data from FITS File
        
@note : This method can throws an exception if a problem occus with the file.
    
"""       
        self._extractData(self.filename)
    
    def getHeader(self):
        """ This method permits to get the header of a FITS file under the form of a dictionnary structure.
        
@return dict : Header
@note : This method can throws an exception if a problem occus with the file.

"""

        return pyfits.getheader(self.filename)

    def getDate(self):
        """ This method gives the data of the observation from the 'DATA-OBS' field contained in the header.
        
@return string : Date
@note : This method can throws an exception if a problem occus with the file.

"""
        header = self.getHeader()
        return header['DATE-OBS']
   
    def getStartTime(self):
        """ This method gives the time of the observation from the 'TIME-OBS' field contained in the header.
        
@return string : Start time of the observation
@note : Peut renvoyer une exception si fichier incorrect

"""
        header = self.getHeader()
        return header['TIME-OBS']
    
    def _correctionDatas(self):
        """ This method corrects a feature of Callisto"""
        
        self.freq = self.freq[:-7]
        self.data = self.data[:-7,:]
        

    def fitToTxt(self,filenameOut1='', filenameOut2=''):
        """ This method permits to get in a standard ASCII text file data into the FITS file
In the standard case, the file of frequencies and time will be named $Filename+_'1D.txt', and
the file containing data (matrix) will be named $Nom_du_fichier+_'2D.txt'.
In the file named $Filename+_'1D.txt', the first column is for the time and the second for the frequency.
        
@param filenameOut1 : Filename for the file will contain time and frequency
@param filenameOut2 : Filename for the file will contain data

"""
        tmp = np.append(self.freq,np.empty((self.time.size-self.freq.size,))*np.nan)
        
        if filenameOut1=='': filenameOut1 = self.filename[:-4]+'_1D.txt'
        if filenameOut2=='': filenameOut2 = self.filename[:-4]+'_2D.txt'
            
        np.savetxt(filenameOut1,np.vstack((tmp, self.time)).T)
        np.savetxt(filenameOut2,self.data)
        
        
    def fitToHDF5(self,filenameOut=''):
        """ This method allows to convert a E-Callisto FITS file in to a HDF5 file.
            This function was created only to permit to work with this fucking bullshit Scilab software,
            which is unable to manage FITS file ! Scilab, Fuck you !!
            
        """
        
        if filenameOut=='':
            filenameOut=self.filename[:-3]+'hdf5'
            
        file = h5.File(filenameOut,'w')
        file.create_dataset('Time',data=self.time)
        file.create_dataset('Freq',data=self.freq)
        file.create_dataset('Data',data=self.data)
        file.close()
        
        