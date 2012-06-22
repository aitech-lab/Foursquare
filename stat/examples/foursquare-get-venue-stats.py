import httplib
import sys
sys.path.append('lib/python')

import simplejson as json
import time
import token
import random

timestamp = int(time.time()) - 60*60*24
# ailove_id
venue_id = "4bd168d977b29c74288d8c82"

while 1 :
    conn = httplib.HTTPSConnection("api.foursquare.com");
    conn.request("GET",
        "/v2/venues/%s/stats"
        "?oauth_token=%s"
        "&v=20120619"
         % (venue_id, token.token))
    
    resp = conn.getresponse()
    print resp.status, resp.reason
    timestamp = int(time.time())

    print resp.read()    

    # sleep 10 min
    print "sleeping 60sec"
    time.sleep(60)
