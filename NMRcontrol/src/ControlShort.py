'''
Created on Oct 27, 2016

@author: Andi Klein
'''
import wx
import os
import platform



class MySHC(wx.App):
    """ master subclass"""
 
    def OnInit(self):
        """ initializes the application"""
                # instantitae ANA
        
        self.MySC = MyShortControl(None,"Short Control Window")
        self.MySC.Show()
        print "oninit"
        return True








class MyShortControl(wx.Frame):
    '''
    Creates all the necessary oclass MyGuiApp(wx.App):
    """ master subclass"""
 
    def OnInit(self):
        """ initializes the application"""
                # instantitae ANA
        
        self.MyHG = MyHelpGUI(None,"helper window")
        self.MyHG.Show()
        print "oninit"
        return True
verhead to run NMR_short
    Again I am using python and wxpyton as a setup environmnet
    which ultimately will run a C++ engine.
    '''
    def __init__ (self,parent,title="NMR_short Control"):
        """ creates the parent frame"""

        super(MyShortControl,self).__init__(parent,title=title,style=wx.MINIMIZE_BOX | wx.RESIZE_BORDER | wx.CLOSE_BOX)
        # self.Center() puts panel into the center
        if platform.system == "Darwin":
            print" we are on OSX"
            self.OS = 'OSX'
        else:
            self.OS = 'Linux'
        
        #Get screen coordinates
        w = wx.SystemSettings.GetMetric(wx.SYS_SCREEN_X)
        h = wx.SystemSettings.GetMetric(wx.SYS_SCREEN_Y)
        # set width and height of panel
        print w,h
        pan_width  = 400
        pan_height = 600
        #want to set position of panel in right upper CORNER_
        posx = w-pan_width
        posy = 100
        
        #choose input driectory
        dlg1 = wx.DirDialog(None,"Data Directory",style=wx.VSCROLL | wx.HSCROLL)
        if self.OS == 'OSX' :
            dlg1.ShowModal() #there is an inconsitency between OSX and Linux when it comes to file and dir dialog
        
        if dlg1.ShowModal() == wx.ID_OK:
            self.DataDir = dlg1.GetPath()
            dlg1.Destroy()
                
    
        # now check if the root directory below exists
        self.CheckDirectory()
        # add fw slash
        self.DataDir = self.DataDir+'/'
        
        # now get the input files
        
        
        dialog = wx.FileDialog(None, "Choose an inputfile", self.DataDir,"", "*.csv",style = wx.OPEN | wx.MULTIPLE)
        if dialog.ShowModal() == wx.ID_OK:
            dialog.GetPath() 
            #self.input_filelist =[]
            MyFiles = dialog.GetFilenames()
            
        self.MyFileList=[]
        # now strip the ending 
        for k in range(0,len(MyFiles)):
            self.MyFileList.append( MyFiles[k].replace('.csv',''))
            
        print self.MyFileList
        
        
        
        #now we can run the NMR short with all these files.
        # I just loop ver the command
    
    
         
        
        
        
        
        
        self.panel = MyControlPanel(self)
        print posx,posy
        self.panel.Center()
        self.panel.SetBackgroundColour('grey')
        #create a list control
        self.list_ctrl = wx.ListCtrl(self.panel, size=(-1,100),
                         style=wx.LC_REPORT | wx.VSCROLL|
                         wx.BORDER_SUNKEN
                         )
        self.list_ctrl.InsertColumn(0, 'Filename')
        self.list_ctrl.InsertColumn(1, 'Number?')
        self.index=0
        # add lines to list control in column 0
        for k in range(0,len(self.MyFileList)):
            self.list_ctrl.InsertStringItem(self.index,self.MyFileList[k])
            self.index  += 1
        
        # change column width
        self.list_ctrl.SetColumnWidth(0,wx.LIST_AUTOSIZE)

            
        
        
        
        
        
        
        
        
        self.panel.Show()
    
    def CheckDirectory(self):   
        """ this routine checks if the data dir exists
        if not it creates the directory"""
        temp_dir = self.DataDir + "/root"
        if not os.path.exists(temp_dir):
            print "root directory does not exist, create ", temp_dir
            # now create this directory:
            os.makedirs(temp_dir)
        
        
        
     
        
        
        
class MyControlPanel(wx.Panel):
    def __init__ (self,parent):
        super(MyControlPanel,self).__init__(parent)
        








  
  
  
if __name__ == '__main__':
    MySC = MySHC(redirect = False) 
    MySC.MainLoop()
            