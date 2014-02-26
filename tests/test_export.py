#!/usr/bin/env python2
# -*- coding: utf-8 -*-

from popeye.utils.export import SaveFile, NoExtensionKnowException
import numpy as np
import os
import pytest


F = os.path.dirname(__file__)
FILENAMEDATA = os.path.join(F, "Data/test.jpg")
FILEDATA_OUT_WRONG = os.path.join(F, "Data/out.jpg")
FILEDATA_OUT = os.path.join(F, "Data/out.tps")

def test_creator_save():
    mysave = SaveFile([FILENAMEDATA], FILEDATA_OUT, np.array([[[1, 2], [1, 3], [3, 4]]]), [1, 2])
    mysave.save()

def test_wrong_creator_landmarks():
    with pytest.raises(IndexError) as excinfo:
        mysave = SaveFile([FILENAMEDATA], FILEDATA_OUT, np.array([[1, 2], [1, 3], [3, 4]]), [1, 2])
        mysave = SaveFile([FILENAMEDATA], FILEDATA_OUT, [[[1, 2], [1, 3], [3, 4]]], [1, 2])


def test_wrong_filterlandmarks():
    with pytest.raises(IndexError) as excinfo:
        mysave = SaveFile([FILENAMEDATA], FILEDATA_OUT, np.array([[1, 2], [1, 3], [3, 4]]), [4, 5])

def test_wrong_extension():
    with pytest.raises(NoExtensionKnowException) as excinfo:
        mysave = SaveFile([FILENAMEDATA], FILEDATA_OUT_WRONG, np.array([[[1, 2], [1, 3], [3, 4]]]), [1, 2])
        mysave.save()

def test_empty_extension():
    with pytest.raises(IOError) as excinfo:
        mysave = SaveFile([FILENAMEDATA], "", np.array([[[1, 2], [1, 3], [3, 4]]]), [1, 2])
        mysave.save()

