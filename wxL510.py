#!/usr/bin/env python3
import wx
import wx.dataview
import json

class MainFrame(wx.Frame):
    def __init__(self, *args, **kwds):
        wx.Frame.__init__(self, *args, **kwds)
        self.SetTitle("wxL510")

        # Menu Bar
        self.menubar = wx.MenuBar()
        self.SetMenuBar(self.menubar)

        # Status Bar
        self.statusbar = self.CreateStatusBar(2)
        self.statusbar.SetStatusText('Status left')
        self.statusbar.SetStatusText('Status right', 1)

        # Notebook
        self.notebook = wx.Notebook(self, wx.ID_ANY)

        # "All Parameters" Pane
        self.all_parameters_pane = wx.Panel(self.notebook, wx.ID_ANY)
        self.notebook.AddPage(self.all_parameters_pane, "All Parameters")

        self.all_parameters_ctrl = wx.dataview.TreeListCtrl(self.all_parameters_pane, wx.ID_ANY)

        # Creating columns:
        self.all_parameters_ctrl.AppendColumn("Group")
        self.all_parameters_ctrl.AppendColumn("Number")
        self.all_parameters_ctrl.AppendColumn("Parameter")
        self.all_parameters_ctrl.AppendColumn("Default")
        self.all_parameters_ctrl.AppendColumn("Profile")
        self.all_parameters_ctrl.AppendColumn("VFD")
        self.all_parameters_ctrl.AppendColumn("Unit")

        root = self.all_parameters_ctrl.GetRootItem()

        with open('json/parameters.json') as f:
            parameters = json.load(f)

        for group in parameters.keys():
            group_node = self.all_parameters_ctrl.AppendItem(root, group)
            self.all_parameters_ctrl.SetItemText(group_node, 2, parameters[group]['name'])
            for number in parameters[group].keys():
                print(group,number)
                if number == "name":
                    continue
                number_node = self.all_parameters_ctrl.AppendItem(group_node, number)
                self.all_parameters_ctrl.SetItemText(number_node, 0, '')
                self.all_parameters_ctrl.SetItemText(number_node, 1, number)
                self.all_parameters_ctrl.SetItemText(number_node, 2, parameters[group][number].get('name',''))
                self.all_parameters_ctrl.SetItemText(number_node, 3, parameters[group][number].get('default',''))
                self.all_parameters_ctrl.SetItemText(number_node, 6, parameters[group][number].get('unit',''))

        all_parameters_sizer = wx.BoxSizer(wx.VERTICAL)
        all_parameters_sizer.Add(self.all_parameters_ctrl, 1, wx.EXPAND, 0)
        self.all_parameters_pane.SetSizer(all_parameters_sizer)

        # Parameter Sets Pane
        self.parameter_sets_pane = wx.Panel(self.notebook, wx.ID_ANY)
        self.parameter_sets_ctrl = wx.dataview.TreeListCtrl(self.parameter_sets_pane, wx.ID_ANY)

        # Creating columns:
        self.parameter_sets_ctrl.AppendColumn("Set")
        self.parameter_sets_ctrl.AppendColumn("Group")
        self.parameter_sets_ctrl.AppendColumn("Number")
        self.parameter_sets_ctrl.AppendColumn("Parameter")
        self.parameter_sets_ctrl.AppendColumn("Default")
        self.parameter_sets_ctrl.AppendColumn("Profile")
        self.parameter_sets_ctrl.AppendColumn("VFD")
        self.parameter_sets_ctrl.AppendColumn("Unit")

        root = self.parameter_sets_ctrl.GetRootItem()

        with open('json/parameter_sets.json') as f:
            parameter_sets = json.load(f)

        for set in parameter_sets.keys():
            set_node = self.parameter_sets_ctrl.AppendItem(root, set)
            for group_num in parameter_sets[set]:
                (group,num) = group_num.split('-')
                param_node = self.parameter_sets_ctrl.AppendItem(set_node, '')
                self.parameter_sets_ctrl.SetItemText(param_node, 1, group)
                self.parameter_sets_ctrl.SetItemText(param_node, 2, num)
                self.parameter_sets_ctrl.SetItemText(param_node, 3, parameters[group][num].get('name',''))
                self.parameter_sets_ctrl.SetItemText(param_node, 4, parameters[group][num].get('default',''))
                self.parameter_sets_ctrl.SetItemText(param_node, 7, parameters[group][num].get('unit',''))


        parameter_sets_sizer = wx.BoxSizer(wx.VERTICAL)
        parameter_sets_sizer.Add(self.parameter_sets_ctrl, 1, wx.EXPAND, 0)
        self.parameter_sets_pane.SetSizer(parameter_sets_sizer)
        self.notebook.AddPage(self.parameter_sets_pane, "Parameter Sets")

        self.Layout()
        # end wxGlade

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
