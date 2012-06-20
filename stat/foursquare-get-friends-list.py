import httplib
import sys
sys.path.append('lib/python')

import simplejson as json
import time
import csv

import tokens

# ailove_id
venue_id = "4bd168d977b29c74288d8c82"
friends  = []
checkiners = []
checkiners_file = open("data/ailove-checkiners.db", "a")

print tokens.tokens[0]
print tokens.tokens[1]

def sendFriendRequest(uid) : 
    print "SEND FRIEND REQUEST TO", uid
    
    conn = httplib.HTTPSConnection("api.foursquare.com");
    url  = "/v2/users/%s/request?oauth_token=%s&v=20120619" % (str(uid), tokens.tokens[0])
    print url
    conn.request("POST", url)
    resp = conn.getresponse()
    print resp.status, resp.reason
    print resp.read() 
       
def getFriends() :
    
    print "FRIENDS"

    conn = httplib.HTTPSConnection("api.foursquare.com");
    url = "/v2/users/self/friends"\
        "?oauth_token=%s"\
        "&v=20120619"\
        % (tokens.tokens[1])
    
    conn.request("GET", url)   
    resp = conn.getresponse()
    
    if (resp.status == 200) :
        d = json.loads(resp.read())
        
        for f in d['response']['friends']['items'] :
            friends.append(f['id'])
            print  f['id']

        return True

    else :
        print resp.read()
        return False

print getFriends()
for f in friends :
    sendFriendRequest(f)
