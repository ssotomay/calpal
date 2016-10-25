'''
calpal
Mollee Jain, Serry Park, Selina Sotomayor
schedule.py 

This is a file that includes helper functions that helps the CGI python file collect the data and 
display what the user wants. 
Last updated: 5/15/2016
'''


#imports
import MySQLdb
import dbconn2

#setup
dsn = dbconn2.read_cnf('/students/calpal/.my.cnf')
dsn['db'] = 'random' #current database being used
dsn['host'] = 'localhost'
conn = dbconn2.connect(dsn)
curs = conn.cursor() 

#queryCourse()
#Takes in the crn of a course and returns the entire course entry in raw data (in a tuple format)
def queryCourse(crn):
    if (crn == '' or crn is None):
        return "Please enter CRN"
    curs.execute("SELECT * FROM course_data WHERE CRN = %s",(crn,))
    courseList = curs.fetchone()
    if courseList is None or courseList == '':
        return "CRN not in database"
    return courseList

#checkUser()
#Takes in bNum of the student and checks if the student currently has any courses in their calendar
#If true, then there are no courses, if false, then the student has courses in their calendar
def checkUser(bNum):
    curs.execute("SELECT count(*) from students where bNum = %s", (bNum,))
    row = curs.fetchone()
    row = int(row[0])
    return row == 0 #bool

#validBNUM()
#Checks if the given bNumber is a valid bNumber in length + type
def validBNUM(bNum):
    if bNum == '' or bNum == None:
        return False
    elif not bNum.isdigit():
        return False
    elif len(bNum) != 8:
        return False
    return True

#returnTable()
#Returns the 'calendar' table which contains all of the courses a student has
#signed up for (or added to their calendar)
#This is a dictionary of (course, times) where course is the data obtained from the course
# browswer and times are the times of the course converted into military time. 
def returnTable(bNum):
    curs.close() #close previous cursor
    curs2 = conn.cursor() #open new cursor
    curs2.execute("select * from students where bNum = %s",(bNum,))
    courses = curs2.fetchall()
    if (courses != None and len(courses) > 0):
        courseDict = {} #store courses by day in a dictionary 
        for course in courses: #for each course
            courseDict = getDict(course,courseDict) 
        return courseDict #return a nicely formatted dictionary
    else:
        return ''

#printDict()
#Takes in a dictionary where KEY: day (ie. 'M') and VALUE: (course, military time)
#This prints out the dictionary in a way more visually appealing. 
def printDict(dictionary):
    string = ''
    for key in dictionary:
        #VERSION1: Prints out all the data - ugly formatting!
        string += '<br><br><strong>' + toDay(key) +'</strong>' #+ str(dictionary[key])
        for x in range(len(dictionary[key])):
            courseIndex = x%2
            if courseIndex == 0: #look at ONLY the course part of the tuple (course, military times)
                string +=  "<br>" + 'CRN: ' + str(dictionary[key][x][1]) + ' , ' + str(dictionary[key][x][2]) + ',  ' + str(dictionary[key][x][3]) + ',  ' + str(dictionary[key][x][5])
    return string
        
#toDay
#Takes in a day (ie. 'R') and returns the string representation of that day (ie. Thursday)
def toDay(key):
    val = ''
    if key == 'M':
        val = 'Monday'
    elif key == 'T':
         val = 'Tuesday'
    elif key == 'W':
         val = 'Wednesday'
    elif key =='R':
        val = 'Thursday'
    elif key == 'F':
         val = 'Friday'
    return val

#checkCourse()
#Takes in a crn of a course and checks if there exists any course with that CRN
def checkCourse(bNum,crn):
    curs.execute("SELECT count(*) from students where bNum = %s and CRN = %s", (bNum,crn))
    row = curs.fetchone()
    introw = int(row[0])
    return introw == 0

#addCourse()
#Takes in an entire course (see queryCourse) in raw format and inserts it into the student table
def addCourse(courseList,bNum):
    if (courseList == '' or courseList == None or (courseList[0].isdigit() == False)):
        pass
    else:
        #courseList information directly from data
        (crn,course,title,distribution,time,professor1,professor2,location,day) = (courseList[0],courseList[1], courseList[2], courseList[3], courseList[4], courseList[5], courseList[6], courseList[7], courseList[8])
        
        #data to be inserted into the student's table (includes student bNum)
        data = (bNum,crn,course,title,distribution,time,professor1,professor2,location,day)
        curs.execute("insert into students (bNum, CRN, course, title, distribution, time, professor1,professor2, location, days) values (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)",data)

