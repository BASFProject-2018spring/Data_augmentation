#!/bin/python

# Run pre-process first

import argparse
from PIL import Image
import os
import re
from shutil import copyfile
import copy
def parse_args():
    parser = argparse.ArgumentParser(description="Image rotated, x-flipped, y-flipped")
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

def txt_to_point(txt_str):
    plist = []
    str_list = txt_str.split()
    i = 1
    for _ in range(int(str_list[0])):
        xmin = int(str_list[i])
        i+=1
        ymin = int(str_list[i])
        i+=1
        xmax = int(str_list[i])
        i+=1
        ymax = int(str_list[i])
        i+=1
        clabel = str(str_list[i])
        i+=1
        pdict = {"label":clabel,"points":[[xmin,ymin],[xmax,ymax],[xmin,ymax],[xmax,ymin]]}
        plist.append(pdict)
    return plist

def point_to_txt(plist):
    txt = str(len(plist))+"\n"
    for pdict in plist:
        xmin = min([x[0] for x in pdict['points']])
        xmax = max([x[0] for x in pdict['points']])
        ymin = min([x[1] for x in pdict['points']])
        ymax = max([x[1] for x in pdict['points']])
        txt += str(xmin)+' '+str(ymin)+' '+str(xmax)+' '+str(ymax)+' '+str(pdict['label'])+"\n"
    return txt

def point_apply(plist,func):
    global width,height
    for pdict in plist:
        new_point = []
        for point in pdict['points']:
            np = func(point)
            #if np[0]<0:
            #    np[0]=0
            #if np[0]>=width:
            #    np[0] = width-1
            #if np[1]<0:
            #    np[1]=0
            #if np[1]>=height:
            #    np[1]=height-1
            new_point.append(np)
        pdict['points']=new_point

count = 0
args = parse_args()
if not os.path.exists(args.aug_img):
    os.makedirs(args.aug_img)
if not os.path.exists(args.aug_label):
    os.makedirs(args.aug_label)

for label in list_files(args.label):
    img_path = re.sub('^'+args.label,args.img,label)[:-3] + 'jpg'
    orig_img = Image.open(img_path)
    width, height = orig_img.size
    orig_plist = txt_to_point(open(label,'r').read())
    count += 1

    #save original
    orig_img.save(os.path.join(args.aug_img,str(count)+'.jpg'),quality=args.quality)
    open(os.path.join(args.aug_label,str(count)+'.txt'),'w').write(point_to_txt(orig_plist))

    #rotate 180
    count+= 1
    orig_img.rotate(180).save(os.path.join(args.aug_img,str(count)+'.jpg'),quality=args.quality)
    plist=copy.deepcopy(orig_plist)
    point_apply(plist,lambda x: [width-x[0],height-x[1]])
    open(os.path.join(args.aug_label,str(count)+'.txt'),'w').write(point_to_txt(plist))

    #flip left-right
    count+= 1
    flip_img = orig_img.transpose(Image.FLIP_LEFT_RIGHT)
    flip_img.save(os.path.join(args.aug_img,str(count)+'.jpg'),quality=args.quality)
    plist = copy.deepcopy(orig_plist)
    point_apply(plist,lambda x: [width-x[0],x[1]])
    open(os.path.join(args.aug_label,str(count)+'.txt'),'w').write(point_to_txt(plist))

    #flip top-bottom
    count+= 1
    flip_img.rotate(180).save(os.path.join(args.aug_img,str(count)+'.jpg'),quality=args.quality)
    point_apply(plist,lambda x: [width-x[0],height-x[1]])
    open(os.path.join(args.aug_label,str(count)+'.txt'),'w').write(point_to_txt(plist))

print('done')