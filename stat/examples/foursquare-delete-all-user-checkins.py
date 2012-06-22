import httplib
import simplejson as json
import time

# Code needs access token 
import tokens

count   = 1000
counter = 0
i = 0
checkins = []
while counter<=count:
    
    conn = httplib.HTTPSConnection("api.foursquare.com");    
    conn.request("GET", 
        "/v2/users/self/checkins"
        "?oauth_token=%s"
        "&v=20120601"
        "&limit=250"
        "&offset=%s"
        % (tokens.tokens[0],str(250*i)))
    resp = conn.getresponse()
    print resp.status, resp.reason
    if (resp.status == 200) :
        d = json.loads(resp.read())
        count = int(d["response"]["checkins"]["count"])
        for c in d["response"]["checkins"]["items"] :
            checkins.append(c["id"])
            print counter,"\t",c["id"]
            counter+=1
    i+=1
for cid in checkins:

    print "delete", cid
    conn = httplib.HTTPSConnection("api.foursquare.com");    
    conn.request("POST", 
        "/v2/checkins/%s/delete"
        "?oauth_token=%s"
        "&v=20120601"
        % (str(cid),"HERE_MUST_BE_A_TOKEN_GRABED_FROM_FSQ_SITE"))
    resp = conn.getresponse()
    print resp.status, resp.reason

raw_input("Press Enter to continue...")

