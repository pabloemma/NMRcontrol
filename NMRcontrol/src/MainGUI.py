'''
Created on Aug 17, 2016

@author: klein
'''
import wx
import os
import AnaControl as ANA
import HelpGUI
import NMR
import ControlShort
import threading # we will run the analyzer in a secodn thread
import subprocess
from copy import  deepcopy
import getpass # to chekc for username, only way I can get the shell commands right
#import ParFrame as PF










class MainGUI(wx.App):
    '''
    This is the top application controlling things
    '''
    def __init__ (self,redirect=True, filename=None, EDir = None, RDir = None):
        """ creates the parameters, parameter list is what is contained in parameter file"""
        print "Parameter Frame init"
        self.ParFilename = filename
        self.EngineDir = EDir
        self.RunDir = RDir
        wx.App.__init__(self,redirect,filename)


    def OnInit(self): 
        self.frame = MyFrame(parent=None,id=-1,title= "NMR control", filename = self.ParFilename,edir = self.EngineDir,rdir=self.RunDir)
        print " id of frame",self.frame.GetId()

        
        
 
        self.frame.Show()
        # make this the topwindow
        self.SetTopWindow(self.frame)
        print "I am in OnInit"
        # temporarya dialog
        return True


class MyFrame(wx.Frame):
    """ This is the main control frame 
    This is changed from GUI.py
    I am trying to get everything into one controll box if possible
    
    """
    def __init__ (self,parent,id,title, filename,edir,rdir):
        print "Frame init"
        #
        self.panelx=800
        self.panely=800
        wx.Frame.__init__(self,parent,id,title,pos = (100,100),size = (self.panelx,self.panely),style = wx.DEFAULT_FRAME_STYLE)
        # determine the parent Id so that we can place parameter panel into main panel (hopefully)
        self.MyPanel = wx.Panel(self)
        
        #Instantiate my control, first check if there is a parameter file defined.
        if(filename == None):  # if we give no filename, then we need to assign a dummy string so that the os.path can find file (it expects string)
            filename='dummy'
        if(os.path.isfile(filename)):
            self.ParFilename=filename
            print "using parameter file " ,self.ParFilename
        else :
            dlg1 = wx.FileDialog(None,"Choose Parameter File")
            dlg1.ShowModal()
            if dlg1.ShowModal() == wx.ID_OK:
                self.ParFilename = dlg1.GetPath()
                dlg1.Destroy()
        print "using parameter file " ,self.ParFilename
 
        
        self.myC = ANA.myControl(self.ParFilename)
        # read papameter file
        self.ParList = self.myC.ReadParameterFile()
        print "Gui", self.ParList


        #location of the two analysis engines.
        self.SetAnaEngineDir(edir)
        self.SetRunShortEngineDir(rdir)
        
        
        

        self.myANA = NMR.NMR() #instantiate the engie
        self.NMRthread = [] # create an empty list of threads
        self.NMRthreadcount = 0 # number of threads

        # create a background color
        MyColor =wx.Colour(240)
        MyColorF =wx.Colour(240-50)
        #self.MyPanel.SetBackgroundColour(MyColor)
        self.MyPanel.SetForegroundColour(MyColorF)
        
        
        self.MyStatusBar = self.CreateStatusBar()
        self.MyToolBar = self.CreateToolBar()

        #self.ParFileName = filename
        
        
        
        menuBar = wx.MenuBar()  # Create the menu bar
        menu1 = wx.Menu()
          

        menuitem1 = menu1.Append(wx.NewId(),"Q&uit")
        menuBar.Append(menu1, "&File") # add this submenu to the menu bar


        menuHelp = wx.Menu()  #this is the control menu

        menuHelp1 = menuHelp.Append(wx.NewId(),"Help on GUI") # the commands are (id, menu item, what is whown with mouse over)
        menuHelp2 = menuHelp.Append(wx.NewId(),"Help on Analyzer") # the commands are (id, menu item, what is whown with mouse over)
        menuBar.Append(menuHelp,"Help")
         

        self.Bind(wx.EVT_MENU,self.OnExit,menuitem1) # bind action to menu item       
        self.Bind(wx.EVT_MENU,self.OnHelpGui,menuHelp1)
        self.Bind(wx.EVT_MENU,self.OnHelpAnalyzer,menuHelp2)


 
        self.SetMenuBar(menuBar)
      
        

            #binding the action to the menus

        
        # now create the sizer
        #self.NewPanelLayout()
        self.PanelLayout()

        self.MyPanel.Show()
        #self.ParList = ParList
        
        
        
        
        
    def NewPanelLayout(self):  
        """ test for layout of panel
        """  
        
        self.NewSizer = wx.GridBagSizer( hgap = 5, vgap =5)
        
        self.MyFileLabel = wx.StaticText(self.MyPanel, wx.ID_ANY,"Parameter File")  # put the variable name from the key
        #self.MyFileLabel = wx.TextCtrl(self.MyPanel, wx.ID_ANY,"Parameter File")  # put the variable name from the key
        rowpos= 0   # for grid sizer , absolute row position (y pos)
        colpos= 0# absolute column position (x pos)
        rowspan = 1 # span in y or rows
        colspan = 4 #span in x or columns
        
        wxflag = wx.ALIGN_CENTER_VERTICAL | wx.ALL
        
        self.NewSizer.Add(self.MyFileLabel,pos = (rowpos, colpos),span=(rowspan,colspan),flag = wxflag)

        self.MyFileInput = wx.TextCtrl(self.MyPanel, wx.ID_ANY,self.ParFilename ,size=(500,25),style = wx.TE_PROCESS_ENTER|wx.TE_AUTO_SCROLL | wx.TE_PROCESS_TAB)
        colpos += 7
        colspan += 10
        self.NewSizer.Add(self.MyFileInput,pos = (rowpos,colpos),span=(rowspan,colspan),flag=wxflag)

        

        
        
        self.MyPanel.SetSizer(self.NewSizer)
        self.MyPanel.SetBackgroundStyle(wx.BG_STYLE_ERASE)
        self.MyPanel.Show()
        #self.Fit()

        
        
    
    def PanelLayout(self): 
        
        
        # create a grid bag sizer
        self.MySizer = wx.GridBagSizer( hgap = 3, vgap =3)
        
        # currently add two things, namely the file diaolog and the run button
        
        
        #Display filename turns out I need to define the size in the tex ctrl box
        self.MyFileLabel = wx.StaticText(self.MyPanel, wx.ID_ANY,"Parameter File",size =(100,25))  # put the variable name from the key
        self.MyFileLabel.SetForegroundColour((245,245,245)) # see http://www.tayloredmktg.com/rgb/
        self.MyFileInput = wx.TextCtrl(self.MyPanel, wx.ID_ANY,self.ParFilename ,size=(500,25),style = wx.TE_PROCESS_ENTER|wx.TE_AUTO_SCROLL | wx.TE_PROCESS_TAB)
 
        #bind textctrl to right click
        self.MyFileInput.Bind(wx.EVT_RIGHT_DOWN, self.OnFileDialogSingle) # bring up file dialog when right clicked
        self.MyFileInput.Bind(wx.EVT_TEXT_ENTER, self.OnFilePressedEnter) # save new file name

        #self.MyFileInput.Bind(wx.EVT_SET_FOCUS, self.OnFileDialog) 
        
        wxflag = wx.ALIGN_CENTER_VERTICAL | wx.ALL
        
        #self.MySizer.AddGrowableCol(colpos, 10) # make colum4 growable
        self.MyInputFileLabel = wx.StaticText(self.MyPanel, wx.ID_ANY,"InputFile",size=(100,25))  # put the variable name from the key
        self.MyInputFileLabel.SetForegroundColour((245,245,245))

        FileButton = wx.RadioButton(self.MyPanel,-1,"Analyzer")

        #FileButton = wx.Button(self.MyPanel,-1,"Analyzer",)
        

        
        
        rowpos= 0   # for grid sizer , absolute row position (y pos)
        colpos= 0# absolute column position (x pos)
        rowspan = 1 # span in y or rows
        colspan = 4 #span in x or columns

        
        self.MySizer.Add(self.MyFileLabel,pos = (rowpos, colpos),span=(rowspan,colspan),flag = wxflag)
        colpos = colspan
        self.MySizer.Add(self.MyFileInput,pos = (rowpos,colpos),span=(rowspan,colspan),flag=wxflag)
        colpos = 0
        rowpos = rowpos+rowspan        
        self.MySizer.Add(self.MyInputFileLabel,pos = (rowpos,colpos),span=(rowspan,colspan))
        colpos = colspan
        self.MySizer.Add(FileButton,pos = (rowpos,colpos))
        rowpos = rowpos+rowspan
        
        
        # bind to rght click
        #self.MyInputFileLabel.Bind(wx.EVT_RIGHT_DOWN, self.OnFileDialogMultiple) 
    
        
        # create the run button
        
        
        
        #set up pamatere block
        
        self.MyIcon = []
        self.MyLabelArray = []
        self.MyInputArray = []
        self.MyLabel = []
        self.MyInput = []
        for k in self.ParList:
            self.MyLabel.append(k)            
            self.MyInput.append(self.ParList[k])
            
        #create the tex boxes
        self.counter =0 
        self.ParListOriginal= deepcopy(self.ParList)  # here we stor the original parameter list; at the end before we run we check if anything has changed
        # if that is the caase we ask user to either overwrite parameters of save them.
        for k in self.ParList:
            print k
            #store in original list
