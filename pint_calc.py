# -*- coding: utf-8 -*-
"""
Units-converter using pint and wxwidgets

Created on Mon Sep 07 13:40:14 2015

@author: Hannes
"""

import wx
import pint

nasty_units = False
TITLE = "Have a pint."


class wxPintCalc(wx.Frame):
    """
    Unit conversion calculator.
    """

    def __init__(self, debug=False):
        """
        Create (and Show) this Frame, a main panel/sizer, and the status icons
        If debug is True, print logging info
        """
        super(wxPintCalc, self).__init__(None, wx.ID_ANY, title=TITLE)
        self.debug = debug

        # defaults
        self.quantity = unit.meter
        self.conv_quantity = self.quantity.to("kilometer")

        self.init_UI()
        self.Show()

    @property
    def magnitude(self):
        return self.quantity.magnitude

    @property
    def units(self):
        return self.quantity.units

    @property
    def conv_magnitude(self):
        return self.conv_quantity.magnitude

    @property
    def conv_units(self):
        return self.conv_quantity.units

    def init_UI(self):
        self.init_panel()
        self.init_sizer()

    def init_panel(self):
        self.panel = wx.Panel(self, wx.ID_ANY)

    def init_sizer(self):
        sizer = wx.FlexGridSizer(rows=3, cols=3)

        empty_txt = wx.StaticText(self.panel, label="")
        magnitude_txt = wx.StaticText(self.panel, label="Magnitude")
        unit_txt = wx.StaticText(self.panel, label="Unit")
        in_txt = wx.StaticText(self.panel, label="Input")
        out_txt = wx.StaticText(self.panel, label="Output")

        mag_c = wx.TextCtrl(self.panel, name='mag_c')
        mag_c.SetValue(str(self.magnitude))
        mag_c.Bind(wx.EVT_TEXT, self.magnitude_input)

        unit_c = wx.TextCtrl(self.panel, name='unit_c',
                             style=wx.TE_PROCESS_ENTER)
        unit_c.SetValue(str(self.units))
        unit_c.Bind(wx.EVT_TEXT_ENTER, self.unit_input)

        unit_out_c = wx.TextCtrl(self.panel, name='unit_out_c',
                                 style=wx.TE_PROCESS_ENTER)
        unit_out_c.SetValue(str(self.conv_units))
        unit_out_c.Bind(wx.EVT_TEXT_ENTER, self.unit_request)

        mag_out = wx.TextCtrl(self.panel, style=wx.TE_READONLY, name='mag_out')
        self.set_mag_out()

        sizer.AddMany([(empty_txt), (magnitude_txt), (unit_txt),
                      (in_txt), (mag_c, 1, wx.EXPAND), (unit_c, 1, wx.EXPAND),
                      (out_txt), (mag_out), (unit_out_c, 1, wx.EXPAND)])

        self.panel.SetSizer(sizer)

    def magnitude_input(self, event):
        mag_c = self.FindWindowByName('mag_c')
        value = mag_c.GetValue()
        self.quantity *= float(value) / self.magnitude
        self.conv_quantity = self.quantity.to(self.conv_units)
        self.set_mag_out()

    def set_mag_out(self):
        mag_out = self.FindWindowByName('mag_out')
        mag_out.ChangeValue(str(self.conv_magnitude))

    def unit_input(self, event):
        unit_c = self.FindWindowByName('unit_c')
        value = unit_c.GetValue()
        self.quantity = self.magnitude * unit(value)
        self.conv_quantity = self.quantity.to(self.conv_units)
        self.set_mag_out()

    def unit_request(self, event):
        unit_out_c = self.FindWindowByName('unit_out_c')
        value = unit_out_c.GetValue()
        self.conv_quantity = self.quantity.to(str(unit(value)))
        self.set_mag_out()

try:
    if nasty_units:
        unit = pint.UnitRegistry("unit_definitions_all.txt")
    else:
        unit = pint.UnitRegistry("unit_definitions.txt")
except ValueError:
    unit = pint.UnitRegistry() # use default, if no files are found

if __name__ == '__main__':
    app = wx.App()
    wxPintCalc(debug=True)
    app.MainLoop()
