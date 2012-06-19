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


def getFriends() :
    
    print "FRIENDS"

    conn = httplib.HTTPSConnection("api.foursquare.com");
    url = "/v2/users/self/friends"\
        "?oauth_token=%s"\
        "&v=20120619"\
        "&limit=500"\
        "&offset=0"\
        % (tokens.tokens[0])
    
    #print "https://api.foursquare.com"+url;
    conn.request("GET", url)   
    resp = conn.getresponse()
    print resp.status, resp.reason

    if (resp.status == 200) :
        d = json.loads(resp.read())
        
        for f in d['response']['friends']['items'] :
            friends.append(int(f['id']))
            print  f['id']

        return True

    else :
        print resp.read()
        return False

def loadCheckiners() :
    print "LOAD CHECKINERS"

    for line in open('data/ailove-checkiners.db','r'):
        checkiners.append(int(line))
        print line

def sendFriendRequest(uid) : 
    print "SEND FRIEND REQUEST TO", uid
    if (uid not in friends) :
        conn = httplib.HTTPSConnection("api.foursquare.com");
        url = "/v2/users/%s/request?oauth_token=%s" % (str(uid), tokens.tokens[0])
        print url
        conn.request("POST", url)
        resp = conn.getresponse()
        print resp.status, resp.reason
        if (resp.status != 200) :
            print resp.read() 
        friends.append(uid)    

def getCheckins() :

    print "AILOVE CHECKINS"

    conn = httplib.HTTPSConnection("api.foursquare.com");
    url = "/v2/venues/"+venue_id+"/herenow"\
        "?oauth_token=%s"\
        "&v=20120619"\
        "&limit=500"\
        "&offset=0"\
        "&afterTimestamp=1262325600"\
        % (tokens.tokens[0])
    
    # print "https://api.foursquare.com"+url;
    conn.request("GET", url)
         
    resp = conn.getresponse()
    print resp.status, resp.reason
    
    if (resp.status == 200) :
        d = json.loads(resp.read())
        for c in d['response']['hereNow']['items'] :
            uid = int(c['user']['id'])
            print uid, c['user']['relationship']

            if(uid not in checkiners) :
                print  "new checkiner ", uid
                checkiners_file.write(str(uid) + "\n");
                checkiners.append(uid)

            if (c['user']['relationship'] != "friend") :
                sendFriendRequest(uid)
    else :
        print resp.read()


# print getFriends()
loadCheckiners()
while 1 :
    getCheckins()
    print "sleeping 60 sec"
    time.sleep(60)

