import httplib
import sys
sys.path.append('lib/python')

import simplejson as json
import time
import token
import random

checkin_ids = set()
checkin_file = open("checkins_ids.txt","a")
lat, lng = "55.757801", "37.620761"

while 1 :
    conn = httplib.HTTPSConnection("api.foursquare.com");
    conn.request("GET",
        "/v2/venues/trending"
        "?oauth_token=%s"
        "&v=20120601"
        "&ll=%s,%s"
        "&limit=50"
        "&radius=2000"
         % (token.token, lat, lng))
    resp = conn.getresponse()
    print resp.status, resp.reason

    d = json.loads(resp.read())
    f = open("trending.txt", "w"); f.write(str(d)); f.close()
    for v in d['response']['venues']:
        lat = str(v['location']['lat'])
        lng = str(v['location']['lng'])
        print v['id'], v['hereNow']['count'], lat, lng
        if(v['id'] not in checkin_ids) :
            checkin_ids.add(v['id'])
            checkin_file.write(v['id']+"\n")
            conn.request("POST",
                "/v2/checkins/add"
                "?oauth_token=%s"
                "&v=20120601"
                "&venueId=%s"
                "&broadcast=public,twitter,facebook"
                % (token.token, v['id']))
            resp = conn.getresponse()
            print resp.status, resp.reason
            d = resp.read();
            # print d
            break
    # sleep 10 min
    print "sleeping 15-60 min"
    time.sleep(random.randint(900,3600))
