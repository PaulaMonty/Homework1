#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Feb  3 11:06:53 2019

@author: Olukolade Adelabi

"""

import requests

##VARIABLES##
URL = "https://api.pmp.io"

headers = {'4e88e60d-0ffa-493d-bed9-8686e7b2e892:e0c46a55c8790cbea20a6917'}


response = requests.get(URL)

data = response.json



print(data)