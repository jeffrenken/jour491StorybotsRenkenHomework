#The Lincoln Police Crime stats page is fairly awful, so I made this.
#Scrapes the LPD daily crime stats page, and adds stats to a database.
#Tweets from @lincolncartheft the location and description of vehicle whenever 'AUTO THEFT' is reported
#Writes a few sentences based on the type of call and amount
#Emails this paragraph to myself-right now the paragraph is fairly pointless.
#I could easily modify the DB query to return whatever info is necessary.

import urllib, urllib2, string, datetime, time, json, re, sqlite3, sys, smtplib

from bs4 import BeautifulSoup
from datetime import datetime
from twython import Twython
from string import digits
from email.header    import Header
from email.mime.text import MIMEText

######## Twitter ###########
API_KEY = ''
API_SECRET = ''
ACCESS_TOKEN = ''
ACCESS_TOKEN_SECRET = ''
twitter = Twython(API_KEY, API_SECRET, ACCESS_TOKEN, ACCESS_TOKEN_SECRET)


########## Database  ############
sqlite_file = 'lpdcrime.sqlite'
conn = sqlite3.connect(sqlite_file)
c = conn.cursor()
sqlite_file = 'lpdcrime.sqlite'


#html = urllib2.urlopen("http://www.lincoln.ne.gov/city/police/stats/cfsfri.htm")
html = urllib2.urlopen("http://cjis.lincoln.ne.gov/~lpd/cfstoday.htm")

soup = BeautifulSoup(html)
tables = soup.findAll('table')


currentDate = time.strftime("%Y-%m-%d")
dayOfWeek = time.strftime("%A")


########## Auto Theft Section ##########
#Table Name =  lpdautothefttable Columns = location, vehicleDescription, dateReported, dayOfWeek

recent_incidents = tables[4]
incidentsRows = recent_incidents.findAll('tr')

incidents = []
autoRow = []
for row in incidentsRows:
    autoRow.append(row.text)
    tds = row.findAll('td')
    for td in tds:
        incidents.append(td.text)

vehicleLocation = []
vehicleDescription = []
i=0
for row in autoRow:
    if 'AUTO THEFT' in row:
        autoIndex = incidents.index(row)
        description = incidents[autoIndex+7].replace("u", "").replace("\r", " ").replace("\n", "").lstrip()
        vehicleDescription.append(description)
        vehicleLocation.append(row)
        location = (vehicleLocation[i].rstrip()[:-9]).lstrip().rstrip()[32:]
        location = location[10:].lstrip()

        #Check if crime is already in database
        c.execute("SELECT vehicleDescription FROM lpdautothefttable WHERE location=?", (location,))
        testLocation = str(c.fetchone())

        #If not, add to database, and do something else. Probably tweet.
        if testLocation == 'None':

            status = "%s %s" % (location, vehicleDescription[i])
            if len(status) > 140:
                #print len(status)
                status = status[0:139]
            #print len(status)
            twitter.update_status(status= status)
            time.sleep(3)
            print status

            #Add to table, not sure why REPLACE is still there, should be ok to delete it
            c.execute("INSERT OR REPLACE INTO lpdautothefttable (location, vehicleDescription, dateReported, dayOfWeek) VALUES (?,?,?,?)", (location, vehicleDescription[i], currentDate, dayOfWeek))
            print "ADDED to db", status
        i +=1



########### Crimes by Type Section ############
#Table Name =  lpdcrimetable Columns = typeOfCall, amount, dateReported, dayOfWeek

reports_container = tables[3]

rows = reports_container.findAll('tr')
typeOfCall = []
for row in rows:
    tds = row.findAll('td')
    for td in tds:
        typeOfCall.append(td.text)

crimeAmountList = []
i=0
list = []
crimeTypeList = []
for row in typeOfCall[::2]:
    row = row.replace("u", "").replace("\r", "").replace("\n", "")
    crimeAmountList.append(int(row.rstrip()[-3:]))
    list.append(row.rstrip()[:-3])
    result = ''.join(j for j in list[i] if not j.isdigit())
    result = result.replace("-", "").rstrip().lstrip()
    crimeTypeList.append(result)

    if crimeTypeList[i] in row:

        #Check if record is already in database
        c.execute("SELECT amount FROM lpdcrimetable WHERE typeOfCall=? AND dateReported=?", (crimeTypeList[i],currentDate,))
        amount = c.fetchone()
        strAmount = str(amount)
        if strAmount != "None":
            intAmount = int(amount[0])

        #If not in database, add it.
        if strAmount == 'None':
            c.execute("INSERT INTO lpdcrimetable (typeOfCall, amount, dateReported, dayOfWeek) VALUES (?,?,?,?)", (crimeTypeList[i], crimeAmountList[i], currentDate, dayOfWeek))
            print "Added", crimeTypeList[i], crimeAmountList[i]

        #Check if Amount has increased and update
        elif intAmount < crimeAmountList[i]:
            c.execute("UPDATE lpdcrimetable SET amount=? WHERE typeOfCall=? AND dateReported=?", (crimeAmountList[i], crimeTypeList[i], currentDate))
            print "Updated", crimeTypeList[i], crimeAmountList[i]
    i +=1

