#!/usr/bin/env python
# -*- coding:utf-8 -*-

# import csv
import os
# print(os.path.dirname(__file__))
script_dir = os.path.dirname(__file__) #<-- absolute dir the script is in
rel_path = "trained_models/shape_predictor_68_face_landmarks.dat"
abs_file_path = os.path.join(script_dir, rel_path)
# # read flash.dat to a list of lists
# datContent = [i.strip().split() for i in open(abs_file_path,'r',encoding='latin1').readlines()]
# print(datContent,encoding='latin1')
# # write it as a new CSV file
# with open("./trained_models/shape_predictor_68_face_landmarks.csv", "a") as f:
#     writer = csv.writer(f)
#     writer.writerows(datContent)

###########################

# import re

# with open(abs_file_path, encoding='latin1') as f:
#     lines = f.readlines()
#     text = "".join(lines)

# regex = r"\|(.*?);"
# matches = re.finditer(regex, text, re.MULTILINE | re.DOTALL)


# data = []

# for matchNum, match in enumerate(matches, start=1):
#     for group in match.groups():
#         data.append(group.split(","))

# for d in data:
#     print(d)

################################

# import numpy as np

# data = np.genfromtxt(abs_file_path,
#                      skip_header=1,
#                      skip_footer=1,
#                      names=True,
#                      dtype=None,
#                      delimiter=' ')
# print(data)
# # print garble
###############################

import time
import binascii
import csv
import serial

with open(abs_file_path, 'b') as binary_file:    
    for num in range(1,10):
        data = binary_file.readline()
        print(data)
# print garble
