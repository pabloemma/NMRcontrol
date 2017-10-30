'''
Created on Oct 25, 2017

@author: klein
'''

import os
import sys 
import time
import subprocess
import datetime
import glob
import shutil

class MainControl(object):
    """ This modules controls the NMR analyzer and the establishes a handshake between
    labview and the analzyer. It will run on both Mac and Linux. 
    The program expects that labview at the begin of the NMR running creates two files
    called lvrun and lvheart. Once labview stops the NMR, it deletes lvrun and creates lvstop.
    lvheart gets touched or updated every x seconds. The control program checks for the following conditions:
    lvrun and not lvstop and lvheart updated. 
    if lvrun and lvstop present: exit
    if lvrun and lvheart not updated: exit
    if lvstop and not lvrun: do nothing.
    
    """
    def __init__(self,directory, anafile):
        
        self.prompt = 'MainControl> '
        self.err = '!!!! err err err !!!!!'
        self.directory = directory # this is the labview storage directory
        self.root_directory = self.directory+'/root'
        self.backup_directory = self.directory +'/backup' # where raw data get moved once it has been analyzed
        #check if directory exists:
        if(not os.path.exists(self.directory)):
            message = self.directory+'   directory does not exist'
            self.ErrorMessage(message)
        if( not os.path.exists(self.backup_directory)):
            os.mkdir(self.backup_directory)
        if( not os.path.exists(self.root_directory)):
            os.mkdir(self.root_directory)
        
        self.run = self.directory+'/lvrun'
        self.stop = self.directory+'/lvstop'
        self.heart = self.directory+'/lvheart'
        self.last_time = 0 # time stamp of last time change
        
        self.anafile = self.directory+'/'+anafile  # this is filename, where all the analyzed files get stored

    def LastRun(self):
        """ determines the last run analyzed assuming the last line in the file
        is the last run """
        
        # determine the last run which has been analyzed
        if(os.path.isfile(self.anafile)):
            #read last line
            with open(self.anafile, "rb") as f:
                first = f.readline()        # Read the first line.
                f.seek(-2, os.SEEK_END)     # Jump to the second last byte.
                while f.read(1) != b"\n":   # Until EOL is found...
                    f.seek(-2, os.SEEK_CUR) # ...jump back the read byte plus one more.
                self.LastAnalyzed = f.readline()         # Read last line.
                print self.LastAnalyzed
                f.close()
        else:
            # create the anafile
            f = open(self.anafile,"w+")
            mydate  =time.strftime("%d/%m/%Y")
            mytime = time.strftime("%H:%M:%S")
            myline = '********************************************************\n\n'
            f.write(myline)
            myline = 'this file has been created on '+ mydate +' @ '+mytime +'\n'
            f.write(myline)
            myline = '********************************************************\n\n'
            f.write(myline)
            self.LastAnalyzed = ''
            f.close()
            
    def OuterLoop(self): 
        """ this is outer loop, just checking for labview run or stop """   
        if(os.path.isfile(self.run)  and not os.path.isfile(self.stop)):
            print self.prompt, "labview is running, checking for hearbeat"
            self.InnerLoop()

        elif(os.path.isfile(self.run) and os.path.isfile(self.stop)):
            self.ErrorMessage(' we have both start and stop file, fix this first ')
            
        elif( not os.path.isfile(self.run)):
            print self.prompt,' waiting for Labview'
        
    def InnerLoop(self):
        """ this is the main inner loop, it will wait for heart beat """
        
             #check if labiew is running
        
        while True:
            if(os.path.isfile(self.heart)):
            # check that hearbeat file has been updated
                stamp = os.stat(self.heart).st_mtime
                if(stamp != self.last_time):
                        last_time = stamp
                self.DoActionNew()
                        
                        
                        
            else:
                    # wait for wakeup
                print 'waiting for heartbeat'
                time.sleep(5) # time out for 30 seconds
                
                
    def DoAction(self):  
        """ this checks if run has been analyzed, and if not will run analyzer engine.
        There is a master file of analyzed runs. it checks for last entry and sees if there are any newer files.
        If newer files exist it will analyze them, under the condition that there is an .avg file .
        The .avg file gets created by Labview when the run is finished. This way we ensure that we are not
        analyzing runs, which are not finished. the dirctory for the analyzed files is a subdirectory of the cvs 
        files called root
        """
        # check for latest file , but see below.
        list_of_files = glob.glob(self.directory+'/*') # * means all if need specific format then *.csv
        print list_of_files
        latest_file = max(list_of_files, key=os.path.getctime)
        print latest_file
        while True:
            if(latest_file == self.anafile or latest_file == self.heart):
                print " no changes"
            else:
                print latest_file
                # now check if it is analyzed
                if(latest_file != self.LastAnalyzed):
                    print "need to analyze file"
                    # this is where we need to start analyzer
                    # however there is still a problem:if we have created more than one file
                    # since the last update of the analyzed file, currently this will only
                    # analyze the absolute last one.
                    #maybe a better way to do is to determine the mtime of the last analyzed
                    # and then list all the files which have a newer mtime
                    # exclude the ones w=hich do not have the typical
                    # 3 characters as starting point.
                    # in order not to make the list of files longer and longer
                    # we need to move the csv files into a subdirectory called backup
                    # that might be the easiest way, the moment a file is analyzed move it to backup
                else:
                    print "that file is already analyzed"
                pass
        
    def DoActionNew(self):  
        """ this checks if run has been analyzed, and if not will run analyzer engine.
        There is a master file of analyzed runs. it checks for last entry and sees if there are any newer files.
        If newer files exist it will analyze them, under the condition that there is an .avg file .
        The .avg file gets created by Labview when the run is finished. This way we ensure that we are not
        analyzing runs, which are not finished. the dirctory for the analyzed files is a subdirectory of the cvs 
        files called root
        """
        # check for latest file , but see below.
                    # this is where we need to start analyzer
                    # however there is still a problem:if we have created more than one file
                    # since the last update of the analyzed file, currently this will only
                    # analyze the absolute last one.
                    #maybe a better way to do is to determine the mtime of the last analyzed
                    # and then list all the files which have a newer mtime
                    # exclude the ones w=hich do not have the typical
                    # 3 characters as starting point.
                    # in order not to make the list of files longer and longer
                    # we need to move the csv files into a subdirectory called backup
                    # that might be the easiest way, the moment a file is analyzed move it to backup
        # get list of files with extension csv in directory
        f=open(self.anafile,'a') #open file for append
        list_of_files = glob.glob('*.csv')
        for myfile in list_of_files:
            # analyze files
            f.write(myfile) #append to analyzed
            shutil(self.directory+'/'+myfile , self.backup_directory+'/'+myfile) # move raw file to backup
        f.close()
            
        
        
        
        
    
    def CreateTime(self,name):
        """
        Create an integer from the time part of the labview run names
        used to det"""
        temp = name[3:len(self.LastAnalyzed)]
        datestring = temp[0:len(temp)-4]
        return int(datestring)
    
    
    def GetDate(self): 
        datestring = self.CreateTime(self.LastAnalyzed)
        print datestring
        # now strip the firts three chracters and the last 4 to just get the labview date
        # now convert to integer
        mytime = int(datestring)-2082844800  #labview to Unix time alignment
        # convert to unix time
        print 'last run analyzed ',datetime.datetime.fromtimestamp(mytime).strftime('%Y-%m-%d  @  %H:%M:%SZ')
        

   
        
            
                
            
            
    def ErrorMessage(self, myerror):  
        """
         prints out error message"""
        print   self.prompt,self.err,myerror,self.err
        sys.exit()  
        
        



if __name__ == '__main__':
    ana_dir = '/Users/klein/labviewtest'
    ana_name = 'analyzed_files.txt'

    MS = MainControl(ana_dir,ana_name)
    MS.LastRun()
    MS.GetDate()
    MS.InnerLoop()
    pass