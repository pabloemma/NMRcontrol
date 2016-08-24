'''
Created on Aug 24, 2016

@author: klein
'''

import wx



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
        
        