'''
Created on Aug 17, 2016

@author: klein
'''
import wx
import os
import AnaControl as ANA
import NMR
#import ParFrame as PF










class MainGUI(wx.App):
    '''
    This is the top application controlling things
    '''
    def __init__ (self,redirect=True, filename=None):
        """ creates the parameters, parameter list is what is contained in parameter file"""
        print "Parameter Frame init"
        self.ParFilename = filename
        wx.App.__init__(self,redirect,filename)


    def OnInit(self): 
        myC = ANA.myControl("/Users/klein/git/NMRanalyzer/parameterfiles/test_april25_noQcurve.par")
        self.ParList = myC.ReadParameterFile()
        print "Gui", self.ParList
        self.frame = MyFrame(parent=None,id=-1,title= "NMR control",parlist = self.ParList, filename = self.ParFilename)
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
    def __init__ (self,parent,id,title,parlist, filename):
        print "Frame init"
        #
        wx.Frame.__init__(self,parent,id,title,pos = (100,100),size = (1200,800),style = wx.DEFAULT_FRAME_STYLE)
        # determine the parent Id so that we can place parameter panel into main panel (hopefully)
        self.MyPanel = wx.Panel(self)
        
        #Instantiate my control
        self.myC = ANA.myControl("/Users/klein/git/NMRanalyzer/parameterfiles/test_april25_noQcurve.par")
        self.myANA = NMR.NMR() #instantiate the engie

        # create a background color
        MyColor =wx.Colour(240)
        MyColorF =wx.Colour(240-50)
        #self.MyPanel.SetBackgroundColour(MyColor)
        self.MyPanel.SetForegroundColour(MyColorF)
        
        
        self.MyStatusBar = self.CreateStatusBar()
        self.MyToolBar = self.CreateToolBar()
        self.ParList = parlist
        self.ParFileName = filename
        
        # now create the sizer
        self.PanelLayout()
        

        self.MyPanel.Show()
        #self.ParList = ParList
        
    def PanelLayout(self): 
        """ this lays out the control panel 
        using sizers"""
        
        # create a grid bag sizer
        self.MySizer = wx.GridBagSizer( hgap = 3, vgap =3)
        
        # currently add two things, namely the file diaolog and the run button
        
        
        #Display filename turns out I need to define the size in the tex ctrl box
        self.MyFileLabel = wx.TextCtrl(self.MyPanel, wx.ID_ANY,"Parameter File",size =(100,25),style = wx.TE_READONLY)  # put the variable name from the key
        self.MyFileInput = wx.TextCtrl(self.MyPanel, wx.ID_ANY,self.ParFileName ,size=(500,25),style = wx.TE_PROCESS_ENTER|wx.TE_AUTO_SCROLL | wx.TE_PROCESS_TAB)

        #bind textctrl to right click
        self.MyFileInput.Bind(wx.EVT_RIGHT_DOWN, self.OnFileDialogSingle) 

        #self.MyFileInput.Bind(wx.EVT_SET_FOCUS, self.OnFileDialog) 

        
        
        self.MySizer.Add(self.MyFileLabel,pos = (0,0),span=(1,4))
        self.MySizer.Add(self.MyFileInput,pos = (0,4),span=(1,10))
        self.MySizer.AddGrowableCol(4, 10) # make colum4 growable
 
        self.MyInputFileLabel = wx.TextCtrl(self.MyPanel, wx.ID_ANY,"InputFile",size =(100,25),style = wx.TE_READONLY)  # put the variable name from the key
        self.MySizer.Add(self.MyInputFileLabel,pos = (1,0),span=(1,4))
        # bind to rght click
        #self.MyInputFileLabel.Bind(wx.EVT_RIGHT_DOWN, self.OnFileDialogMultiple) 
        FileButton = wx.RadioButton(self.MyPanel,-1,"Choose")
        self.MySizer.Add(FileButton,pos = (1,4))
    
        
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
        for k in self.ParList:
            print k
