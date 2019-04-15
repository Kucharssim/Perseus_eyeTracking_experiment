# -*- coding: utf-8 -*-
"""
Created on Sat Mar 16 11:22:13 2019

@author: Jiri
"""
import os
import pandas


DISPTYPE = 'psychopy'
DISPSIZE = (1280,720)

TRACKERTYPE = 'eyelink'
DUMMYMODE = True

FGC = (255, 255, 255)
BGC = (0, 0, 0)

FIXTIME = 10000
IMGTIME = 10000

DIR = os.path.dirname(os.path.abspath('__file__'))
MATDIR = os.path.join(DIR,'games')
MATNAMES = os.listdir(MATDIR)

# Get game structure values

df_own = pandas.read_csv(os.path.join(MATDIR,'games_own.csv'))
game_vectors_own = df_own.values

df_other = pandas.read_csv(os.path.join(MATDIR,'games_other.csv'))
game_vectors_other = df_other.values