#!/usr/bin/python3
# -*- coding: utf-8 -*-

import sys

def test_version():
	assert(sys.version_info.major == 3)
	assert(sys.version_info.minor >= 7)

