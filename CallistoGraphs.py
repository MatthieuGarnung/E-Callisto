# -*-coding=utf-8 -*
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.gridspec as mpl_grid
import CallistoFITS.CallistoMaths as cm
import datetime

class CallistoGraphs:
    
    """ Static class provides a lot of methods to plot Callisto data"""
    
    def _createDate(cali):
        """ This method creates a datetime object to manipulate the date and the hour of the begin of the observation
        
@param cali : CallistoFITS object
@return datetime : datetime object (Python Object) contening the date and the hour of the begin of the observation
@see : datetime in Python3's documentation

"""
        date = cali.getDate().split('/')
        date = [int(i) for i in date]
        starthour = cali.getStartTime()
        starthour = starthour[:starthour.rfind('.')]
        starthour = starthour.split(':')
        starthour = [int(i) for i in starthour]
        tmp = date + starthour
        
        return datetime.datetime(*tmp)
     
    def _xaxisTick(cali,date,nbr=5):
        """ This method sets the text and the label position of labels over x axis.
        
@param cali : CallistoFITS object
@param date : datetime object providing the time of the observation
@param nbr : Number of labels over the x axis
@return tuple : (label position, text label)
@see : _createDate

"""
    
        step = cali.time.size//nbr
        pos_xtick = np.arange(0,cali.time.size+step,step)
        pos_xtick[-1] -= 1
        txt_xtick = [(date+datetime.timedelta(seconds=i)).strftime('%H:%M:%S') for i in cali.time[pos_xtick]]
        
        return (pos_xtick, txt_xtick)
       
    def _yaxisTick(cali, freq=None, nbr=8):
        """ This method sets the text and the label position of labels over y axis.
        
@param cali : CallistoFITS object
@param date : datetime object providing the time of the observation
@param nbr : Number of labels over the y axis
@return tuple : (label position, text label)
@see : _createDate

"""    
        if freq is None:
            freq = cali.freq
        
        pos_ytick = np.arange(0,freq.size,freq.size//nbr)
        txt_ytick = ['{:.0f}'.format(i) for i in freq[pos_ytick]]
        
        return (pos_ytick, txt_ytick)
       
    def _blackBand(cali,fmin,fmax):
        """ This method allow to insert black bands over frequency axis. These black bands show where the Callisto instrument has not done a measure.
            Their insertion have to recompute both frequency axis and data matrix from raw data.

@param cali : CallistoFITS object
@param mini : The lowest frequency
@param maxi : The highest frequency
@return tuple : (frequency, data within black bands)

"""
        
        freq = np.flipud(np.arange(fmin,fmax))
        data = np.empty((freq.size,cali.time.size),np.int16)*np.nan

        for ind,f in enumerate(np.floor(cali.freq)):
            pos = np.where(f==freq)[0]
            
            if pos.size!=0:
                data[pos,:] = cali.data[ind,:]
                
        return (freq, data)
                

    def _createName(date,prefix='',sep='_'):
        return prefix+sep+date.strftime('%Y%m%d')+sep+date.strftime('%H%M%S')
        
        
    def savefig(name,dpi=300):
        """ This method saves the plot in to a file. By default, it is a .png file.

@param name : Filename
@param dpi : Resolution
@see Matplotlib.pyplot.savefig()

"""
        plt.savefig(name+'.png',dpi=dpi)
    
    def mapGraph(cali,prefix='',suffix='',sep='_',mapp=plt.cm.jet,mini=None,maxi=None,black_band=True,fmin=-1,fmax=-1,savefig=True,dpi=300):
        
        plt.clf()
        
        if fmin==-1 or fmax==-1:
            fmin = np.floor(cali.freq.min())
            fmax = np.floor(cali.freq.max())

        date = CallistoGraphs._createDate(cali)
        pos_xtick, txt_xtick = CallistoGraphs._xaxisTick(cali,date)
        
        if suffix == '':
            name = prefix+CallistoGraphs._createName(CallistoGraphs._createDate(cali))
        else:
            name = prefix+CallistoGraphs._createName(CallistoGraphs._createDate(cali))+sep+suffix
        
        ax = plt.gca()
        
        if black_band:
        
            ax.set_axis_bgcolor('black')
           
            freq, data = CallistoGraphs._blackBand(cali,fmin,fmax)
            
            pos_ytick, txt_ytick = CallistoGraphs._yaxisTick(cali,freq)

        else:
            pos_ytick, txt_ytick = CallistoGraphs._yaxisTick(cali)
            data = cali.data
            
        img = ax.imshow(data,cmap=mapp,aspect='auto',interpolation='none', vmin=mini,vmax=maxi)     
        ax.set_xticks(pos_xtick)
        ax.set_xticklabels(txt_xtick)
        ax.set_yticks(pos_ytick)
        ax.set_yticklabels(txt_ytick)
        ax.set_xlabel('Time (UT)')
        ax.set_ylabel('Frequence (MHz)')
        ax.set_title('{}  $ SNR={:3f}'.format(date,cali.snr))
        cb = plt.colorbar(img,ax=ax,orientation='horizontal',shrink=0.7)
        cb.set_label('Valeur instrumentale')
        
        if savefig:
            CallistoGraphs.savefig(name,dpi=300)
           
        else:
            return (name, pos_xtick, txt_xtick)
          
            
    def graphTemp(cali,prefix='',suffix='',sep='_',mapp=plt.cm.jet,mini=None,maxi=None,black_band=True,fmin=-1,fmax=-1,savefig=True,dpi=300):
        
        plt.clf()
        
        ax = plt.axes([0.1, 0.45, 0.8, 0.5])
        ax2 = plt.axes([0.25, 0.35, 0.5, 0.03])
        ax1 = plt.axes([0.1, 0.1, 0.8, 0.2])
        
        if fmin==-1 or fmax==-1:
            fmin = np.floor(cali.freq.min())
            fmax = np.floor(cali.freq.max())

        date = CallistoGraphs._createDate(cali)
        pos_xtick, txt_xtick = CallistoGraphs._xaxisTick(cali,date)
        
        if suffix == '':
            name = prefix+CallistoGraphs._createName(CallistoGraphs._createDate(cali))
        else:
            name = prefix+CallistoGraphs._createName(CallistoGraphs._createDate(cali))+sep+suffix
        
        
        if black_band:
        
            ax.set_axis_bgcolor('black')
           
            freq, data = CallistoGraphs._blackBand(cali,fmin,fmax)
            
            pos_ytick, txt_ytick = CallistoGraphs._yaxisTick(cali,freq)

        else:
            pos_ytick, txt_ytick = CallistoGraphs._yaxisTick(cali)
            data = cali.data
            
        img = ax.imshow(data,cmap=mapp,aspect='auto',interpolation='none', vmin=mini,vmax=maxi)     
        ax.set_xticks(pos_xtick)
        ax.set_xticklabels(txt_xtick)
        ax.set_yticks(pos_ytick)
        ax.set_yticklabels(txt_ytick)
        ax.set_ylabel('Frequence (MHz)')
        
        ax.set_title('{}  $ SNR={:3f}'.format(date,cali.snr))
        cb = plt.colorbar(img,cax=ax2,orientation='horizontal')
        #cb.set_label('Valeur instrumentale')
        
        
        
        ax1.grid(True)
        ax1.plot(cali.time,cm.CallistoMaths.flattenFreq(cali),'g')
        #ax1.plot(cali.freq, np.sum(cali.data,0),'g')
        ax1.set_xlabel('Time (UT)')
        ax1.set_ylabel('Flux total')
        ax1.set_xlim((150,190))
        ax1.set_xticks(cali.time[pos_xtick])
        ax1.set_xticklabels(txt_xtick)
        
        if savefig:
            CallistoGraphs.savefig(name,dpi=300)

            
    _createDate = staticmethod(_createDate)
    _blackBand = staticmethod(_blackBand)
    _createName = staticmethod(_createName)
    _xaxisTick = staticmethod(_xaxisTick)
    _yaxisTick = staticmethod(_yaxisTick)
    mapGraph = staticmethod(mapGraph)
    savefig = staticmethod(savefig)
    graphTemp = staticmethod(graphTemp)

                        