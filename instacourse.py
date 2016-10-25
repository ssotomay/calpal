# -*- coding: utf-8 -*-
"""
Created on Sat Apr 16 12:25:54 2016

@author: Serry
"""

import json
import csv
#import itertools
from datetime import datetime

def convertToMinBeforeMidnight(time):
    date_object = datetime.strptime(time, '%I:%M %p')
    return date_object.time()
 
with open("courses.json") as inputfile:
   courses = json.load(inputfile)

course_data = courses

# open a file for writing
cdata = open('cdata.csv', 'w')

# create the csv writer object
csvwriter = csv.writer(cdata)

# extract info from JSON data
CRN = []
course = []
title = []
dist = []
time = []
prof1 = []
prof2 = []
loc = []
day = []

#header = ['CRN','Course','Title','Distribution','Time','Professor1','Professor2','Location','Day']
#csvwriter.writerow(header)

for c in course_data:
    crns = str(c['CRN'])
    CRN.append(crns)
    coursename = str(c['COURSE'])
    course.append(coursename)
    coursetitle = str(c['LONG_TITLE'])
    title.append(coursetitle)
    distname = str(c['DISTRIBUTIONS'])
    dist.append(distname)
    times = str(c['MEETING_TIMES'])
    time.append(times)
    profs = str(c['INSTRUCTOR1_PRINTNAME'])
    prof1.append(profs)
    profs = str(c['INSTRUCTORS'])
    prof2.append(profs) 
    locs = str(c['LOCATIONS'])
    loc.append(locs) 
    days = str(c['DAYS'])
    days = replaceTh(days)
    day.append(days)
    for cr, cn, ct, ds, t, p1, p2, l, d in zip(CRN, course, title, dist, time, prof1, prof2, loc, day):
        values = cr, cn, ct, ds, t, p1, p2, l, d
        
    csvwriter.writerow(values)

cdata.close()
'''
#replaceTh()
#Replaces all intances of Th with R to make computation easier in the future
def replaceTh(day):
    s = []
    for x in day:
        if len(x) > 1:
            combo = []
            for y in x:
                w = x.replace('Th','R')
                combo.append(w)
            s.append(combo)
        else:
            w = x.replace('Th','R')
            s.append(w)
    return s
'''

def replaceTh(day):
    b = day
    if 'Th' in day:
        b = day.replace('Th','R')
    return b

    
'''    
def splitz(data):
    new = []
    for x in data:
        if ';' in x:    
            splitit = x.split("; ")
            new.append(splitit)
        else:
            new.append(x)
    return new


def replaceTh():
    s = []
    for x in day:
        if len(x) > 1:
            combo = []
            for y in x:
                w = x.replace('Th','R')
                combo.append(w)
            s.append(combo)
        else:
            w = x.replace('Th','R')
            s.append(w)
    return s


def replaceNum(data):
    t = []    
    for x in data:
        if len(x) > 1:
            combo = []
            for y in x:
                if len(y) > 1:
                    if y[1] == '1' or y[1] == '2':
                        combo.append(y[0])
                    else:
                        combo.append(y)
            t.append(combo)
        else:
            t.append(x)
    return t 


def separate(data):
    new = []
    for x in data:
        if len(x) == 1:
            new.append(list(x))
        else:
            for y in x:
                new.append(list(y)) 
    return new
  

def converttime():
    startTimes = []
    endTimes = []
    for x in time:
        #split the shit by ; and -
        #put into list splitTime
        splitTime = x.split("; ")    #if multiple times, splits each one
        for i in splitTime:
            if i != "None":
                startTime = i.split(" - ")[0]
                endTime = i.split(" - ")[1]
                start = convertToMinBeforeMidnight(startTime)
                end = convertToMinBeforeMidnight(endTime)
                startTimes.append(start)
                endTimes.append(end)
    return startTimes, endTimes
'''