#            self.MyLabelArray.append(wx.StaticText(self.panel, wx.ID_ANY, k))  # put the variable name from the key
            self.MyLabelArray.append(wx.TextCtrl(self.MyPanel, wx.ID_ANY, k,style = wx.TE_READONLY))  # put the variable name from the key
            self.MyInputArray.append(wx.TextCtrl(self.MyPanel, wx.ID_ANY, self.ParList[k],style = wx.TE_PROCESS_ENTER ))
            print self.counter+2
            self.MyLabelArray[self.counter].SetBackgroundColour('Yellow')
            self.MySizer.Add(self.MyLabelArray[self.counter], pos=(4+self.counter,0),span=(1,4))
            self.MySizer.Add(self.MyInputArray[self.counter], pos=(4+self.counter,colspan),span=(rowspan,2))
            self.counter = self.counter+1

        #control buttons
        #stop does not do anything yet
        
        #RunButton = wx.RadioButton(self.MyPanel,-1,"Run")
        RunButton = wx.Button(self.MyPanel,-1,"Run",)
        RunButton.SetBackgroundColour('Blue')
        RunButton.ClearBackground()
        
       
        self.MySizer.Add(RunButton,pos = (4+self.counter,1))
        StopButton = wx.Button(self.MyPanel,-1,"Stop")
        StopButton.SetBackgroundColour('Red')
        self.MySizer.Add(StopButton,pos = (4+self.counter,4))
        SaveButton = wx.Button(self.MyPanel,-1,"Save Parameter File",)
        SaveButton.SetBackgroundColour('green')
        SaveButton.ClearBackground()
        self.MySizer.Add(SaveButton,pos = (4+self.counter,6))

        # Now set up a button for running the input converter
        RunConverterButton = wx.Button(self.MyPanel,-1,"Converter",)
        RunConverterButton.SetBackgroundColour('Green')
        RunConverterButton.ClearBackground()
        self.MySizer.Add(RunConverterButton,pos = (1,6))

          
        
        #do the parametre list with independent window, but then give the parameters in boxes on main control
        
         
        # file list
        self.MyFileList=wx.ListCtrl(self.MyPanel, wx.ID_ANY,pos=(600,300),size=(400,800),style=wx.LC_REPORT)
        self.MyFileList.InsertColumn(0,'!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!! Input files for analysis file !!!!!!!!!!!!!!!!!!!!!!!!')
        self.MyFileList.SetColumnWidth(0,wx.LIST_AUTOSIZE)
        
        #self.MyFileList.InsertStringItem(1,'test')

        
        # add the title and version to the control
        Title = "The NMR Control Program \n Andi Klein"
        Version = "Version 0.1 September 2016"
        
        self.MyTitleLabel = wx.TextCtrl(self.MyPanel, wx.ID_ANY,Title,size = (350,75),style = wx.TE_READONLY|wx.TE_MULTILINE) 
        #self.MyTitleLabel.SetLabelMarkup('big')
        # create a wxfont
        #temp_font=wx.Font(14,wx.FONTFAMILY_SWISS,wx.FONTSTYLE_SLANT,wx.FONTSIZE_XX_LARGE )
        temp_font=wx.Font(14,wx.FONTFAMILY_SWISS,wx.FONTSTYLE_SLANT,wx.FONTWEIGHT_BOLD)
        temp_font.Scale(1.5)
        temp_font.MakeBold()
        self.MyTitleLabel.SetFont(temp_font)        
        self.MyTitleLabel.SetBackgroundColour('Blue')
        self.MyVersion = wx.TextCtrl(self.MyPanel, wx.ID_ANY,Version,size =(350,50),style = wx.TE_READONLY) 
        temp_font.Scale(.9)
        temp_font.SetFamily(wx.FONTFAMILY_TELETYPE)        
        self.MyVersion.SetBackgroundColour('Pink')
        self.MyVersion.SetFont(temp_font)
        self.MySizer.Add(self.MyTitleLabel,pos = (4,6),span=(4,4))
        self.MySizer.Add(self.MyVersion,pos =(8,6),span=(6,4))
        self.MySizer.Add(self.MyFileList,pos=(25,0),span=(10,10))

        
        self.MyPanel.SetSizer(self.MySizer)

        
        

        
        
        
        self.Show()
        self.Fit()
 
        
        # Now bind the actions
        # bind the textinpout on the par file line

