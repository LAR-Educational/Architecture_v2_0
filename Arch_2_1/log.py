#!/usr/bin/env python
# -*- coding: utf-8 -*-

import file
import datetime

debug = True


class bcolors:
    RED = '\033[1;31m'
    BLUE = '\033[1;34m'
    CYAN = '\033[1;36m'
    GREEN = '\033[0;32m'
    HEADER = '\033[0;95m'
    WARNING = '\033[1;93m'
    FAIL = '\033[1;91m'
    ENDC = '\033[;0m'
    BOLD = '\033[;1m'
    UNDERLINE = '\033[;4m'
    REVERSE = '\033[;7m'


class tag:
    INFO = 0
    WARNING = 1
    EXCEPTION = 2
    ERROR = 3


class Log(object):
    def __init__(self, debug=False):
        self.debug = debug
        self.file = file.File('log', 'LogFiles')

    def log(self, stringToPrint, logTag=tag.INFO,
            module='General', activity='Default'):
        if self.debug:
            if(logTag == tag.INFO):
                print('{}[INFO]{} [{}] [{}] [{}]{} {}'.format(
                    bcolors.BOLD, bcolors.BOLD, activity, module,
                    datetime.datetime.now().strftime('%Y-%m-%d %H:%M'),
                    bcolors.ENDC, stringToPrint))
            elif(logTag == tag.WARNING):
                print('{}[WARNING]{} [{}] [{}] [{}]{} {}'.format(
                    bcolors.WARNING, bcolors.BOLD, activity, module,
                    datetime.datetime.now().strftime('%Y-%m-%d %H:%M'),
                    bcolors.ENDC, stringToPrint))
            elif(logTag == tag.EXCEPTION):
                print('{}[EXCEPTION]{} [{}] [{}] [{}]{} {}'.format(
                    bcolors.BLUE, bcolors.BOLD, activity, module,
                    datetime.datetime.now().strftime('%Y-%m-%d %H:%M'),
                    bcolors.ENDC, stringToPrint))
            elif(logTag == tag.ERROR):
                print('{}[ERROR]{} [{}] [{}] [{}]{} {}'.format(
                    bcolors.FAIL, bcolors.BOLD, activity, module,
                    datetime.datetime.now().strftime('%Y-%m-%d %H:%M'),
                    bcolors.ENDC, stringToPrint))
        if(logTag == tag.INFO):
            self.file.write('INFO, {}, {}, {}, {}'.format(
                activity, module,
                datetime.datetime.now().strftime('%Y-%m-%d %H:%M'),
                stringToPrint))
        elif(logTag == tag.WARNING):
            self.file.write('WARNING, {}, {}, {}, {}'.format(
                activity, module,
                datetime.datetime.now().strftime('%Y-%m-%d %H:%M'),
                stringToPrint))
        elif(logTag == tag.EXCEPTION):
            self.file.write('EXCEPTION, {}, {}, {}, {}'.format(
                activity, module,
                datetime.datetime.now().strftime('%Y-%m-%d %H:%M'),
                stringToPrint))
        elif(logTag == tag.ERROR):
            self.file.write('ERROR, {}, {}, {}, {}'.format(
                activity, module,
                datetime.datetime.now().strftime('%Y-%m-%d %H:%M'),
                stringToPrint))
