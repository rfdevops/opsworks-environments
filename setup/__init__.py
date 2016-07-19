# -*- coding: utf-8 -*-
import os
import sys
APP_ROOT = os.path.dirname(os.path.realpath(__file__))

print APP_ROOT
sys.path.append(APP_ROOT)
os.environ.setdefault("PYTHONPATH", APP_ROOT)

print sys.path