#delCourse()
#Takes in the CRN of a course and deletes it from the student table
def delCourse(bNum,crn):
    if (checkCourse(bNum,crn) == False and crn.isdigit()): 
        curs.execute("delete from students where bNum = %s and CRN = %s", (bNum,crn))

#formatTime()
#Takes in a string of time as it is formatted in the data (ie. '1:30 pm - 3:00 pm')
#Formats it so that it is military time to allow for sorting the courses by time
def formatTime(timeString):
    times = timeString.split(" - ") 
    
    #get each individual time
    startTime = times[0] 
    endTime = times[1]
    
    #convert startime:
    startMTime = toMilitary(startTime)
    endMTime =  toMilitary(endTime)
    return (int(startMTime), int(endMTime))
    #return times as a tuple

#toMilitary()
#Takes in singluar time formatted like X:XX ym and returns its value in military time
def toMilitary(time):
    (hour,minutes) = time.split(" ")[0].split(":") #gets the time, ie. 2:15pm instring format
    if ('pm' in time) and ('12' in time):
        mTime = hour + minutes
    elif ('pm' in time): #if in afternoon, add 12 onto the value
        hour = int(hour) + 12
        mTime = str(hour) + str(minutes)
    else: #in morning
        mTime = hour + minutes
    return mTime #return military time

#splitBySemicolon()
#Takes in a string that may or may not be formatted with a semicolon and reformats string
#so that the first and second value are used separately (ie. 'M;W' -> ['M'],['W'])
def splitBySemicolon(string):
    #temp lists to store the splitting values
    new = []
    first = []
    second = []
    if ';' in string: #if and only if the semicolon is in the string
        splitit = string.split("; ")
        firstday = splitit[0]
        secondday = splitit[1]
        first.append(firstday) #append to a new list
        second.append(secondday) #append to a new list
        new.append(first)
        new.append(second)
    else:  #otherwise 'MW' append each day as an element in the list (ie. ['M','W'])
        for day in string:
            new.append(day)
    return new #return formatted list


#replaceNum()
#Takes in the day format (ie. 'W1' or 'M3') and removes the number from the end
#to make it simpler for later formatting/computation('W' or 'M')
def replaceNum(day):
    newDay = ''
    for x in day: #for each day
        if x.isdigit():
            pass
        else:
            newDay+=x
    return newDay

#separate()
#Separates a string so each character is in a list(ie. 'MWF' -> ['M','W','F'])
#The code is longer/more complicated because it allows us to handle corner cases later
def separate(data):
    new = []
    for x in data:
        if len(data) > 1:      
            for y in x:
                if len(y) > 1:
                    a = list(y)
                    new.append(a)
                else:
                    a = list(x)
                    new.append(a)
        else: 
            new.append(x)
    return new


#Returns day of course
def getDay(course):
    day = course[9]
    day = day.strip('\r')
    day1 = splitBySemicolon(day)
    day2 = separate(day1)
    return day2
    
#getTime()
#Returns time of course as tuple in military time (i.e (1830,2100))
def getTime(course):
    tm = course[5]
    times = []
    #If course meets at two different times (indicated by ;)
    if ';' in tm:
        tm1 = splitBySemicolon(tm)
        for x in tm1:
            a = formatTime(x[0])
            times.append(a)
    else:
        tm1 = [tm]
        for x in tm1:
            a = formatTime(x)
            times.append(a)
    return times

#getDict()
#Returns dictionary containing days as keys and time as values (i.e M: (1830, 2100))
def getDict(course,cdict):
    day = getDay(course)
    tm = getTime(course)
    for x in day:
        ind = day.index(x)
        for y in x:
            #If day is not in dictionary add it as key, and time as value
            if y not in cdict: 
                if (len(tm) > 1):
                    cdict[y] = (course,tm[ind])
                else:
                    cdict[y] = (course,tm[0])
            else:
                if (len(tm) > 1):
                    cdict[y] += (course,tm[ind])
                else:
                    cdict[y] += (course,tm[0])
                #cdict[y] += (course,tm[ind])
    return cdict
