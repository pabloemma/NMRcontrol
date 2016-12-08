'''
Created on Aug 8, 2016

@author: klein
'''
"""
main control for NMR analysis chain
"""
import time

import os

import wx



        

class myControl(object):
    """ this is the base class"""
    
    
    def __init__(self,filename):
        """ initialzing routine"""
        #next file is default for now, we will later change this through wx widgets.
        self.ParameterFile=filename
        
        self.ParList = {}   # this will hold the list of parameters from the parameter file
                            #Later we will change these values in the GUI
        # default run parameters for NMRanalzyer
        self.arg1 = "/Users/klein/git/NMRanalyzer/Testfiles/"   
        self.arg2 =  "TER3544457259.root"
        self.arg3a  = "-f "
        self.arg3b = "/Users/klein/git/NMRanalyzer/parameterfiles/test_april25_noQcurve.par"
                            
        
        
        
    def ReadParameterFile(self):
        """ Reads parameter file and puts variables into a dictionary """
        self.ParFile = open(self.ParameterFile,'r+')  # read and write
        

        
        self.TempCopy = self.ParameterFile+'_'+str(time.time()) # Create a backup copy with the current time added
        print "Backup Copy of parameter file: " , self.TempCopy
        
        self.outfil = open(self.TempCopy,'w') 
        

        
        for myline in self.ParFile:  # iterate over the lines
            tempbuf = myline.split()    # split at one white space and slit at the most once
            self.outfil.write(myline)
            print tempbuf[0], tempbuf[1]
            self.ParList[tempbuf[0]] = tempbuf[1]
            
        self.outfil.close()  # now we are safe, the backup is closed
         
        # loop over dictionary
        print "ANa control", self.ParList
        return self.ParList
    
        
    def WriteParameterFile(self):
        """ Creates new file with new parameters this is used if we want to overwrite the file"""
        
        # delete old file by truncating it to 0
        self.ParFile = open(self.ParameterFile,'w')  # read and write
        self.ParFile.truncate(0)
        self.ParFile.close()  # have to do this otherwise we have starnge chracters in the file
        self.ParFile = open(self.ParameterFile,'w')  # read and write
        
        
        
        for k in self.ParList:
            templine =k+'     '+self.ParList[k]+'\n'
            print k, templine
            self.ParFile.write(templine)
        self.ParFile.close()
        # now we can delete the backup copy
        print 'wp',self.TempCopy
        os.remove(self.TempCopy)
        os.remove(self.outfil)
        
    def SaveNewParameterFile(self, filename):
        """ Creates new file with new parameters this is used if we want to overwrite the file"""
        
        # delete old file by truncating it to 0
        self.ParFile1 = open(filename,'w')  # read and write
        
        
        
        for k in self.ParList:
            templine =k+'     '+self.ParList[k]+'\n'
            print k, templine
            self.ParFile1.write(templine)
        self.ParFile1.close()
        # now we can delete the backup copy
        print 'sp',self.TempCopy
 
        os.remove(self.TempCopy)
        os.remove(self.outfil)
        
 
            
    def CreateNMRAna(self):
        """this creates the commandline to be passed to NMRanalyzer,
        again, these are hooks to whatever gets changed in the wxpython list"""
        
        self.NMRcommand = self.arg1+' '+self.arg2+' ' +self.arg3a+self.arg3b
        

    def Cleanup(self):
        """ finishes up"""
        
        #close any open files
        self.ParFile.close()

if __name__ == '__main__':
    import NMR
    myC = myControl()
    myC.ReadParameterFile()
    myC.WriteParameterFile()
    myC.CreateNMRAna()
    myC.Cleanup()
    
    
    
    # now pass control over to root
    
    #myANA = NMR.NMR()
    #print myC.NMRcommand
    #myANA.Analyzer("/Users/klein/git/NMRanalyzer/Debug/NMRana",myC.NMRcommand)
    #pass