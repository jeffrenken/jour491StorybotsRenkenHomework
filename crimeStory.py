__author__ = 'jeffreyrenken'

#crimeStory bot reads from UCRdata.csv to write a story based on every city's crime data


import string, csv, operator, sys

ucrData = list(csv.reader(open('UCRdata.csv', 'rU'), dialect="excel"))


crimeRateLowest = 100000
crimeRateHighest = 0
cityCrimeList = []
dictCityCrime = {}
unreportedList = []

#sorting For loop - 2012 crime rate
for row in ucrData[1:]:
    if row[4]:
        if row[9]:
            if row[3]:
                sortCrimeRate2012 = ((float(row[4])+float(row[9]))/float(row[3]))*100000
                sortCity = row[2]
                sortStateAP = row[1]
                cityState = "%s, %s" % (sortCity, sortStateAP)
                dictCityCrime[cityState] = sortCrimeRate2012
    else:
        sortCrimeRate2012 = None
"""
    sortCity = row[2]
    sortStateAP = row[1]
    cityState = "%s, %s" % (sortCity, sortStateAP)

    if sortCrimeRate2012 != None:
        dictCityCrime[cityState] = sortCrimeRate2012
#print dictCityCrime
"""
sorted_dictCityCrime = sorted(dictCityCrime.items(), key=operator.itemgetter(1))


#start of main For loop that creates every story
for row in ucrData[1:]:

    #Create list of cities with unreported data. Last line could be put in else clauses to be more specific, but repeats
    testList = filter(None,row)
    if len(testList) < len(row):
        unreportedList.append(testList)


#calc total crime rate for all years
    #ifs check for empty cells
    if row[35]:
        if row[40]:
            if row[34]:
                crimeRate2009 = ((float(row[35])+float(row[40]))/float(row[34]))*100000
    else:
        crimeRate2009 = None


    if row[25]:
        if row[30]:
            if row[24]:
                crimeRate2010 = ((float(row[25])+float(row[30]))/float(row[24]))*100000
    else:
        crimeRate2010 = None

    if row[15]:
        if row[20]:
            if row[14]:
                crimeRate2011 = ((float(row[15])+float(row[20]))/float(row[14]))*100000
    else:
        crimeRate2011 = None

    if row[4]:
        if row[9]:
            if row[3]:
                crimeRate2012 = ((float(row[4])+float(row[9]))/float(row[3]))*100000
    else:
        crimeRate2012 = None



#trend check for 3 consecutive years - overall crime rate
    if crimeRate2012 > crimeRate2011 > crimeRate2010 > crimeRate2009:
        crimeRateTrend = ", the third consecutive year with higher crime"
    elif crimeRate2012 < crimeRate2011 < crimeRate2010 < crimeRate2009:
        crimeRateTrend = ", a decline for the third consecutive year"
    else:
        crimeRateTrend = ""

#calc Crime Rate Percent Change
    if crimeRate2012:
        if crimeRate2011:
            crPercentChange = ((crimeRate2012-crimeRate2011) / crimeRate2011)*100
    else:
        crPercentChange = None

#Verb Crime Rate percent change
    if crPercentChange > 0:
        crPercentChangeDirection = "increase"
    elif crPercentChange < 0:
        crPercentChangeDirection = "decrease"
    else:
        crPercentChangeDirection = "change"

    if crPercentChange:
        crPercentChange = abs(crPercentChange)




#Property Crime Section
    if row[40]:
        if row[34]:
            propertyCrimeRate2009 = ((float(row[40]))/float(row[34]))*100000
    else:
        propertyCrimeRate2009 = None


    if row[30]:
        if row[24]:
            propertyCrimeRate2010 = ((float(row[30]))/float(row[24]))*100000
    else:
        propertyCrimeRate2010 = None


    if row[20]:
        if row[14]:
            propertyCrimeRate2011 = ((float(row[20]))/float(row[14]))*100000
    else:
        propertyCrimeRate2011 = None


    if row[9]:
        if row[3]:
            propertyCrimeRate2012 = ((float(row[9]))/float(row[3]))*100000
    else:
        propertyCrimeRate2012 = None


#Calc Property Crime percent change
    propertyPercentChange = ((propertyCrimeRate2012-propertyCrimeRate2011) / propertyCrimeRate2011)*100

#Vebs property crime
    if propertyPercentChange > 0:
        propertyPercentChangeDirection = "an increase"
        propertyRateChangeDirection = "rose"
    elif propertyPercentChange < 0:
        propertyPercentChangeDirection = "a decrease"
        propertyRateChangeDirection = "dropped"
    else:
        propertyPercentChangeDirection = "unchanged"
        propertyRateChangeDirection = "stayed constant"

    propertyPercentChange = abs(propertyPercentChange)



#Violent Crime Rate Section

    if row[35]:
        if row[34]:
            violentCrimeRate2009 = ((float(row[35]))/float(row[34]))*100000
    else:
        violentCrimeRate2009 = None

    if row[25]:
        if row[24]:
            violentCrimeRate2010 = ((float(row[25]))/float(row[24]))*100000
    else:
        violentCrimeRate2010 = None

    if row[15]:
        if row[14]:
            violentCrimeRate2011 = ((float(row[15]))/float(row[14]))*100000
    else:
        violentCrimeRate2011 = None

    if row[4]:
        if row[3]:
            violentCrimeRate2012 = ((float(row[4]))/float(row[3]))*100000
    else:
        violentCrimeRate2012 = None


