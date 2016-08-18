'''
Created on Aug 17, 2016

@author: klein
'''
import wx
import os
import AnaControl as ANA










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
        self.frame = MyFrame(parent=None,id = -1,title= "NMR control",parlist = self.ParList, filename = self.ParFilename)
        
        
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
        wx.Frame.__init__(self,parent,id,title,pos = (100,100),size = (1200,800),style = wx.DEFAULT_FRAME_STYLE)
        
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
        self.MyFileInput.Bind(wx.EVT_RIGHT_DOWN, self.OnFileDialog) 

        #self.MyFileInput.Bind(wx.EVT_SET_FOCUS, self.OnFileDialog) 

        
        
        self.MySizer.Add(self.MyFileLabel,pos = (0,0),span=(1,4))
        self.MySizer.Add(self.MyFileInput,pos = (0,4),span=(1,10))
        self.MySizer.AddGrowableCol(4, 10) # make colum4 growable
 
        
        
        # create the run button
        
        
        RunButton = wx.RadioButton(self.MyPanel,-1,"Run")
        self.MySizer.Add(RunButton,pos = (10,1))
        self.SetSizer(self.MySizer)
        
        
        
        
        self.Fit()
        
        # Now bind the actions

        self.Bind(wx.EVT_RADIOBUTTON,self.OnRunAnalyzer,RunButton)
        self.Bind(wx.EVT_RIGHT_DCLICK,self.OnFileDialog,self.MyFileInput)
        
                         
        # now the file dialog
        
                         
##########################################                         
                    
         
    def OnExit(self,event):
        """finishing"""
        print "leaving"
        self.Close(True)
    

    def OnRunAnalyzer(self,event):
        print "hit run"
        pass
       
    def OnFileDialog(self,event):
        """ If I hit tab in file input it opens file dialog"""
        wildcard = "*.par |*.*"

        dialog = wx.FileDialog(None, "Choose a file", os.getcwd(), "", wildcard, wx.OPEN)
        if dialog.ShowModal() == wx.ID_OK:
            print dialog.GetPath() 

        dialog.Destroy()

        
 

if __name__ == '__main__':
    MyG = MainGUI(redirect = False, filename ="/Users/klein/git/NMRanalyzer/parameterfiles/test_april25_noQcurve.par" )
    print " before loop"
    MyG.MainLoop()
    print "After Loop"        