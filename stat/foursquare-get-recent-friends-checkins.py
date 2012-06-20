import httplib
import sys
sys.path.append('lib/python')

import simplejson as json
import time
import tokens
import random

file = open("data/friends-checkins.txt", "a")

timestamp = int(time.time()) - 60*60*24

while 1 :
    conn = httplib.HTTPSConnection("api.foursquare.com");
    conn.request("GET",
        "/v2/checkins/recent"
        "?oauth_token=%s"
        "&limit=100"
        "&v=20120619"
        "&afterTimestamp=%s"
         % (tokens.tokens[0], str(timestamp)))
    
    resp = conn.getresponse()
    print resp.status, resp.reason
    timestamp = int(time.time())

    if (resp.status == 200) :
        d = json.loads(resp.read())
        for c in d['response']['recent'] :
            uid = str(c['user']['id'])
            vid = str(c['venue']['id'])
            lat = str(c['venue']['location']['lat'])
            lng = str(c['venue']['location']['lng'])
            utm = str(c['createdAt'])

            print uid, " "*(8-len(uid)), vid, lat, " "*(13-len(lat)), lng, " "*(13-len(lng)), utm  
            file.write("%s, %s, %s, %s, %s\n" % (uid, vid, lat, lng, utm))

    # sleep 10 min
    print "sleeping 60sec"
    time.sleep(60)
