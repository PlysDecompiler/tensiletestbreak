#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# usage:
# python tensiletest.py [path_to_P1-R100 [with_images]]


import os
import pathlib
import time
import sys
import numpy as np
import PIL
from PIL import Image, ImageDraw


def is_tear_in_file(filepath, image=False):
    startX, endX = 900, siz[0]-350
    startY, endY = 175, siz[1]-175
    STARTX = 50
    STARTY = 20
    img = Image.open(filepath)
    cropped = img.crop((startX, startY, endX, endY))
    crsize = cropped.size
    maxYStreak = 0
    yStreak = 0
    maximumPositions = []
    for y in range(STARTY, crsize[1]-STARTY):
        maxXStreak = 0
        xStreak = 0
        xPosMax = 0
        for x in range(STARTX, crsize[0]-STARTX):
            if cropped.getpixel((x,y)) < 1200:
                xStreak += 1
                if xStreak > maxXStreak:
                    maxXStreak = xStreak
                    xPosMax = x
            else:
                xStreak = 0
        if maxXStreak > 5:
            maximumPositions.append((xPosMax,y))
            yStreak += 1
            if yStreak > maxYStreak:
                maxYStreak = yStreak

    if image:
        if len(maximumPositions) > 2:
            weirdDistance = True
            while weirdDistance:
                if abs(maximumPositions[0][0] - maximumPositions[1][0]) < 20:
                    weirdDistance = False
                else:
                    maximumPositions = maximumPositions[1:]
            draw = ImageDraw.Draw(cropped)
            draw.line([maximumPositions[0], maximumPositions[-1]], fill=255)
            return cropped
    else:
        if maxYStreak > 10:
            return True
    return False


def binary_find_first_tear(prePath, files):
    fileAmount = len(files)
    
    if fileAmount < 5:
        for f in files:
            filePath = os.path.join(prePath, f)
            if is_tear_in_file(filePath):
                print(f)
                if wantImages:
                    tearImg = is_tear_in_file(filePath, True)
                    path = pathlib.PurePath(filePath)
                    lastPart = path.parent.name
                    tearImg.save(f"found_{lastPart}_{f}")
                return f
                
    middleResult = is_tear_in_file(os.path.join(prePath, files[fileAmount//2-1]))
    if middleResult:
        return binary_find_first_tear(prePath, files[:fileAmount//2])
    else:
        if fileAmount >=3:
            return binary_find_first_tear(prePath, files[fileAmount//2:])

        
def start_binary_find_first_tear(trialPath):
    fileList = os.listdir(trialPath)
    return binary_find_first_tear(trialPath, fileList)

def find_all_first_tears(folder):
    allTrials = os.listdir(folder)
    startTime = time.time()
    for trial in allTrials:
        print(os.path.join(folder, trial))
        start_binary_find_first_tear(os.path.join(folder, trial))
        print(f"{(time.time()-startTime):.1f}")


if __name__ == '__main__':
    wantImages = False
    if len(sys.argv) >= 2:
        print(sys.argv)
        mainFolder = sys.argv[1]
        if len(sys.argv) >= 3:
            if sys.argv[2] == "with_images":
                wantImages = True
    else:
        mainFolder = "P1-R100"
       
    allTrials = os.listdir(mainFolder)
    firstTrialPath = os.path.join(mainFolder, allTrials[0])
    firstTrialFiles = os.listdir(firstTrialPath)
    img0 = Image.open(os.path.join(firstTrialPath, firstTrialFiles[0]))
    siz = img0.size
    
    find_all_first_tears(mainFolder)
        