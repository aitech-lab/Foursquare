import httplib
import simplejson as json
import time

# Code needs access token 
import token

for i in range(0, 10) :

    conn = httplib.HTTPSConnection("api.foursquare.com");    
    conn.request("GET", 
        "/v2/users/self/checkins"
        "?oauth_token=%s"
        "&v=20120601"
        "&limit=250"
        "&offset=%s"
        % (token,str(250*i)))
    resp = conn.getresponse()
    print resp.status, resp.reason
    f = open("data/user-checkins."+str(i)+".json", 'w')
    f.write(resp.read())
    f.close()

raw_input("Press Enter to continue...")

