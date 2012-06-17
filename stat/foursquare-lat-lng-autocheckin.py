import httplib
import token
import simplejson as json
import time
import csv
import urllib

file = open('data/lat-lng.csv','r')
data = csv.reader(file, delimiter=',')

for row in data:
    conn = httplib.HTTPSConnection("api.foursquare.com");
    conn.request("GET", 
        "/v2/venues/search"
        "?oauth_token=%s"
        "&v=20120601"
        "&ll=%s,%s"
         % (token,  str(row[1]), str(row[0])))
    resp = conn.getresponse()
    print resp.status, resp.reason

    d = json.loads(resp.read());
    # f = open('venues.txt', 'w'); f.write(str(d)); f.close(); 
    # break;

    url= "/v2/checkins/add?oauth_token=%s&v=20120601&ll=%s,%s&venueId=%s" % (token, str(row[1]), str(row[0]), str(d['response']['venues'][0]['id']))
    conn.request("POST", url) 
    resp = conn.getresponse()
    print url, resp.status, resp.reason
    d = resp.read();
    # print d
    # sleep 10 min
    print "sleeping 30 sec"
    time.sleep(5)
raw_input("Press Enter to continue...")
