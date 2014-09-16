# First, you need to import libraries. Good practice is to make any imports first.
import csv, string, datetime




# Now, to read a csv file, you have to create an object that uses the csv library's reader function. The code below opens the file in universal line ending mode, and in the excel dialect, which is a safe default most of the time.
reader = csv.reader(open("blsdata.csv", "rU"), dialect=csv.excel)

# The first line of the file is going to be the header row, which you don't want, so skip ahead.
reader.next()

# Okay, this gets a little weird. The reader object here LOOKS like a list, but it's not a list. So, we have to make it into one.
dataList = [] # This creates an empty list for us to shove things.

for row in reader: # Starts a loop through the reader object
    dataList.append(row) # Shoves the row into our list.


# Now, to be able to compare a thing to the previous item in a list, you have to use enumerate. Enumerate makes each item in a list into a tuple with the index number and the item itself. By having the index, we can move up and down the index with simple math.
list(enumerate(dataList))

#find latest and previous month rates
currentYearList = dataList[-1] #last row = current year
currentYearList = filter(None, currentYearList) #trim empty space
currentMonthRate = float(currentYearList[-1])
previousMonthRate = float(currentYearList[-2])
lengthCurrentYear = len(currentYearList)


#find year before rate
yearBeforeList = dataList[-2]
yearBeforeList = filter(None, yearBeforeList) #trim empty space
rateYearBefore = float(yearBeforeList[lengthCurrentYear-1])
previousYear = (yearBeforeList[0])


#get the name of months
month = str(lengthCurrentYear-1) #convert last month number to string(next line needs it as string)
monthName = datetime.datetime.strptime(month,'%m').strftime('%B')   #Actual month name from number
previousMonth = str(lengthCurrentYear-2)
previousMonthName = datetime.datetime.strptime(previousMonth,'%m').strftime('%B')   #Actual month name from number


# Year before increase/decrease verb
if currentMonthRate > rateYearBefore:
    yearDirection = "an increase"
elif currentMonthRate == rateYearBefore:
    yearDirection = "unchanged "
else:
    yearDirection = "a decrease"

# Month before increase/decrease verb
if currentMonthRate > previousMonthRate:
    monthDirection = "an increase"
elif currentMonthRate == previousMonthRate:
    monthDirection = "unchanged"
else:
    monthDirection = "a decrease"

print "The Bureau of Labor Statistics reported the unemployment rate to be %s%% in %s. This is %s from the %s rate of %s%% and %s from the %s %s rate of %s%%." % (currentMonthRate, monthName, monthDirection, previousMonthName, previousMonthRate, yearDirection, monthName, previousYear, rateYearBefore)

#find consecutive months, only works up to 1 year
counter = len(currentYearList)-2
consecutiveMonths = 1

if float(currentMonthRate) < float(previousMonthRate):
    while currentMonthRate < currentYearList[counter]:
        currentMonthRate = currentYearList[counter]
        counter -= 1
        #print currentYearList[counter]
        consecutiveMonths  += 1
        #print consecutiveMonths
else:
    while float(currentMonthRate) > float(currentYearList[counter]):
        currentMonthRate = currentYearList[counter]
        counter = counter - 1
        consecutiveMonths  += 1

#print if consecutive month is >=3
if consecutiveMonths >= 3:
    print "The rate has shown", monthDirection, "for", consecutiveMonths, "consecutive months."




"""Other Stuff

Code for a single column:
column = [x[0] for x in dataList]
"""