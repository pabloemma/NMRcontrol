'''
Created on Oct 25, 2017

@author: klein
'''
#import  termios
import  tty
import platform
import getpass
import os
import sys 
import time
import subprocess
import datetime
import glob
import shutil
import threading # we will run the analyzer in a secodn thread

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
    
    There are a couple of directories
    
    the labview_root directory
    and beneath it:
    control  ,  root , backup
    control has the lvrun,lvstop and lvheart in it
    root has the converted root files
    backup has the raw files after it had been converted.
    
    """
    def __init__(self,directory, anafile, convert_engine_dir, online):
        
        self.prompt = 'MainControl> '
        self.err = '!!!! err err err !!!!!'
        self.directory = directory # this is the labview storage directory
        self.root_directory = self.directory+'/root'
        self.control_directory = self.directory+'/control'
        self.backup_directory = self.directory +'/backup' # where raw data get moved once it has been analyzed
        self.convert_engine_dir = convert_engine_dir
        #check if directory exists:
        if(not os.path.exists(self.directory)):
            message = self.directory+'   directory does not exist'
            self.ErrorMessage(message)
        if(not os.path.exists(self.control_directory)):
            message = self.control_directory+'   directory does not exist'
            self.ErrorMessage(message)
        
        if( not os.path.exists(self.backup_directory)):
            os.mkdir(self.backup_directory)
        if( not os.path.exists(self.root_directory)):
            os.mkdir(self.root_directory)
        
        self.run = self.control_directory+'/lvrun'
        self.stop = self.control_directory+'/lvstop'
        self.heart = self.control_directory+'/lvheart'
        self.online = online # if this is true it checks for hearbeat
        self.last_time = 0 # time stamp of last time change
        
        self.anafile = self.directory+'/'+anafile  # this is filename, where all the analyzed files get stored
        
        #go to labview data dir
        os.chdir(self.directory)

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
                temp = f.readline()        # Read last line.
                self.LastAnalyzed = temp.strip('\n')        # Read last line.
                print "last file analyzed", self.LastAnalyzed
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
            
       
    def InnerLoop(self):
        """ this is the main inner loop, it will wait for heart beat """
        
             #check if labiew is running
        while True:
            if not (self.online):
            # manually add to heartbeat, since we are offline
                os.utime(self.heart) #set herabeat file to current time

            if(os.path.isfile(self.heart)):
            # check that hearbeat file has been updated
                stamp = os.stat(self.heart).st_mtime
                if(stamp != self.last_time):
                        self.last_time = stamp
                        self.DoActionNew()  
                        
                        
                        
                else:
                    # wait for wakeup
                    print 'waiting for heartbeat, seems the NMR is nor running'
                    time.sleep(10) # time out for 30 seconds
                
                
          
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
            #now strip extension
            if(myfile != self.LastAnalyzed):
                temp=myfile[0:len(myfile)-4]

                arg2 = '-k'+self.directory +'/  -i '+temp
                command = self.convert_engine_dir +'ReadNMR_short '+arg2 
                print "***************    ",command
                os.system(command)

            
                shutil.move(self.directory+'/'+myfile , self.backup_directory+'/'+myfile) # move raw file to backup
                f.write(myfile) #append to analyzed
                f.write('\n')
                self.LastAnalyzed = myfile
                self.GetDate()
            else:
                shutil.move(self.directory+'/'+myfile , self.backup_directory+'/'+myfile) # move raw file to backup
               

        f.close()
            
        
        
        
        
    
    def CreateTime(self,name):
        """
        Create an integer from the time part of the labview run names
        used to det"""
        temp = name[3:len(self.LastAnalyzed)]
        datestring = temp[0:len(temp)-4]

        return int(datestring)
    
    
    def GetDate(self): 
        temp =self.LastAnalyzed[0:3]
        
        if not (temp == "TEQ" or temp == "POL" or temp == "QCV"):
            return
        else:
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
    # first detect opearting system
    # on MAC the home directory is /Users/name
    # on linux it is /home/name
    if(platform.system() == 'Linux'):
        home='/home/'+getpass.getuser()+'/'
    else:
        home='/Users/'+getpass.getuser()+'/'
    
    
    ana_dir = home+'labviewtest'
    ana_name = 'analyzed_files.txt'
    convert_engine_dir = home+'git/NMR_short/ReadNMR_short/Debug/'
    online = True
    MS = MainControl(ana_dir,ana_name,convert_engine_dir,online)
    MS.LastRun()
    MS.GetDate()
    MS.InnerLoop()
    pass