import wx


class SizeDialog(wx.Dialog):
    def __init__(self, parent, id, title):
        wx.Dialog.__init__(self, parent, id, title, size=(300, 175))

        mainbox = wx.BoxSizer(wx.VERTICAL)
        vbox = wx.BoxSizer(wx.VERTICAL)
        textbox = wx.BoxSizer(wx.HORIZONTAL)
        hbox = wx.BoxSizer(wx.HORIZONTAL)
        text1 = "Enter in a custom size (> 0 accepted)"
        msg = wx.StaticText(self, -1, text1, (30,15), style=wx.ALIGN_CENTRE)
        msg.SetLabel(text1)
        self.myTxtCtrl = wx.TextCtrl(self, -1, '', (100, 50))
        
        textbox.Add(self.myTxtCtrl, flag=wx.LEFT|wx.RIGHT|wx.ADJUST_MINSIZE,
                 border=10)
        vbox.Add(msg, flag=wx.ALL, border=10, proportion=1)
        vbox.Add(textbox, flag=wx.EXPAND|wx.TOP|wx.BOTTOM|wx.ADJUST_MINSIZE,
                 border=10)
        self.myTxtCtrl.SetValue(str(5))
        
        okButton = wx.Button(self, wx.ID_OK, 'OK', size=(70, 25))
        closeButton = wx.Button(self, wx.ID_CANCEL, 'Cancel', size=(70, 25))

        hbox.Add(okButton)
        hbox.Add((20, 20))
        hbox.Add(closeButton)
        
        mainbox.Add(vbox, flag=wx.ALL, border=10)
        mainbox.Add(wx.StaticLine(self), 0, wx.ALL|wx.EXPAND, 5)
        mainbox.Add(hbox, flag=wx.CENTER,
                    border=10)
        self.SetSizer(mainbox)
    
    def getText(self):
        """
        Get text typed
        """
        return self.myTxtCtrl.GetValue()
