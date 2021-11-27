#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Created on 2019年1月17日
@author: Irony
@site: https://pyqt5.com https://github.com/892768447
@email: 892768447@qq.com
@file: Test.TestDownProgress
@description: 
"""

__Author__ = "Irony"
__Copyright__ = "Copyright (c) 2019"

from contextlib import closing

import requests


if __name__ == '__main__':
    url = 'https://raw.githubusercontent.com/PyQt5/PyQt/master/Demo/Data/dlib-19.4.0.win32-py3.5.exe'
    with closing(requests.get(url, stream=True)) as response:
        chunk_size = 1024  # Single request maximum
        content_size = int(response.headers['content-length'])  # Total size
        print('content_size:', content_size)
        data_count = 0
        with open('dlib-19.4.0.win32-py3.5.exe', "wb") as file:
            for data in response.iter_content(chunk_size=chunk_size):
                file.write(data)
                data_count = data_count + len(data)
                now_jd = (data_count / content_size) * 100
                print("\r File download progress：%d%%(%d/%d) - %s" %
                      (now_jd, data_count, content_size, url), end=" ")
