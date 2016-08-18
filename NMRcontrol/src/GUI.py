'''
Created on Aug 9, 2016

@author: klein
'''
import wx
import AnaControl as ANA
import os
#import images

class RunFrame(wx.Frame):
       def __init__ (self,parent,id,title,parameter_list):
        """ creates the parameters, parameter list is what is contained in parameter file"""
        print "Parameter Frame init"
        wx.Frame.__init__(self,parent,id,title,(300,300),(600,400),style = wx.DEFAULT_FRAME_STYLE)
        self.panel = wx.Panel(self)
        self.panel.SetBackgroundColour('Grey')
 


class ParameterFrame(wx.Frame):
    def __init__ (self,parent,id,title,parameter_list):
        """ creates the parameters, parameter list is what is contained in parameter file"""
        print "Parameter Frame init"
        wx.Frame.__init__(self,parent,id,title,(50,50),(50,400),style = wx.DEFAULT_FRAME_STYLE)
        self.panel = wx.Panel(self)
        self.panel.SetBackgroundColour('Pink')
        self.parameter_list = parameter_list
        




        bmp = wx.ArtProvider.GetBitmap(wx.ART_INFORMATION, wx.ART_OTHER, (16, 16))
        titleIco = wx.StaticBitmap(self.panel, wx.ID_ANY, bmp)
        title = wx.StaticText(self.panel, wx.ID_ANY, 'Parameters')

        
        self.MyIcon = []
        self.MyLabelArray = []
        self.MyInputArray = []
        self.MyLabel = []
        self.MyInput = []
        for k in self.parameter_list:
            self.MyLabel.append(k)
            self.MyInput.append(self.parameter_list[k])
        print "Parameter frame" , self.parameter_list
 
        bmp = wx.ArtProvider.GetBitmap(wx.ART_TIP, wx.ART_OTHER, (16, 16))
        self.counter =0 
        for k in self.parameter_list:
            print k
#            self.MyLabelArray.append(wx.StaticText(self.panel, wx.ID_ANY, k))  # put the variable name from the key
            self.MyLabelArray.append(wx.TextCtrl(self.panel, wx.ID_ANY, k,style = wx.TE_READONLY))  # put the variable name from the key
            self.MyInputArray.append(wx.TextCtrl(self.panel, wx.ID_ANY, self.parameter_list[k],style = wx.TE_PROCESS_ENTER ))
            self.counter = self.counter+1
         

        okBtn = wx.Button(self.panel, wx.ID_ANY, 'OK')
        cancelBtn = wx.Button(self.panel, wx.ID_ANY, 'Cancel')
        self.Bind(wx.EVT_BUTTON, self.onOK, okBtn)
        self.Bind(wx.EVT_BUTTON, self.onCancel, cancelBtn)

        topSizer        = wx.BoxSizer(wx.VERTICAL)
        titleSizer      = wx.BoxSizer(wx.HORIZONTAL)
        # create array of sizer box
        SizerBox =[]
        for l in range(0,self.counter):
            SizerBox.append(wx.BoxSizer(wx.HORIZONTAL))
        btnSizer        = wx.BoxSizer(wx.HORIZONTAL)

        titleSizer.Add(titleIco, 0, wx.ALL, 5)
        titleSizer.Add(title, 0, wx.ALL, 5)
        
        for l in range(0,self.counter):
            SizerBox[l].Add(self.MyLabelArray[l], 0, wx.ALL, 5)
            SizerBox[l].Add(self.MyInputArray[l], 1, wx.ALL|wx.EXPAND, 5)
        


        btnSizer.Add(okBtn, 0, wx.ALL, 5)
        btnSizer.Add(cancelBtn, 0, wx.ALL, 5)

        topSizer.Add(titleSizer, 0, wx.CENTER)
        topSizer.Add(wx.StaticLine(self.panel,), 0, wx.ALL|wx.EXPAND, 5)
        for l in range(0,self.counter):
            topSizer.Add(SizerBox[l], 0, wx.ALL|wx.EXPAND, 5)

        topSizer.Add(wx.StaticLine(self.panel), 0, wx.ALL|wx.EXPAND, 5)
        topSizer.Add(btnSizer, 0, wx.ALL|wx.CENTER, 5)

        self.panel.SetSizer(topSizer)
        topSizer.Fit(self)


    def onOK(self, event):
        # Do something
        # we need to create the parameter list again:
        
        for l in range(0,self.counter):
            #print self.MyLabelArray[l].GetValue(),self.MyInputArray[l].GetValue()
            self.parameter_list[self.MyLabelArray[l].GetValue()] = self.MyInputArray[l].GetValue()
        print 'onOK handler'
        #print self.parameter_list
        self.Destroy()
        return self.parameter_list

    def onCancel(self, event):
        self.Destroy()
        return 0

    def closeProgram(self):
        self.Close()
        
        
         
        
    def onAction(self, event, argument,arg2):
        """
        check for numeric entry and limit to 2 decimals
        accepted result is in self.value
        """
        print "onAction",arg2
        raw_value = argument.GetValue().strip()
        print raw_value,arg2
        # numeric check
        if all(x in '0123456789.+-' for x in raw_value):
            # convert to float and limit to 2 decimals
            self.value = round(float(raw_value), 2)
            argument.ChangeValue(str(self.value))
        else:
            argument.ChangeValue("Number only")
            
        #argument.SetValue("5.3")
        
        


class MyFrame(wx.Frame):
    """ This is the main control frame """
    def __init__ (self,parent,id,title,parlist):
        print "Frame init"
        wx.Frame.__init__(self,parent,id,title,(100,100),(600,400),style = wx.DEFAULT_FRAME_STYLE)
        
        panel = wx.Panel(self)
        panel.SetBackgroundColour('Blue')
        statusBar = self.CreateStatusBar()
        toolbar = self.CreateToolBar()
        self.ParList = parlist
        #self.ParList = ParList
        
        
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
        
        self.MyParFrame = ParameterFrame(parent=None,id = -1,title= "Set Parameters",parameter_list =self.ParList)  # open a parameter frame
        self.MyParFrame.Show()
        
        
        
        
        return  # on save or close or whatever
        print "setparameters"
        
        
        
    def OnRunAnalyzer(self,event):
        self.MyRunFrame = RunFrame(parent=None,id = -1,title= "Run Control",parameter_list =self.ParList)  # open a parameter frame
        wildcard = "Python source (*.py)|*.py|" 
        "Compiled Python (*.pyc)|*.pyc|" \
        "All files (*.*)|*.*"
        dialog = wx.FileDialog(None, "Choose a file", os.getcwd(), "", wildcard, wx.OPEN)
        if dialog.ShowModal() == wx.ID_OK:
            print dialog.GetPath() 

        dialog.Destroy()

        self.MyRunFrame.Show()
        print "run analyzer"

    

        
class MyGUIapp(wx.App):
    """ master subclass"""
    def __init__(self,redirect=True, filename=None):
        wx.App.__init__(self,redirect,filename)
       
    def OnInit(self):
        """ initializes the application"""
                # instantitae ANA
        myC = ANA.myControl()
        self.ParList = myC.ReadParameterFile()
        print "Gui", self.ParList
        
        
        #myC.WriteParameterFile()
        #myC.CreateNMRAna()
        #myC.Cleanup()

        self.frame = MyFrame(parent=None,id = -1,title= "NMR control",parlist = self.ParList)
        
        
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