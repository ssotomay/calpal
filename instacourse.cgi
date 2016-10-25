#!/usr/local/bin/python2.7
# Serry Park and Selina Sotomayor
# instacourse.cgi 

import sys
import cgi
import cgitb; cgitb.enable()
import cgi_utils_sda
import schedule #from schedule.py
import Calendar #from Calendar.py
import os

#sets most fillers to blank for an empty form
#CRN (if given), B number, and log in message saved into fillers
def onSubmit(form_data,fillers):
    crn = form_data.getfirst('crn')
    bNum = form_data.getfirst('bNum')
    course = schedule.queryCourse(crn)
    fillers['message'] = ''
    fillers['courselist'] = course
    if (course == '' or course is None):
        fillers['savedcrn'] = ''
    else:
        fillers['savedcrn'] = course[0]
    fillers['schedule'] = ''
    fillers['bNum'] = bNum
    if not schedule.checkUser(bNum) or schedule.validBNUM(bNum): #if in sql table
        fillers["hidden"] = "hidden"
    else:
        fillers["hidden"] = ""
    fillers['loginMessage'] =  "You are logged in with the B number of " + str(bNum)
    return fillers

#adds course data to students table by CRN and B number
#throws error message if CRN is invalid (not in course_data table)
#or if the course data is already in the student table
#CRN, B number, and log in message saved into fillers
def onAdd(form_data,fillers):
    crn = form_data.getfirst('savedcrn')
    bNum = form_data.getfirst('bNum')
    crn= crn[0:5]
    course = schedule.queryCourse(crn)  
    if course[0].isdigit() == False:
        fillers['schedule'] = 'Not added to calendar, invalid CRN'
    elif schedule.checkCourse(bNum,crn):  
        display = "Adding: \n" + str(course)
        fillers['schedule'] = display
        schedule.addCourse(course,bNum) 
    else:
        fillers['schedule'] = "Course already added to Calendar"       
    fillers['message'] = ''
    fillers['courselist'] = ''
    fillers['savedcrn'] = course[0]
    fillers['bNum'] = bNum
    if not schedule.checkUser(bNum) or schedule.validBNUM(bNum): #if in sql table
        fillers["hidden"] = "hidden"
    else:
        fillers["hidden"] = ""
    fillers['loginMessage'] =  "You are logged in with the B number of " + str(bNum)

#removes course data by CRN and B number from students table
#if course is not in table, error message is thrown
#CRN, B number, and log in message saved into fillers
def onDel(form_data,fillers):
  crn = form_data.getfirst('savedcrn')
  bNum = form_data.getfirst('bNum')
  #removes unnecessary '/r' in crn
  crn = crn[0:5]
  if (crn.isdigit()):
      fillers['courselist']= " Deleting course: " + str(crn)
      schedule.delCourse(bNum,crn) 
  else:
      fillers['courselist'] =" Invalid crn or no crn found in calendar. Try again"
      crn = ''
  fillers['message'] = ''
  fillers['savedcrn'] = crn
  fillers['schedule'] = ''
  fillers['bNum'] = bNum
  if not schedule.checkUser(bNum) or schedule.validBNUM(bNum): #if in sql table
      fillers["hidden"] = "hidden"
  else:
      fillers["hidden"] = ""
  fillers['loginMessage'] =  "You are logged in with the B number of " + str(bNum)


# main part: run when the webpage loads and when the appropriate buttons are pressed
if __name__ == '__main__':
    
    print 'Content-type: text/html\n'
    tmpl = cgi_utils_sda.file_contents('instacourse.html')
    form_data = cgi.FieldStorage()
    fillers = {}
    curHidden = False
    #stores B number and CRN (if given) into filler data
    if 'login' in form_data:
      crn = form_data.getfirst('savedcrn')
      bNum = form_data.getfirst('loginbNum')
      fillers['bNum'] = bNum
      if schedule.validBNUM(bNum):
      	 fillers['loginMessage'] = "You are logged in with the B number of " + bNum
         fillers['hidden'] = "hidden"
      else:
          fillers['bNum'] = 'INVALID BNUM'
          fillers['loginMessage'] = "Invalid login. Please enter your B number"
          fillers['hidden'] = ""
      fillers['message'] = ''
      fillers['courselist'] = ''
      fillers['savedcrn'] = crn
      fillers['schedule'] = ''
      
      curHidden = True
    #stores CRN of course selected when submit button is pressed
    elif 'submit' in form_data:
      onSubmit(form_data,fillers)
      
    #adds course to student table via CRN and B number when add button is pressed
    elif 'add' in form_data:
      onAdd(form_data,fillers)
     
    #deletes course from student table via CRN and B number when delete button is pressed
    elif 'delete' in form_data:
      onDel(form_data,fillers)
      #if curHidden:
      fillers['hidden'] = "hidden"
      #else:
       #   fillers['hidden'] = ''
    #returns blank fillers (for returning a blank form) when no buttons are pressed
    else:
      fillers['message'] = ''
      fillers['courselist'] = ''
      fillers['savedcrn'] = ''
      fillers['schedule'] = ''
      fillers['bNum'] = ''
      fillers['loginMessage'] = ''
      fillers["hidden"] = ''
    #returns an updated dictionary of courses for that student
    #for beta version, we will have prettier output
    dictionary = schedule.returnTable(form_data.getfirst('bNum'))
    fillers['curCourses'] = schedule.printDict(dictionary)
    fillers['schedBlock'] = Calendar.createBlocks(dictionary) #temp

    print tmpl.format(**fillers)
