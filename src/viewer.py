#!/usr/bin/python
"""

Simple CSV viewer for large files.

"""

import wx
import os, sys
import json
import argparse
import logging

from interface import Viewer

if __name__ == "__main__":

    parser = argparse.ArgumentParser()

    parser.add_argument('--header', '-hd', action='store_true', help='treat first line as header')
    parser.add_argument('--regex', '-re', action='store_true', help='treat search text as regular expression')
    parser.add_argument('--search', '-s', default='', help='search string. value may be regular expression if --regex/-re is used. format: column:value. ')
    parser.add_argument('filename')

    log_level = logging.DEBUG
    logging.basicConfig(format='%(asctime)-15s %(levelname)s: %(message)s',  datefmt='%m/%d/%Y %H:%M:%S', level=log_level)

    args = parser.parse_args()

    # make sure given filename and default config exist
    if not os.path.isfile(args.filename):
        logging.critical('Could not find filename {0}'.format(args.filename))
        sys.exit(1)

    if not os.path.isfile('conf.json'):
        logging.critical('Could not find default config file conf.json')
        sys.exit(1)

    print(os.path.realpath(__file__))

    # load default configuration options
    with open('conf.json') as fid:
        config = json.load(fid)

    # overwrite default config with given arguments
    for key, value in vars(args).items():
        config[key] = value

    app = wx.App()
    Viewer(config)
    app.MainLoop()
