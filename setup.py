#!/usr/bin/env python2
# -*- coding: utf-8 -*-

from distutils.core import setup
import py2exe
import os

opts = {
    'py2exe': { "includes" : [ "sip", "PyQt4"],
                'excludes': ['_gtkagg', '_tkagg', '_agg2', '_cairo', '_cocoaagg',
                             '_fltkagg', '_gtk', '_gtkcairo', ],
                'dll_excludes': ['libgdk-win32-2.0-0.dll',
                                 'libgobject-2.0-0.dll', 'MSVCP90.dll']#,'bundle_files': 2,'optimize': 2
              }
       }

setup(windows=[{"script" : "main.py"}], options=opts) #,   data_files=matplotlib.get_py2exe_datafiles())
