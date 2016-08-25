'''
Created on Aug 17, 2016

@author: klein
'''
import wx
import os
import AnaControl as ANA
import ParFrame as PF










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
        myC = ANA.myControl()
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
        self.MyPanel.SetBackgroundColour('Grey')
        
        
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
        
        
        RunButton = wx.RadioButton(self.MyPanel,-1,"Run")
        self.MySizer.Add(RunButton,pos = (10,1))
        
        
        
        
        
        #do the parametre list with independent window, but then give the parameters in boxes on main control
        
        # now get the parameters in
        #self.ParF = PF.ParameterFrame(parent=None,id = -1,title= "Parameters",parameter_list = self.ParList)
        self.ParF = PF.ParameterFrame(parent=self.MyPanel,id = -1,title= "Parameters",parameter_list = self.ParList)
        ## put the parameter frame into the sizer
        self.MySizer.Add(self.ParF,(1,5))
        #self.MySizer.Add(self.ParF.panel,pos = (1,5),span=(8,12))
  #      print self.ParF.MyLabel
        
        
        self.SetSizerAndFit(self.MySizer)
        self.Show()
        
        
        
        
        self.Fit()
        
        # Now bind the actions

        self.Bind(wx.EVT_RADIOBUTTON,self.OnRunAnalyzer,RunButton)
        
        self.Bind(wx.EVT_RIGHT_DCLICK,self.OnFileDialogSingle,self.MyFileInput)
        
        self.Bind(wx.EVT_RADIOBUTTON,self.OnFileDialogMultiple,FileButton)
                        
        # now the file dialog
        
                         
##########################################                         
                    
         
    def OnExit(self,event):
        """finishing"""
        print "leaving"
        self.Close(True)
    

    def OnRunAnalyzer(self,event):
        print "hit run"
        pass
       
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

        dialog = wx.FileDialog(None, "Choose an inputfile", os.getcwd(), "", wildcard, wx.OPEN | wx.MULTIPLE)
        if dialog.ShowModal() == wx.ID_OK:
            dialog.GetPath() 
            self.input_filelist = dialog.GetPaths()
            print self.input_filelist

        dialog.Destroy()
        
        
        
         

if __name__ == '__main__':
    MyG = MainGUI(redirect = False, filename ="/Users/klein/git/NMRanalyzer/parameterfiles/test_april25_noQcurve.par" )
    print " before loop"
    MyG.MainLoop()
    print "After Loop"        