#Calc violent percent change
    if violentCrimeRate2012:
        if violentCrimeRate2011:
            violentPercentChange = ((violentCrimeRate2012-violentCrimeRate2011) / violentCrimeRate2011)*100
    else:
        violentPercentChange = 0



    if violentPercentChange > 0:
        violentRateChangeDirection = "an increase"
        violentPercentChangeDirection = "increased"
    elif violentPercentChange < 0:
        violentRateChangeDirection = "a decrease"
        violentPercentChangeDirection = "decreased"
    else:
        violentRateChangeDirection = "is unchanged at"
        violentPercentChangeDirection = "stayed constant at"

    violentPercentChange = abs(propertyPercentChange)

    city = row[2]

    rankedCityState = "%s, %s" % (row[2], row[1])


#Main printing section
    sys.stdout.write ("%s, %s --"  % (string.upper(row[2]), row[1]))

#check for overall unreported data
    try:
        #cityRank = [y[0] for y in sorted_dictCityCrime].index(rankedCityState)
        sys.stdout.write (" Police reported a %.01f percent %s in overall crime in 2012%s." % (crPercentChange, crPercentChangeDirection, crimeRateTrend))
    except TypeError: #ValueError
        sys.stdout.write (" Overall crime for %s is not available due to unreported crime data." % (city))
        #i = -1

#check for property crime unreported data

    try:
        sys.stdout.write (" Property crime in the city %s %.01f percent. This is %s from %.0f crimes per 100,000 residents in 2011 to %.0f in 2012." % (propertyRateChangeDirection, propertyPercentChange, propertyPercentChangeDirection, propertyCrimeRate2011, propertyCrimeRate2012))
    except TypeError:
        sys.stdout.write (" Property crime rates are unavailable due to unreported data.")

#check for violent crime unreported data
    try:
        sys.stdout.write (" Violent crime %s %.01f percent to %.0f per 100,000 residents." % (violentPercentChangeDirection, violentPercentChange, violentCrimeRate2012))
    except TypeError:
        sys.stdout.write (" Violent crime rates are unavailable due to unreported data.")


#function to create ordinal ranking numbers
    def ordinal(number):
        if number < 20: #determining suffix for < 20
            if number == 1:
                suffix = 'st'
            elif number == 2:
                suffix = 'nd'
            elif number == 3:
                suffix = 'rd'
            else:
                suffix = 'th'
        else:           #determining suffix for > 20
            tens = str(cityRank)
            tens = tens[-2]
            unit = str(cityRank)
            unit = unit[-1]
            if tens == "1":
                suffix = "th"
            else:
                if unit == "1":
                    suffix = 'st'
                elif unit == "2":
                    suffix = 'nd'
                elif unit == "3":
                    suffix = 'rd'
                else:
                    suffix = 'th'
        return str(number)+ suffix

#Calc and Print ranking for safest city
    try:
        cityRank = [y[0] for y in sorted_dictCityCrime].index(rankedCityState)
        cityRank +=1
        #Call ordinal converting cityRank
        cityRankString = ordinal(cityRank);
        sys.stdout.write (" Based on the 2012 overall crime rate, %s is the %s safest city in the U.S." % (city, cityRankString))

    except ValueError:
        i = -1
        #sys.stdout.write (" Due to unreported 2012 crime data, %s isn't ranked." % (city))



#This could be changed to one print statement now, but I don't care.

    #sys.stdout.write ("%s police reported a %.01f percent %s in overall crime in 2012%s. Property crime in the city %s %.01f percent. This is %s from %.0f crimes per 100,000 residents in 2011 to %.0f in 2012. Violent crime %s %.01f percent to %.0f per 100,000 residents." % (city, crPercentChange, crPercentChangeDirection, crimeRateTrend, propertyRateChangeDirection, propertyPercentChange, propertyPercentChangeDirection, propertyCrimeRate2011, propertyCrimeRate2012, violentPercentChangeDirection, violentPercentChange, violentCrimeRate2012))
    #sys.stdout.write (" Based on the 2012 overall crime rate, %s is the %s safest city in the U.S." % (city, cityRankString))
    print ""
    print ""

print "Cities with unreported data:"
for item in unreportedList:
    print "%s, %s" % (item[2], item[0])

"""
#find highest and lowest crime rates
    if crimeRate2012:
        if crimeRate2012 < crimeRateLowest:
            crimeRateLowest = crimeRate2012
            lowestCrimeRateCity = row[2]


    if crimeRate2012:
        if crimeRate2012 > crimeRateHighest:
            crimeRateHighest = crimeRate2012
            highestCrimeRateCity = row[2]

sorted_dictCityCrime = sorted(dictCityCrime.items(), key=operator.itemgetter(1))

for row in ucrData[1:]:
    rankedCityState = "%s, %s" % (row[2], row[1])

    try:
        cityRank = [y[0] for y in sorted_dictCityCrime].index(rankedCityState)
        #print rankedCityState, cityRank
    except ValueError:
        i = -1


print lowestCrimeRateCity, "had the lowest crime rate at %.0f" % crimeRateLowest
print highestCrimeRateCity, "had the highest crime rate at %.0f" % crimeRateLowest
print cityState

    #The total crime rate in Lincoln, NE decreased from 1195 in 2000 to 786 in 2010, a 31.34 percent drop. It's the 4th largest decline in the US, with Burwell, NE leading the nation.

Charlotte police reported a 22 percent increase in overall crime compared to last year. Violent crime rose 37% to 4545 per 100,000 residents.
property crime in the city rose 45%. this is an increse from 3343 to 3443 per 100000 compared to 2011

"""