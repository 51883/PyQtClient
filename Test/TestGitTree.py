#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Created on 2019年1月16日
@author: Irony
@site: https://pyqt5.com https://github.com/892768447
@email: 892768447@qq.com
@file: Test.TestGitTree
@description: 
"""
import json
import os

import requests


__Author__ = "Irony"
__Copyright__ = "Copyright (c) 2019"

# https://raw.githubusercontent.com/PyQt5/PyQt/master/.gitattributes

RepositoryTrees = {'/': []}

url = 'https://api.github.com/repos/PyQt5/PyQt/git/trees/master?recursive=1'

if not os.path.isfile('tree.json'):
    req = requests.get(url)
    open('tree.json', 'wb').write(req.content)
    trees = req.json()['tree']
else:
    trees = json.loads(open('tree.json', 'rb').read().decode())['tree']

for tree in trees:
    path = tree['path']
    if path.startswith('.'):
        # The file or directory begins
        continue
    # File under the root directory
    if path.count('/') == 0 and tree['type'] == 'blob':
        RepositoryTrees['/'].append(tree)
        continue
    # Extract the directory under all root nodes
    name = path.split('/')[0]
    if name not in RepositoryTrees:
        RepositoryTrees[name] = []
    else:
        # Add non-directory
        if tree['type'] != 'tree':
            RepositoryTrees[name].append(tree)

print(RepositoryTrees)
