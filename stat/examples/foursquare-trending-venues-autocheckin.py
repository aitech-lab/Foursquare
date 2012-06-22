import httplib
import simplejson as json
import time
import token

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
         % (token, lat, lng))
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
                "&shout=%s"
                % (token, v['id'], "%D1%81%D0%BE%D0%B1%D0%B0%D0%BA%D0%B0-%D1%82%D1%83%D1%81%D1%8F%D0%BA%D0%B0"))
            resp = conn.getresponse()
            print resp.status, resp.reason
            d = resp.read();
            # print d
            break
    # sleep 10 min
    print "sleeping 10 mins"
    time.sleep(600)

raw_input("Press Enter to continue...")
