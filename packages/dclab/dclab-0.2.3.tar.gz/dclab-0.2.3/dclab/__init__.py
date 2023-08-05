#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
This library contains classes and methods for the analysis
of real-time deformability cytometry (RT-DC) data sets.
"""
from __future__ import division, print_function, unicode_literals

import os

# Definitions
from . import definitions as dfn
from ._version import version as __version__
from .rtdc_dataset import RTDC_DataSet, GetProjectNameFromPath
from .polygon_filter import PolygonFilter
from . import statistics, elastic

 
def GetTDMSFiles(directory):
    """ Recursively find projects based on '.tdms' file endings
    
    Searches the `directory` recursively and return a sorted list
    of all found '.tdms' project files, except fluorescence
    data trace files which end with `_traces.tdms`.
    """
    directory = os.path.realpath(directory)
    tdmslist = list()
    for root, _dirs, files in os.walk(directory):
        for f in files:
            # Exclude traces files of fRT-DC setup
            if (f.endswith(".tdms") and (not f.endswith("_traces.tdms"))):
                tdmslist.append(os.path.realpath(os.path.join(root,f)))
    tdmslist.sort()
    return tdmslist
