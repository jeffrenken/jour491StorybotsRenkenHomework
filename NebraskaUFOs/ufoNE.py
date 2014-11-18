# twitter/NebraskaUFOs
# Reads the Nebraska table from the National UFO Reporting Center and sends a tweet with info and link for any new sighting
# Put ufoNE.txt in the same directory, or I think you can run the program once with the tweet status commented out
# I don't really know what libraries are necessary, nor do I know how the url shortener works. But it works.
# Right now, the Anniversary section isn't included
# For different states only the abbreviations would need to be changed


import urllib, urllib2, string, datetime, time, json

from bs4 import BeautifulSoup
from datetime import datetime
from twython import Twython



html = urllib2.urlopen("http://www.nuforc.org/webreports/ndxlNE.html")

soup = BeautifulSoup(html)


#URL shortening
def goo_shorten_url(url):
    post_url = 'https://www.googleapis.com/urlshortener/v1/url'
    postdata = {'longUrl':url}
    headers = {'Content-Type':'application/json'}
    req = urllib2.Request(
        post_url,
        json.dumps(postdata),
        headers
    )
    ret = urllib2.urlopen(req).read()
    #print ret
    return json.loads(ret)['id']

#get data from table
for tr in soup.find_all('tr')[1:]:
    tds = tr.find_all('td')
    for row in tr.find_all('a'):
        linkID = row.get('href')
        linkID = str(linkID)
        link = "http://www.nuforc.org/webreports/" + linkID
        city = tds[1].text
        summary = tds[5].text
        dateAndTime = tds[0].text

        #remove time from date td
        if ":" in dateAndTime:
            eventTime = dateAndTime[-5:]
            eventDate = ''.join(dateAndTime.split())[:-5].upper()
        else:
            eventDate = dateAndTime
            eventTime = ""

        #remove 2-digit year
        eventMonthAndDay = ''.join(eventDate.split())[:-3].upper()
        currentMonthAndDay = datetime.now().strftime('%m/%d')


        #compare with text file to check for new entries
        if linkID in open('ufoNE.txt', 'rb').read():
            continue
        else:
            shortUrl = goo_shorten_url(link)
            status = "%s %s, %s" % (eventMonthAndDay, city, summary)
            if len(status) > 110:
                status = status[0:110].rstrip() +"... " + shortUrl
            else:
                shortUrl = goo_shorten_url(link)
                status = status.rstrip() + " " + shortUrl
            #print len(status)

            #found something new! print and tweet
            print status
            twitter.update_status(status= status)

            #add new entry to text file
            searchFile = open('ufoNE.txt', 'a+b');
            searchFile.write(linkID + ", " + eventMonthAndDay + ", \n")
            searchFile.close()
            time.sleep(5)
"""
#Anniversary check
        searchFile = open('ufoNE.txt', 'r');

        line = searchFile.readline()
        if currentMonthAndDay in line:
            time.sleep(3)
            shortUrl = goo_shorten_url(link)
            #time.sleep(5)
            status = "Old UFO:%s %s, %s" % (eventDate, city, summary)
            if len(status) > 115:
                status = status[0:115].rstrip() +"... " + shortUrl
            else:
                shortUrl = goo_shorten_url(link)

                status = status.rstrip() + " " + shortUrl

            print status
            #twitter.update_status(status= status)
            searchFile.close()

"""
