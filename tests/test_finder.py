#!/usr/bin/env python2
# -*- coding: utf-8 -*-

from popeye.finder import Finder
import numpy as np
import os
import pytest


F = os.path.dirname(__file__)
FILENAMEDATA = os.path.join(F, "Data/test.jpg")
FILENAMEDATA_WRONG = os.path.join(F, "Data/not_found.jpg")

def test_find_landmarks():
    myfinder = Finder([FILENAMEDATA])
    myfinder.find_landmarks()
    assert np.all(myfinder.landmarks != 0)
    #check the landmarks position are located in the face
    
def test_wrong_finder_loader():
	with pytest.raises(IOError) as excinfo:
		myfinder = Finder([FILENAMEDATA_WRONG])
		myfinder.find_landmarks()

def test_draw_landmarks():
    myfinder = Finder([FILENAMEDATA])
    myfinder.find_landmarks()
    images = myfinder.draw_landmarks([i for i in range(77)])
    assert len(images) == len([FILENAMEDATA])

def test_wrong_draw_landmarks():
    with pytest.raises(IndexError) as excinfo:
        myfinder = Finder([FILENAMEDATA])
        myfinder.find_landmarks()
        images = myfinder.draw_landmarks([i for i in range(np.random.randint(78, 200))])

