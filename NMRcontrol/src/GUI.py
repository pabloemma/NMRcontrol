'''
Created on Aug 9, 2016

@author: klein
'''
import wx
#import images

class ParameterFrame(wx.Frame):
    def __init__ (self,parent,id,title):
        print "Parameter Frame init"
        wx.Frame.__init__(self,parent,id,title,(300,300),(600,400),style = wx.DEFAULT_FRAME_STYLE)
        panel = wx.Panel(self)
        panel.SetBackgroundColour('Pink')
        
        


class MyFrame(wx.Frame):
    """ This is the main control frame """
    def __init__ (self,parent,id,title):
        print "Frame init"
        wx.Frame.__init__(self,parent,id,title,(100,100),(600,400),style = wx.DEFAULT_FRAME_STYLE)
        
        panel = wx.Panel(self)
        panel.SetBackgroundColour('Blue')
        statusBar = self.CreateStatusBar()
        toolbar = self.CreateToolBar()
        
        
       #toolbar.AddSimpleTool(wx.NewId(), images.getNewBitmap(),"New","long help for 'New'")
        menuBar = wx.MenuBar()  # Create the menu bar
        menu1 = wx.Menu()  

        menuitem1 = menu1.Append(wx.NewId(),"Q&uit","Leave Dodge")
        menuBar.Append(menu1, "&File") # add this submenu to the menu bar

        
        menuControl = wx.Menu()  #this is the control menu

        menuCont1 = menuControl.Append(wx.NewId(),"S&et Parameters","choose run parameters") # the commands are (id, menu item, what is whown with mouse over)

        
        menuCont2 = menuControl.Append(wx.NewId(),"Go","Run the NMRanalyzer")

        menuBar.Append(menuControl,"Control")


            #binding the action to the menus
        self.Bind(wx.EVT_MENU,self.OnExit,menuitem1) # bind action to menu item       
        self.Bind(wx.EVT_MENU,self.OnSetParameters,menuCont1)
        self.Bind(wx.EVT_MENU,self.OnRunAnalyzer,menuCont2)


        self.SetMenuBar(menuBar)
        
        #Event Handlers
        
    def OnExit(self,event):
        """finishing"""
        print "leaving"
        self.Close(True)
    
    def OnSetParameters(self,event):
        """this will read or display the current parameters in a display window
        the user can then change the values of these parameters. Once this is finished
        the parameters are save to file and the loop is exited"""
        
        self.MyParFrame = ParameterFrame(parent=None,id = -1,title= "Set Parameters")  # open a parameter frame
        self.MyParFrame.Show()
        
        
        return  # on save or close or whatever
        print "setparameters"
        
        
        
    def OnRunAnalyzer(self,event):
        print "run analyzer"


        
class MyGUIapp(wx.App):
    """ master subclass"""
    def __init__(self,redirect=True, filename=None):
        wx.App.__init__(self,redirect,filename)
        
    def OnInit(self):
        """ initializes the application"""
        self.frame = MyFrame(parent=None,id = -1,title= "NMR control")
        self.frame.Show()
        # make this the topwindow
        self.SetTopWindow(self.frame)
        print "I am in OnInit"
        # temporarya dialog

        
        
        
        dlg = wx.MessageDialog(None,'Continue','Dialog',wx.YES_NO |wx.ICON_QUESTION)
        result = dlg.ShowModal()
        dlg.Destroy()
        return True
    
    def OnExit(self):
        print" OnExit"
        
        
    



if __name__ == '__main__':
    MyG = MyGUIapp(redirect = False)
    print " before loop"
    MyG.MainLoop()
    print "After Loop"