#       self.Bind(wx.EVT_RADIOBUTTON,self.OnRunAnalyzer,RunButton)
        self.Bind(wx.EVT_BUTTON,self.OnRunAnalyzer,RunButton)
        self.Bind(wx.EVT_BUTTON,self.OnStopAnalyzer,StopButton)
        self.Bind(wx.EVT_BUTTON,self.OnSaveParameterFile,SaveButton)

        self.Bind(wx.EVT_BUTTON,self.OnRunConverter,RunConverterButton)
         
        self.Bind(wx.EVT_RIGHT_DCLICK,self.OnFileDialogSingle,self.MyFileInput)
        
        self.Bind(wx.EVT_RADIOBUTTON,self.OnFileDialogMultiple,FileButton)
        self.Bind(wx.EVT_ERASE_BACKGROUND, self.OnEraseBackground)  # create background picture                     
        # now the file dialog
      
                         
##########################################                         
                    
         
    def OnExit(self,event):
        """finishing"""
        print "leaving"
        self.Close(True)
        exit()
    
    def OnSaveParameterFile(self,event):
        print "save parameter file"
        self.myC.ParList = self.ParList

        self.myC.WriteParameterFile()       
     
    def OnFilePressedEnter(self,event): 
        temp = event.GetString()
        print" the new filename is" , temp  
        
        
    def OnRunAnalyzer(self,event):
        print "hit run"
        #make sure you get the current parameter list
        for l in range(0,self.counter):
            #print self.MyLabelArray[l].GetValue(),self.MyInputArray[l].GetValue()
            self.ParList[self.MyLabelArray[l].GetValue()] = self.MyInputArray[l].GetValue()
        #self.Destroy()
        
        #check if we have changed anything in parameters
        if(self.ParList == self.ParListOriginal):
            print "nothing has changed"
        else:
            print " we have changes"
        
        # lets get a dialog box, where we can either overwrite the current file or give a new file name
            myDialog = wx.TextEntryDialog(None,'enter filename','test',self.ParFilename,style = wx.OK|wx.CANCEL|wx.RESIZE_BORDER)
            
            if myDialog.ShowModal()           == wx.ID_OK:
                ParFilenam_temp = myDialog.GetValue()
                if(ParFilenam_temp == self.ParFilename):
                    self.myC.ParList = self.ParList
                    self.myC.WriteParameterFile()
                else:
                    self.myC.ParList = self.ParList
                    self.myC.SaveNewParameterFile(ParFilenam_temp)
                    self.ParFilename = ParFilenam_temp
            myDialog.Destroy()  
        
        
        # now create the full command line argument 
        #create one long string out of file list
        arg2 =' '
        for k in range(0,len(self.input_filelist)) :
            arg2=arg2+self.input_filelist[k]+' '
        self.full_command = self.input_directory +'/ ' +arg2+' -f '+ self.ParFilename
        # create a process dialog
        progress = wx.GenericProgressDialog("NMR progress","still analysing",style=wx.PD_ELAPSED_TIME)
        progress.Show()
        
        # need to put this in a separate thread
        NMRFull_command = self.AnaEngineDir+"NMRana"+ ' ' + self.full_command
        #os.system(NMRFull_command)
        
        
        self.RunThread(NMRFull_command)
    
 
        print 'done with root'
        progress.Destroy()
        
        
        
    def OnStopAnalyzer(self,event):
        print "stop run"
 
    def OnRunConverter(self,event):
        """ sets up the machinery for running the converter. This will again use threads and work
        itself through a list of input files."""
        
        
        print " in RunConverter"
        # create an instance of the ControlShort
        ConShort = ControlShort.MySHC()
        #MyShCo = ControlShort.MyShortControl
        print ConShort.MySC.MyFileList
        # loop over input files
        # check that we do not create too many threads
        
 
        
        if (getpass.getuser() =='klein'):
            shell_help = 'export  LD_LIBRARY_PATH = /home/klein/root_all/lib'
        else:
            shell_help = 'export  LD_LIBRARY_PATH = /home/plm/root_all/lib'
        env = dict(os.environ)
        if (getpass.getuser() =='klein'):
            env['LD_LIBRARY_PATH'] = '/home/klein/root_all/lib'
        else:
            env['LD_LIBRARY_PATH'] = '/home/plm/root/lib'
        #the previous is due to the fact that going through an IDE, the environmnet is different
        #it uses the system environment.
        print env['LD_LIBRARY_PATH']," library"
        print env
        
        
        if(len(ConShort.MySC.MyFileList)>5):
                    for k in range(0,len(ConShort.MySC.MyFileList)):
                        
                        
                        
                        
                        
                        arg2 = '-k'+ConShort.MySC.DataDir +'  -i '+ConShort.MySC.MyFileList[k]
                        command = self.RunShortEngineDir +'ReadNMR_short '+arg2 
                        #full_command = shell_help + ' ; '+command
                        
                        print "***************    ",command
                        
                        
                        
                        
                        
                        p = subprocess.Popen(command,shell=True,env=env)   
                        p.wait()
                        #self.RunThread(command)
                        
        else:
            
            for k in range(0,len(ConShort.MySC.MyFileList)):
                arg2 = '-k'+ConShort.MySC.DataDir +'  -i '+ConShort.MySC.MyFileList[k]
                command = self.RunShortEngineDir +'ReadNMR_short '+arg2 
                print "***************    ",command
                self.RunThread(command)

        ConShort.MainLoop()
        ConShort.Destroy()
            
            
            
        

        
        
        
        
           

       
    def OnFileDialogSingle(self,event):
        """ If I hit tab in file input it opens file dialog, selects only one file"""
        wildcard = "*.par|*.*"

        dialog = wx.FileDialog(None, "Choose a file", os.getcwd(), "", wildcard, wx.OPEN)
        if dialog.ShowModal() == wx.ID_OK:
            print dialog.GetPath() 
            self.ParFileName = dialog.GetPath()
        dialog.Destroy()

    def OnFileDialogMultiple(self,event):
        """ If I hit tab in file input it opens file dialog, selects only one file"""
        #make sure not to have spaces in the wildcard definition.
        wildcard = "Root files (*.root)|*.root"

        dialog =wx.DirDialog(None, "Choose an inputdirctory")
        if dialog.ShowModal() == wx.ID_OK:
             
            self.input_directory=dialog.GetPath() 
            directory = self.input_directory 
       

        dialog = wx.FileDialog(None, "Choose an inputfile", directory, "", wildcard, wx.OPEN | wx.MULTIPLE)
        if dialog.ShowModal() == wx.ID_OK:
            dialog.GetPath() 
            #self.input_filelist =[]
            filelist= dialog.GetPaths()
            # the next step is in for historical reasons, the C++ program wants one directory and then all
            # the filenames. So firts I have to strip the directory out again
            
