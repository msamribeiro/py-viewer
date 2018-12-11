#!/usr/bin/python
"""

Interface for viewer

"""

import wx
import re
import os, sys
import logging

from reader import Reader

from wx.lib.mixins.listctrl import ListCtrlAutoWidthMixin
from wx.lib.mixins.listctrl import ColumnSorterMixin


class NewListCtrl(wx.ListCtrl, ColumnSorterMixin, ListCtrlAutoWidthMixin):
    ''' ListCtrl able to sort and manage width change '''

    def __init__(self, parent, data):
        wx.ListCtrl.__init__(self, parent, -1, style=wx.LC_REPORT)

        # the column sorter accepts one argument: number of columns to be sorted
        ColumnSorterMixin.__init__(self, len(data))
        # the data must be a dictionary
        self.itemDataMap = data

    def GetListCtrl(self):
        return self



class Viewer(wx.Frame):
    ''' Viewer interface that displays tables '''

    def __init__(self, config):

        ## define class attributes
        self.logger = logging.getLogger("Viewer")

        self.data   = None           # current data to show
        self.header = None           # first line of file to use as header
        self.title  = None           # filename

        self.useHeader  = config['header']         # if using first line as header
        self.useRegex   = config['regex']          # if searching with regular expression
        self.searchText = config['search']         # initial search string (may be empty)
        self.separator  = str(config['separator'])   # column separator (e.g. comma, tab, space)

        # handle highlighting of alternate lines
        self.highlight  = config['highlightLines']
        #self.highlight_color = wx.Colour(242, 242, 242)  # light gray for light themes
        self.highlight_color = wx.Colour(32, 32, 32)      # dark gray for dark themes

        self.text = None           # search box object
        self.regex_text = None     # regex checkbox object
        self.header_box = None     # header checkbox object

        self.reader = Reader(config)

        chunk = self.reader.next()
        self.ReadData(chunk)

        self.header = self.data[0]
        self.title = config['filename'].split('/')[-1]

        self.InitViewer()



    def InitViewer(self):
        ''' Creates and initializes the Viewer '''
        wx.Frame.__init__(self, None, -1, self.title, size=(1250, 800))

        # main layout manager
        vbox = wx.BoxSizer(wx.VERTICAL)
        panel = wx.Panel(self, -1)

        # first sub-layout manager (for data)
        hbox1 = wx.BoxSizer(wx.HORIZONTAL)

        # create list control and populate
        self.list = NewListCtrl(panel, self.data)

        # add data to layout manager
        hbox1.Add(self.list, 1, wx.EXPAND)

        # second sub-layout manager
        hbox2 = wx.BoxSizer(wx.HORIZONTAL)

        # create and add bottom controls
        regex_text = wx.TextCtrl(panel, value=self.searchText)
        hbox2.Add(regex_text, proportion=1, flag=wx.ALL, border=8)
        searchButton = wx.Button(panel, label='Search', pos=(10, 10))
        hbox2.Add(searchButton, proportion=0, flag=wx.ALL, border=8)
        regex_box = wx.CheckBox(panel, label='Use regex')
        hbox2.Add(regex_box, proportion=0, flag=wx.ALL, border=8)
        header_box = wx.CheckBox(panel, label='Use header')
        hbox2.Add(header_box, proportion=0, flag=wx.ALL, border=8)
        text = wx.StaticText(panel, label='Showing %i items' % (self.list.GetItemCount()))
        hbox2.Add(text, proportion=0, flag=wx.ALL, border=8)

        BackwardButton = wx.Button(panel, label='<--', pos=(10, 10))
        hbox2.Add(BackwardButton, proportion=0, flag=wx.ALL, border=8)

        ForwardButton = wx.Button(panel, label='-->', pos=(10, 10))
        hbox2.Add(ForwardButton, proportion=0, flag=wx.ALL, border=8)


        if self.useHeader:
            header_box.SetValue(True)
        if self.useRegex:
            regex_box.SetValue(True)

        self.text = text
        self.regex_text = regex_text
        self.header_box = header_box

        self.ShowData()

        # bind methods to buttons and check boxes
        searchButton.Bind(wx.EVT_BUTTON, self.OnSearch)
        header_box.Bind(wx.EVT_CHECKBOX, self.OnUseHeader)
        regex_box.Bind(wx.EVT_CHECKBOX, self.OnUseRegex)

        BackwardButton.Bind(wx.EVT_BUTTON, self.OnBackward)
        ForwardButton.Bind(wx.EVT_BUTTON, self.OnForward)

        # add sub-layout managers to main layout manager
        vbox.Add(hbox1, 2, wx.EXPAND)
        vbox.Add(hbox2, 0, wx.EXPAND)

        panel.SetSizer(vbox)

        self.Centre()
        self.Show(True)

    def ReadData(self, chunk):
        ''' prepares data for viewing by finding columns '''

        data = {}
        for i, line in enumerate(chunk):
            data[i] = line.rstrip().split(self.separator)
        self.data = data


    def ShowData(self):
        ''' Show all data items in the list control '''

        # clear all items in the list, if they exist
        self.list.ClearAll()

        # insert columns
        columns = len(self.data[self.data.keys()[0]])
        for index in range(columns):
            col_label = 'column ' + str(index+1)
            self.list.InsertColumn(index, col_label, width=140)

        items = self.data.items()

        # insert rows
        for key, row in items:

            index = self.list.InsertItem(sys.maxint, row[0])
            for i, item in enumerate(row[1:]):
                self.list.SetItem(index, i+1, row[i+1])
            self.list.SetItemData(index, key)

            if self.highlight:
                if index % 2:
                    self.list.SetItemBackgroundColour(index, self.highlight_color)

        if self.useHeader:
            self.OnUseHeader()

        if self.searchText:
            self.OnSearch()

        self.text.SetLabel("Showing %i items" % (self.list.GetItemCount()))



    def ToggleHeader(self, header=False):
        """ Use first line of file as header and shows everything else """
        n_columns = self.list.GetColumnCount()

        #header_labels = self.data[0]
        header_labels = self.header

        for i in range(n_columns):
            col = self.list.GetColumn(i)
            if header:
                col.SetText(header_labels[i])
            else:
                col.SetText('column '+ str(i+1))
            self.list.SetColumn(i, col)

        # find header index by looking for first column (may break here!)
        hindex = self.list.FindItem(-1, header_labels[0])

        if header:
            if hindex >= 0:
                self.list.DeleteItem(hindex)
            # else couldn't find header, so do nothing
        else:
            index = self.list.InsertItem(0, header_labels[0])
            for i, item in enumerate(header_labels[1:]):
                self.list.SetItem(index, i+1, header_labels[i+1])
            self.list.SetItemData(index, 0)

        self.text.SetLabel("Showing %i items" % (self.list.GetItemCount()))


    def ShowSearchData(self, column, pattern):
        """ Shows only data that matches pattern """

        # clear all items in the list
        self.list.ClearAll()

        # load only those that match
        columns = len(self.data[self.data.keys()[0]])
        for index in range(columns):
            col_label = 'column ' + str(index+1)
            self.list.InsertColumn(index, col_label, width=140)

        items = self.data.items()

        if self.useRegex:
            pattern = re.compile(pattern)

        for key, row in items:
            match = False
            if self.useRegex:
                match = pattern.match(row[column])
            elif row[column] == pattern:
                match = True

            if match:
                index = self.list.InsertItem(sys.maxint, row[0])
                for i, item in enumerate(row[1:]):
                    self.list.SetItem(index, i+1, row[i+1])
                self.list.SetItemData(index, key)

        # use header if box is checked
        if self.useHeader:
            self.ToggleHeader(header=True)

        self.text.SetLabel("Showing {0} items".format(self.list.GetItemCount()))


    def OnUseHeader(self, e=None):
        """ Called when headercheck box is used """
        if e:
            sender = e.GetEventObject()
            isChecked = sender.GetValue()
            self.useHeader = isChecked
        else:
            self.useHeader = True

        self.ToggleHeader(header=self.useHeader)


    def OnUseRegex(self, e=None):
        """ Called when regex checkbox is used """
        sender = e.GetEventObject()
        isChecked = sender.GetValue()
        self.useRegex = isChecked


    def OnSearch(self, e=None):
        """ Called when search button is pressed """
        text = self.regex_text.GetLineText(0)

        if text:
            column, pattern = text.split(':')
            for i in range(self.list.GetColumnCount()):
                if column == self.list.GetColumn(i).GetText():
                    self.ShowSearchData(i, pattern)
        else:
            self.ShowData()
            self.ToggleHeader(header=self.useHeader)


    def OnBackward(self, e=None):
        """ Called when Backward button is pressed """
        chunk = self.reader.previous()
        if chunk:
            self.ReadData(chunk)
            self.ShowData()


    def OnForward(self, e=None):
        """ Called when Forward button is pressed """
        chunk = self.reader.next()

        if chunk:
            self.ReadData(chunk)
            self.ShowData()

