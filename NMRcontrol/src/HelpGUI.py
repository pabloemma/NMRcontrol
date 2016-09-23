'''
Created on Sep 2, 2016

@author: klein
'''
import wx
import wx.html2 as html2
import webbrowser
 



class MyGuiApp(wx.App):
    """ master subclass"""
 
    def OnInit(self):
        """ initializes the application"""
                # instantitae ANA
        
        self.MyHG = MyHelpGUI(None,"helper window")
        self.MyHG.Show()
        print "oninit"
        return True




class MyHelpGUI(wx.Frame):
    '''
    classdocs
    '''
    def __init__ (self,parent,title="Help on GUI"):
        """ creates the parent frame"""

        super(MyHelpGUI,self).__init__(parent,title=title,style=wx.MINIMIZE_BOX | wx.RESIZE_BORDER | wx.CLOSE_BOX)
        
        
        
        self.panel = MyPanel(self)
        self.panel.SetBackgroundColour('Grey')
        
        
        
class MyPanel(wx.Panel):
    def __init__ (self,parent):
        super(MyPanel,self).__init__(parent)
        
        
        self.button = wx.Button(self,label="press me")
        webbrowser.open('file:///Users/klein/git/NMRcontrol1/NMRcontrol/src/help_files/GUI_help.htm')
            
        
 



if __name__ == '__main__':
    MyGH = MyGuiApp(redirect = False) 
    MyGH.MainLoop()       