#            self.MyLabelArray.append(wx.StaticText(self.panel, wx.ID_ANY, k))  # put the variable name from the key
            self.MyLabelArray.append(wx.TextCtrl(self.MyPanel, wx.ID_ANY, k,style = wx.TE_READONLY))  # put the variable name from the key
            self.MyInputArray.append(wx.TextCtrl(self.MyPanel, wx.ID_ANY, self.ParList[k],style = wx.TE_PROCESS_ENTER ))
            print self.counter+2
            self.MyLabelArray[self.counter].SetBackgroundColour('Yellow')
            self.MySizer.Add(self.MyLabelArray[self.counter], pos=(3+self.counter,0),span=(1,4))
            self.MySizer.Add(self.MyInputArray[self.counter], pos=(3+self.counter,4),span=(1,4))
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
          
        
        #do the parametre list with independent window, but then give the parameters in boxes on main control
        
         
        # file list
        self.MyFileList=wx.ListCtrl(self.MyPanel, wx.ID_ANY,pos=(600,300),size=(400,800))

        
        # add the title and version to the control
        Title = "The NMR Control Program \n Andi Klein"
        Version = "Version 0.1 September 2016"
        
        self.MyTitleLabel = wx.TextCtrl(self.MyPanel, wx.ID_ANY,Title,size = (350,75),style = wx.TE_READONLY|wx.TE_MULTILINE) 
        #self.MyTitleLabel.SetLabelMarkup('big')
        # create a wxfont
        temp_font=wx.Font(15,wx.FONTFAMILY_SWISS,wx.FONTSTYLE_SLANT,wx.FONTSIZE_XX_LARGE )
        temp_font.Scale(1.5)
        temp_font.MakeBold()
        self.MyTitleLabel.SetFont(temp_font)        
        self.MyTitleLabel.SetBackgroundColour('Blue')
        self.MyVersion = wx.TextCtrl(self.MyPanel, wx.ID_ANY,Version,size =(300,50),style = wx.TE_READONLY) 
        temp_font.Scale(.9)
        temp_font.SetFamily(wx.FONTFAMILY_TELETYPE)        
        self.MyVersion.SetBackgroundColour('Pink')
        self.MyVersion.SetFont(temp_font)
        self.MySizer.Add(self.MyTitleLabel,pos = (4,10),span=(3,1))
        self.MySizer.Add(self.MyVersion,pos =(8,10),span=(6,4))
        self.MySizer.Add(self.MyFileList,pos=(20,8))
        self.SetSizerAndFit(self.MySizer)

        
        
        self.Show()

        
        
        
        self.Fit()
        
        # Now bind the actions

 #       self.Bind(wx.EVT_RADIOBUTTON,self.OnRunAnalyzer,RunButton)
        self.Bind(wx.EVT_BUTTON,self.OnRunAnalyzer,RunButton)
        self.Bind(wx.EVT_BUTTON,self.OnStopAnalyzer,StopButton)
        
        self.Bind(wx.EVT_RIGHT_DCLICK,self.OnFileDialogSingle,self.MyFileInput)
        
        self.Bind(wx.EVT_RADIOBUTTON,self.OnFileDialogMultiple,FileButton)
        self.Bind(wx.EVT_ERASE_BACKGROUND, self.OnEraseBackground)  # create background picture                     
        # now the file dialog
        
                         
##########################################                         
                    
         
    def OnExit(self,event):
        """finishing"""
        print "leaving"
        self.Close(True)
    

    def OnRunAnalyzer(self,event):
        print "hit run"
        #make sure you get the current parameter list
        for l in range(0,self.counter):
            #print self.MyLabelArray[l].GetValue(),self.MyInputArray[l].GetValue()
            self.ParList[self.MyLabelArray[l].GetValue()] = self.MyInputArray[l].GetValue()
        #self.Destroy()
        
        #Now push the parameter list back to the Control Program and write them there
        self.myC.ParList = self.ParList
        self.myC.WriteParameterFile()
        # now create the full command line argument 
        #create one long string out of file list
        arg2 =' '
        for k in range(0,len(self.input_filelist)) :
            arg2=arg2+self.input_filelist[k]+' '
        self.full_command = self.input_directory +'/ ' +arg2+' -f '+ self.ParFileName
        # create a process dialog
        progress = wx.GenericProgressDialog("NMR progress","still analysing",style=wx.PD_ELAPSED_TIME)
        progress.Show()
        
        # need to put this in a separate thread
        Full_command = "/Users/klein/git/NMRanalyzer/Debug/NMRana"+ ' ' + self.full_command
        os.system(Full_command)
 
        print 'done with root'
        progress.Destroy()
        
        
        
    def OnStopAnalyzer(self,event):
        print "stop run"
 
        

       
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
            self.input_filelist =[]
            filelist = dialog.GetPaths()
            # the next step is in for historical reasons, the C++ program wants one directory and then all
            # the filenames. So firts I have to strip the directory out again
            print directory,self.input_filelist
            for temp in range(0,len(filelist)):
                self.input_filelist.append(filelist[temp].replace(directory+'/',''))
                print self.input_filelist[temp]
                self.MyFileList.InsertItem(self.input_filelist[temp])
                

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
        bmp = wx.Bitmap("IMG_0424.jpg")
        dc.DrawBitmap(bmp, 0, 0)       
        
        
         

if __name__ == '__main__':
    MyG = MainGUI(redirect = False, filename ="/Users/klein/git/NMRanalyzer/parameterfiles/test_april25_noQcurve.par" )
    print " before loop"
    MyG.MainLoop()
    print "After Loop"        