conn.commit()

#range to select from database
startDate = "2014-12-03"
endDate = "2014-12-10"
c.execute("SELECT typeOfCall, amount, dayOfWeek FROM lpdcrimetable WHERE dateReported BETWEEN ? AND ?", (startDate, endDate))
crimes = c.fetchall()

assault = []
for row in crimes:
    if "ASSAULT" in row:
        assault.append(row)

for row in assault:
    maxAssault = ( max(assault, key=lambda x: x[1]) )
    maxAssaultDay = str(maxAssault[2])
    maxAssaultAmount = int(maxAssault[1])
averageAssaults = (sum(x[1] for x in assault)) / len(assault)
moreAssault = maxAssaultAmount - averageAssaults


burglary = []
for row in crimes:
    if "BURGLARY" in row:
        burglary.append(row)

for row in burglary:
    maxBurglary = ( max(burglary, key=lambda x: x[1]) )
    maxBurglaryDay = str(maxBurglary[2])
    maxBurglaryAmount = int(maxBurglary[1])
averageBurglary = (sum(x[1] for x in burglary)) / len(burglary)
moreBurglary = maxBurglaryAmount - averageBurglary


narcotics = []
for row in crimes:
    if "NARCOTICS" in row:
        narcotics.append(row)

for row in narcotics:
    maxNarcotics = ( max(narcotics, key=lambda x: x[1]) )
    maxNarcoticsDay = str(maxNarcotics[2])
    maxNarcoticsAmount = int(maxNarcotics[1])
totalNarcotics = sum(x[1] for x in narcotics)
averageNarcotics = (sum(x[1] for x in narcotics)) / len(narcotics)
moreNarcotics = maxNarcoticsAmount - averageNarcotics

totalCalls = []
for row in crimes:
    if "TOTAL CALLS" in row:
        totalCalls.append(row)

for row in totalCalls:
    maxCalls = ( max(totalCalls, key=lambda x: x[1]) )
    maxCallsDay = str(maxCalls[2])
    maxCallsAmount = int(maxCalls[1])
allCalls = sum(x[1] for x in totalCalls)
averageCalls = (sum(x[1] for x in totalCalls)) / len(totalCalls)
moreCalls = maxCallsAmount - averageCalls

startDate = datetime.strptime(startDate, '%Y-%m-%d')
startDate = startDate.strftime("%B %w")
endDate = datetime.strptime(endDate, '%Y-%m-%d')
endDate = endDate.strftime("%B %d")

message1 = "From %s to %s, the Lincoln Police Department reported %s total calls.  %s had the most calls reported with %i. The daily average was %i." % (startDate, endDate, allCalls,  maxCallsDay, maxCallsAmount, averageCalls)
message2 = " Lincoln also averaged %i burglary calls per day while %s had the most with %i." % (averageBurglary, maxBurglaryDay, maxBurglaryAmount)
message3 = " You were most likely to be assaulted on %s when there were %s calls, %i more than the daily average of %s." % (maxAssaultDay, maxAssaultAmount, moreAssault, averageAssaults)
message4 = " There were %i narcotics calls." % totalNarcotics
conn.close()

emailMessage = message1 + message2 + message3


######### Email ############

message = emailMessage

GMAIL_USERNAME = ''
GMAIL_PASSWORD = ''
email_subject  = "LPD Crime Story"
recipient = ""

session = smtplib.SMTP('smtp.gmail.com', 587)
session.ehlo()
session.starttls()
session.login(GMAIL_USERNAME, GMAIL_PASSWORD)

headers = "\r\n".join(["from: " + GMAIL_USERNAME,
                       "subject: " + email_subject,
                       "to: " + recipient,
                       "mime-version: 1.0",
                       "content-type: text/html"])

# body_of_email can be plaintext or html!
content = headers + "\r\n\r\n" + message
session.sendmail(GMAIL_USERNAME, recipient, content)
