import csv, string, datetime

reader = csv.reader(open("blsdata.csv", "rU"), dialect=csv.excel)

reader.next()

dataList = []

for row in reader:
    dataList.append(row)

currentYearList = dataList[-1]
currentYearList = filter(None,currentYearList)

lengthCurrentYear = len(currentYearList)

if lengthCurrentYear > 2:
    currentMonthRate = currentYearList[-1]
    previousMonthRate = currentYearList[-2]
    currentYear = int(currentYearList[0])
    monthNumber = str(lengthCurrentYear-1) #convert last month number to string(next line needs it as string)
    monthName = datetime.datetime.strptime(monthNumber,'%m').strftime('%B')   #Actual month name from number
    previousYearList = dataList[-2]
    previousYearList = filter(None,previousYearList)
    previousYear = (previousYearList[0])

    previousMonth = str(lengthCurrentYear-2)
    previousMonthName = datetime.datetime.strptime(previousMonth,'%m').strftime('%B')


else:
    currentMonthRate = currentYearList[1]
    previousYearList = dataList[-2]
    previousYearList = filter(None,previousYearList)
    previousMonthRate = previousYearList[-1]
    currentYear = int(currentYearList[0])
    monthNumber = str(lengthCurrentYear-1) #convert last month number to string(next line needs it as string)
    monthName = datetime.datetime.strptime(monthNumber,'%m').strftime('%B')   #Actual month name from number
    previousYear = (previousYearList[0])

    previousMonth = str(12)
    previousMonthName = datetime.datetime.strptime(previousMonth,'%m').strftime('%B')


previousYearList = dataList[-2]
previousYearMonthRate = previousYearList[lengthCurrentYear-1]

   #Actual month name from number

# Year before increase/decrease verb
if currentMonthRate > previousYearMonthRate:
    yearDirection = "an increase"
elif currentMonthRate == previousYearMonthRate:
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
    
percentChange = abs((float(currentMonthRate)-float(previousMonthRate))/float(previousMonthRate)*100)


print "The Bureau of Labor Statistics reported the unemployment rate to be %s percent in %s of %s. This is %s of %.1f percent from the %s rate of %s percent and %s from the %s %s rate of %s%%." % (currentMonthRate, monthName, currentYear,  monthDirection, percentChange,  previousMonthName, previousMonthRate, yearDirection, monthName, previousYear, previousYearMonthRate)

#find consecutive months, only works up to 1 year
counter = len(currentYearList)-2
consecutiveMonths = 1

if currentMonthRate < previousMonthRate:
    while float(currentMonthRate) < float(currentYearList[counter]):
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

#add line if consecutive month is >=3
if consecutiveMonths >= 3:
    print "The rate has shown", monthDirection, "for", consecutiveMonths, "consecutive months."


"""Other Stuff

Code for a single column:
column = [x[0] for x in dataList]

add percent change,

"""