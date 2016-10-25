# Serry Park, Mollee Jain, and Selina Sotomayor
# Calendar.py


#converts time into pixels
def convertPxl(time):
	start,end = time

	#adjusts time to start at 6AM
	startpix = int(start) - 600
	endpix = int(end) - 600

	#adjusts time to fit to scale on CalPal
	top = ((startpix/1600.) * 408) + 73
	bottom = ((endpix/1600.) * 408) + 73

	return (top, bottom)

#converts day of the week into pixels
#pixels will be used to set left on the div
def convertDay(day):
	daypix = 0
	if day == 'M':
		daypix = 50 + 88
	if day == 'T':
		daypix = 50 + (88*2)
	if day == 'W':
		daypix = 50 + (88*3)
	if day == 'R':
		daypix = 50 + (88*4)
	if day == 'F':
		daypix = 50 + (88*5)
	return daypix

#creates blocks for each course to be added to CalPal
def createBlocks(dictCourses):
	lines = []

	#lists to keep track of all the courses
	#and to allow us to output course information in 
	#the HTML (ie. in <div> tags to represent blocks)
	allTitles = []
	allTimes = []
	allTimePX = []
	allDayPX = []
	for elt in dictCourses:
		dayPX = convertDay(elt) #to move the block to the correct day 
		for x in range (len (dictCourses[elt])):
			index = x % 2
			if index == 0: #this the course part of the tuple value
				title, time = dictCourses[elt][x][2], dictCourses[elt][x][5] #get title and time info of the course
				allTitles.append(title)
				allTimes.append(time)
			else:
				militaryTime = dictCourses[elt][x]
				timePX = convertPxl(militaryTime) #to size the block
				allTimePX.append(timePX) 
				allDayPX.append(dayPX)
	string = createDivs(allTitles,allTimes,allTimePX,allDayPX)
	lines.append(string) #add the long string to a list
	return "\n".join(lines)	 #join each with a new line character

#A helper function to loop through the lists of course information
#and append it to a string containing <div> tags with the block info
def createDivs(titles,times,timePXs,dayPXs):
	string = ""
	for i in range(len(titles)): #all lists have the same length
		string += "<div class='block' style='left: " + str(dayPXs[i]) + "px;top: " + str(timePXs[i][0]) + "px;bottom: " + str(timePXs[i][1]) + "px; height: " + str(int(timePXs[i][1]-timePXs[i][0])) + "px'> <strong>"  + str(titles[i]) + "</strong><br>" + str(times[i]) + "</div>"
	return string
