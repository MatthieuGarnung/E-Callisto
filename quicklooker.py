import os
import time
import sys
import multiprocessing as mp
import itertools as it
import CallistoFITS.CallistoFITS as cf
import CallistoFITS.CallistoMaths as cm
import CallistoFITS.CallistoGraphs as cg
from matplotlib.pyplot import cm as cmm

def searchFit():
    return (name for name in os.listdir() if '.fit' in name)
   

def init(args):
    global avanc
    avanc = args
    
def task(name):
    global avanc
    avanc.value = avanc.value + 1

    cali = cf.CallistoFITS(name)
    cg.CallistoGraphs.graphTemp(cali,'LPC2E',mini=100,maxi=200,mapp=cmm.inferno)
    cali.data = cm.CallistoMaths.medianeRelative(cali)
    cg.CallistoGraphs.mapGraph(cali,'LPC2E','MED')



if __name__ == '__main__':

   avanc = mp.Value('i',0)
   maxi = len(list(searchFit()))
   
   pool_cpu = mp.Pool(processes=3, initializer=init,initargs=(avanc,))
   pool_cpu.imap(task,searchFit())
   pool_cpu.close()
   
   back_value = avanc.value
   
   while avanc.value<maxi:
       
       if back_value!=avanc.value:
           sys.stdout.write('\r%.2f' % (100.0*avanc.value/maxi))
           back_value = avanc.value
           
       time.sleep(1)
   
   
   pool_cpu.join()
    
