#!/usr/bin/env python3
import wx
import wx.dataview

from vfd import VFD

class MainFrame(wx.Frame):
    def __init__(self, *args, **kwds):
        wx.Frame.__init__(self, *args, **kwds)
        self.SetTitle("wxL510")

        # File Menu
        filemenu = wx.Menu()
        menuAbout = filemenu.Append(wx.ID_ABOUT)
        self.Bind(wx.EVT_MENU, self.OnAbout, menuAbout)
        menuExit = filemenu.Append(wx.ID_EXIT)
        self.Bind(wx.EVT_MENU, self.OnExit, menuExit)

        # VFD Menu
        vfdmenu = wx.Menu()
        menuConnect = vfdmenu.Append(wx.ID_YES, "&Connect")
        self.Bind(wx.EVT_MENU, self.OnConnect, menuConnect)
        menuDisconnect = vfdmenu.Append(wx.ID_NO, "&Disconnect")
        self.Bind(wx.EVT_MENU, self.OnDisconnect, menuDisconnect)

        # Menu Bar
        menubar = wx.MenuBar()
        menubar.Append(filemenu, "&File")
        menubar.Append(vfdmenu, "&VFD")
        self.SetMenuBar(menubar)

        # Status Bar
        self.statusbar = self.CreateStatusBar(2)
        self.statusbar.SetStatusText('Disconnected from VFD')
        self.statusbar.SetStatusText('Status right', 1)

        # Initialize the VFD Object
        self.vfd = VFD('/dev/ttyUSB0',1)

        # Notebook
        self.notebook = wx.Notebook(self, wx.ID_ANY)

        # "All Parameters" Pane
        self.all_parameters_pane = wx.Panel(self.notebook, wx.ID_ANY)
        self.notebook.AddPage(self.all_parameters_pane, "All Parameters")

        self.all_parameters_ctrl = wx.dataview.TreeListCtrl(self.all_parameters_pane, wx.ID_ANY)

        self.all_parameters_ctrl.AppendColumn("Group")
        self.all_parameters_ctrl.AppendColumn("Number")
        self.all_parameters_ctrl.AppendColumn("Parameter")
        self.all_parameters_ctrl.AppendColumn("Default")
        self.all_parameters_ctrl.AppendColumn("Profile")
        self.all_parameters_ctrl.AppendColumn("VFD")
        self.all_parameters_ctrl.AppendColumn("Unit")

        root = self.all_parameters_ctrl.GetRootItem()

        for group in self.vfd.config.groups:
            group_node = self.all_parameters_ctrl.AppendItem(root, group.num)
            self.all_parameters_ctrl.SetItemText(group_node, 2, group.name)
            for parameter in group.parameters:
                 parameter_node = self.all_parameters_ctrl.AppendItem(group_node, parameter.num)
                 self.all_parameters_ctrl.SetItemText(parameter_node, 0, '')
                 self.all_parameters_ctrl.SetItemText(parameter_node, 1, parameter.num)
                 self.all_parameters_ctrl.SetItemText(parameter_node, 2, parameter.name)
                 self.all_parameters_ctrl.SetItemText(parameter_node, 3, parameter.default)
                 self.all_parameters_ctrl.SetItemText(parameter_node, 6, parameter.unit)

        all_parameters_sizer = wx.BoxSizer(wx.VERTICAL)
        all_parameters_sizer.Add(self.all_parameters_ctrl, 1, wx.EXPAND, 0)
        self.all_parameters_pane.SetSizer(all_parameters_sizer)

        # Parameter Sets Pane
        self.parameter_sets_pane = wx.Panel(self.notebook, wx.ID_ANY)
        self.parameter_sets_ctrl = wx.dataview.TreeListCtrl(self.parameter_sets_pane, wx.ID_ANY)

        self.parameter_sets_ctrl.AppendColumn("Set")
        self.parameter_sets_ctrl.AppendColumn("Group")
        self.parameter_sets_ctrl.AppendColumn("Number")
        self.parameter_sets_ctrl.AppendColumn("Parameter")
        self.parameter_sets_ctrl.AppendColumn("Default")
        self.parameter_sets_ctrl.AppendColumn("Profile")
        self.parameter_sets_ctrl.AppendColumn("VFD")
        self.parameter_sets_ctrl.AppendColumn("Unit")

        root = self.parameter_sets_ctrl.GetRootItem()

        for set in self.vfd.config.sets:
            set_node = self.parameter_sets_ctrl.AppendItem(root, set.name)
            for parameter in set.parameters:
                param_node = self.parameter_sets_ctrl.AppendItem(set_node, '')
                self.parameter_sets_ctrl.SetItemText(param_node, 1, parameter.group.num)
                self.parameter_sets_ctrl.SetItemText(param_node, 2, parameter.num)
                self.parameter_sets_ctrl.SetItemText(param_node, 3, parameter.name)
                self.parameter_sets_ctrl.SetItemText(param_node, 4, parameter.default)
                self.parameter_sets_ctrl.SetItemText(param_node, 7, parameter.unit)

        parameter_sets_sizer = wx.BoxSizer(wx.VERTICAL)
        parameter_sets_sizer.Add(self.parameter_sets_ctrl, 1, wx.EXPAND, 0)
        self.parameter_sets_pane.SetSizer(parameter_sets_sizer)
        self.notebook.AddPage(self.parameter_sets_pane, "Parameter Sets")

        self.Layout()

    def OnConnect(self, e):
        self.statusbar.SetStatusText('Connecting to VFD...')
        if self.vfd.connect():
            self.statusbar.SetStatusText('Loading parameters from VFD...')
            group_item = self.all_parameters_ctrl.GetFirstItem()
            while group_item.IsOk():
                print("group_num:", self.all_parameters_ctrl.GetItemText(group_item, 0))
                group = self.vfd.config.group(self.all_parameters_ctrl.GetItemText(group_item, 0))
                self.statusbar.SetStatusText('Loading ' + group.name, 1)
                param_item = self.all_parameters_ctrl.GetFirstChild(group_item)
                while param_item.IsOk():
                    parameter = group.parameter(self.all_parameters_ctrl.GetItemText(param_item, 1))
                    self.all_parameters_ctrl.SetItemText(param_item, 5, str(self.vfd.parameter(parameter)))
                    param_item = self.all_parameters_ctrl.GetNextSibling(param_item)
                group_item = self.all_parameters_ctrl.GetNextSibling(group_item)
            self.statusbar.SetStatusText('', 1)

            item = self.parameter_sets_ctrl.GetFirstItem()
            while item.IsOk():
                group = self.vfd.config.group(self.parameter_sets_ctrl.GetItemText(item, 1))
                if group:
                    parameter = group.parameter(self.parameter_sets_ctrl.GetItemText(item, 2))
                    if parameter:
                        self.parameter_sets_ctrl.SetItemText(item, 6, str(self.vfd.parameter(parameter)))
                item = self.parameter_sets_ctrl.GetNextItem(item)
            self.statusbar.SetStatusText('Connected to VFD')
        else:
            self.statusbar.SetStatusText('VFD Connection Failed')

    def OnDisconnect(self, e):
        self.vfd.disconnect()
        self.statusbar.SetStatusText('Disconnected from VFD')

    def OnAbout(self, e):
        dialog = wx.MessageDialog(self, "A simple interface to the Teco-Westinghouse L510 VFD.", "About wxL510")
        dialog.ShowModal()
        dialog.Destroy()

    def OnExit(self, e):
        self.Close(True)

# end of class MainFrame

class MyApp(wx.App):
    def OnInit(self):
        self.frame = MainFrame(None, wx.ID_ANY, "")
        self.SetTopWindow(self.frame)
        self.frame.Show()
        return True

# end of class MyApp

if __name__ == "__main__":
    app = MyApp(0)
    app.MainLoop()
