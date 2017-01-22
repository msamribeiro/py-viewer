#!/usr/bin/python
"""
Simple CSV viewer for large files.
"""

import wx
import os, sys
import argparse

from interface import Viewer

if __name__ == "__main__":

    parser = argparse.ArgumentParser()

    parser.add_argument('--header', '-hd', action='store_true', help='treat first line as header')
    parser.add_argument('--regex', '-re', action='store_true', help='treat search text as regular expression')
    parser.add_argument('--search', '-s', default='', help='search string. value may be regular expression if --regex/-re is used. format: column:value. ')
    parser.add_argument('filename')

    args = parser.parse_args()

    if not os.path.isfile(args.filename):
        print 'Could not find filename %s' % (args.filename)
        sys.exit()

    app = wx.App()
    Viewer(args)
    app.MainLoop()




## TODO
# Debug Viewer properly 
    # there might be something wrong with the trailing buffer
    # not sure if we're losing lines along the way with the back and forth
# When removing header from non-first chunk, it gets added to list
# why so slow with 1000 lines showing?


# use logging
# proper commenting/documentation
# proper testing


## STATUS
# reads csv from file
# toggles header based on first line of file
# search by column (column:value)
# search based on regex (column:regex)
# input parameters from command line
# alternate colors between rows
# manages large files (not tested properly)


## WISH LIST
# show line counts for visible lines
# when searching from terminal, show top n based on search
# regex search on column (handle multiple column searches)
# regex search with numerical comparisons (=, >, <, ...)
# allow separator to be passed as argument (tabs, spaces, ...)
# editable cells
# copy text
# save to file

