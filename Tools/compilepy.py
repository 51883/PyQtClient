#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Created on 2019年1月18日
@author: Irony
@site: https://pyqt5.com https://github.com/892768447
@email: 892768447@qq.com
@file: Test.compilepy
@description: 
"""

import compileall
import os
from pathlib import Path
import shutil
import sys


__Author__ = "Irony"
__Copyright__ = "Copyright (c) 2019"

os.chdir('../')

# Delete library directory
dirPath = os.path.abspath('Library')

shutil.rmtree(dirPath, ignore_errors=True)

# Create a directory
os.makedirs(dirPath, exist_ok=True)
# Copy catalog
shutil.copytree(os.path.abspath('UiFiles'),
                os.path.join(dirPath, 'UiFiles'))
shutil.copytree(os.path.abspath('Utils'), os.path.join(dirPath, 'Utils'))
shutil.copytree(os.path.abspath('Widgets'),
                os.path.join(dirPath, 'Widgets'))

open(os.path.join(dirPath, '__init__.py'), 'wb').write(b'')

# Compile the entire directory
compileall.compile_dir(dirPath, force=True, optimize=0)


info = sys.version_info
cpythonname = '.cpython-{}{}'.format(info.major, info.minor)
print(cpythonname)

for file in Path(dirPath).rglob('*.pyc'):
    path = os.path.join(str(file.parent.parent), file.name)
    shutil.copy(str(file), path)
    try:
        os.rename(path, path.replace(cpythonname, ''))
    except:
        pass

# Delete PY files and UI files, PYD files
for ext in ('*.py', '*.ui', '*.pyd', '*.bak'):
    for file in Path(dirPath).rglob(ext):
        try:
            os.unlink(str(file))
        except Exception as e:
            print(e)
for file in Path(dirPath).rglob('__pycache__'):
    try:
        shutil.rmtree(str(file), ignore_errors=True)
    except Exception as e:
        print(e)

print('Compilation completion')
