#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Thu Dec  6 22:44:37 2018

@author: root
"""

from skipthoughts import skipthoughts
import numpy as np
import sys

EXPERIMENT = 'interface'

print("Loading Model")
model = skipthoughts.load_model()
encoder = skipthoughts.Encoder(model)

#x = "There was a cold day. John went outside.".split('.')

x = sys.argv[1].split('.')

if x[-1] == '':
    x = x[:-1]

    
length = len(x)
vectors = encoder.encode(x)
np.save("data/" + EXPERIMENT + "/" + str(length), vectors)

print("Converted text to vectors")