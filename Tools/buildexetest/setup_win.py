#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Created on 2019年1月18日
@author: Irony
@site: https://pyqt5.com https://github.com/892768447
@email: 892768447@qq.com
@file: setup_win
@description: 
"""
from distutils.core import setup
import sys

import py2exe  # @UnusedImport


__Author__ = "Irony"
__Copyright__ = "Copyright (c) 2019"


sys.path.append('../')

# windows - No console
# console

sys.argv.append('py2exe')  # Allow programs to be executed in the form of double-click

includes = []
excludes = []
dll_excludes = []

# compressed To 1 compressed file
# optimize For optimization level, default is 0
options = {
    'py2exe': {
        'compressed': 1,
        'optimize': 2,
        'bundle_files': 0,
        'includes': includes,
        'excludes': excludes,
        'dll_excludes': dll_excludes
    }
}

setup(
    version='1.0',
    description='PyQtClient',
    name='PyQtClient',
    zipfile=None,
    options=options,
    windows=[{
        'script': 'PyQtClient.py',
                'icon_resources': [(1, 'app.ico')],
    }],
    data_files=[]
)