#            print directory,self.input_filelist
            self.input_filelist = []
            self.MyFileList.DeleteAllItems()
            for temp in range(0,len(filelist)):
                self.input_filelist.append(filelist[temp].replace(directory+'/',''))
                print self.input_filelist[temp]
                self.MyFileList.InsertStringItem(temp+1,self.input_filelist[temp])
                #self.MyFileList.SetStringItem()
            # now update list control

                

        dialog.Destroy()
        # now create a litsctrl box with all the files
        
    def OnEraseBackground(self, evt):
        """
        Add a picture to the background
        """
        # yanked from ColourDB.py
        dc = evt.GetDC()
 
        if not dc:
            dc = wx.ClientDC(self)
            rect = self.GetUpdateRegion().GetBox()
            dc.SetClippingRect(rect)
        dc.Clear()
        #load image
        img1 = wx.Image("IMG_0424.jpg",wx.BITMAP_TYPE_JPEG)
        
        #bmp = wx.Bitmap("IMG_0424.jpg")
        #scale to size
         # now scale image
        img2 = img1.Scale(self.panelx,self.panely)
        # create bitmapt
        BitM = wx.BitmapFromImage(img2)
        #print bmp.GetWidth(), ' ' , bmp.GetHeight()
#        bmp.SetSize(size=(w/5.,y/5.))
        dc.DrawBitmap(BitM, 0, 0)       
        

    def RunThread(self,command):
        """ creates the root thread, checks first if there is already one"""
                #run the thread
                
                # check if there is already a thread
        
        
        #create the threads to run
        print "In run command"
        self.NMRthread.append(threading.Thread(target = self.NMRThreadTarget(command) ))
        
        self.NMRthread[self.NMRthreadcount].start()
        self.NMRthreadcount = self.NMRthreadcount+1
        
        print " starting NMR thread"
        return

        
        
         
    def NMRThreadTarget(self,command): 
        """ setting up the firts thread""" 
        if (getpass.getuser() =='klein'):
            shell_help = 'export  LD_LIBRARY_PATH = /home/klein/root_all/lib'
        else:
            shell_help = 'export  LD_LIBRARY_PATH = /home/plm/root/lib'
        full_command = shell_help + ' ; '+command
        env = dict(os.environ)
        if (getpass.getuser() =='klein'):
            env['LD_LIBRARY_PATH'] = '/home/klein/lib'
        else:
            env['LD_LIBRARY_PATH'] = '/home/plm/root/lib'
        #the previous is due to the fact that going through an IDE, the environmnet is different
        #it uses the system environment.
        print env['LD_LIBRARY_PATH']," library"
        print env

        print command

       

        try:
            # setup LD_LIBRARY_PATH
            subprocess.Popen(command,shell=True,env=env)   
            #os.system(self.NMRFull_command)
            #os.system(full_command)
            #subprocess.check_call(self.NMRFull_command, env=env)   
        except:
            print " cannot launch NMR thread"
        return   
            
 ############# the menu items

    def OnHelpGui(self,event):
        """ give help on how to use the Control"""
        #open a panel
        print "help gui"
        MyGH = HelpGUI.MyGuiApp(redirect = False) 
        MyGH.MainLoop()       

        
        pass
 
    def OnHelpAnalyzer(self,event):
        pass
 
    def SetAnaEngineDir(self,dirname):
        """ sts directory where engine is"""
        self.AnaEngineDir = dirname
    def SetRunShortEngineDir(self,dirname):
        """ sts directory where engine is"""
        self.RunShortEngineDir = dirname
            

if __name__ == '__main__':
    
    
    EngineDir = '/home/klein/git/NMRanalyzer/Debug/'
    RunShortEngineDir = '/home/klein/git/NMR_short/ReadNMR_short/Debug/'
    
    #EngineDir = '/home/plm/git/NMRanalyzer/Debug/'
    #RunShortEngineDir = '/home/plm/git/NMR_short/ReadNMR_short/Debug/'
    MyG = MainGUI(redirect = False, filename ="/home/klein/macsmall_disk/nmrwork/NMR_Par/Jan15_coil2_pol.par",
                     EDir = EngineDir, RDir = RunShortEngineDir)
    #MyG = MainGUI(redirect = False )
    print " before loop"
    MyG.MainLoop()
    print "After Loop"        