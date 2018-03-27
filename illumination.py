#!/bin/python

# Run pre-process first

import argparse
import os
import re
from shutil import copyfile
import copy
import cv2
import numpy as np
def parse_args():
    parser = argparse.ArgumentParser(description="Image illumination 0.5, 1, 2")
    parser.add_argument('--img_folder',dest="img",default="new_img",type=str)
    parser.add_argument('--label_folder',dest="label",default="new_label",type=str)
    parser.add_argument('--aug_img_folder',dest="aug_img",default="aug_img",type=str)
    parser.add_argument('--aug_label_folder',dest="aug_label",default="aug_label",type=str)
    parser.add_argument('--quality',dest="quality",default=95,type=int)
    args = parser.parse_args()
    return args

def list_files(fldr):
    f_list = []
    for root, directories, filenames in os.walk(fldr):
        for f in filenames:
            f_list.append(os.path.join(root,f))
    return f_list

def adjust_gamma(image, gamma=1.0):
# https://stackoverflow.com/a/41061351
   invGamma = 1.0 / gamma
   table = np.array([((i / 255.0) ** invGamma) * 255
      for i in np.arange(0, 256)]).astype("uint8")

   return cv2.LUT(image, table)

count = 0
args = parse_args()
if not os.path.exists(args.aug_img):
    os.makedirs(args.aug_img)
if not os.path.exists(args.aug_label):
    os.makedirs(args.aug_label)

for label in list_files(args.label):
    img_path = re.sub('^'+args.label,args.img,label)[:-3] + 'jpg'
    orig_img = cv2.imread(img_path, 1)
    orig_plist = open(label,'r').read()
    count += 1

    #save original
    cv2.imwrite(os.path.join(args.aug_img,str(count)+'.jpg'), orig_img, [cv2.IMWRITE_JPEG_QUALITY, args.quality])
    open(os.path.join(args.aug_label,str(count)+'.txt'),'w').write(orig_plist)

    #illum 0.5
    count+= 1
    cv2.imwrite(os.path.join(args.aug_img,str(count)+'.jpg'), adjust_gamma(orig_img,0.5) ,[cv2.IMWRITE_JPEG_QUALITY, args.quality])
    open(os.path.join(args.aug_label,str(count)+'.txt'),'w').write(orig_plist)

    #illum 2
    count+= 1
    cv2.imwrite(os.path.join(args.aug_img,str(count)+'.jpg'), adjust_gamma(orig_img,2) ,[cv2.IMWRITE_JPEG_QUALITY, args.quality])
    open(os.path.join(args.aug_label,str(count)+'.txt'),'w').write(orig_plist)



print('done')
