# coding=utf-8

import urllib
import httplib
import os
import sys
import simplejson as json

token = ""

def venueHereNow(venueId, afterTimestamp="1262325600"):
	
    print "[VENUES %s HERE NOW]" % str(venueId)
    
    conn = httplib.HTTPSConnection("api.foursquare.com");
    conn.request("GET",
        "/v2/venues/%s/herenow"
        "?oauth_token=%s"
        "&v=20120619"
        "&limit=500"
        "&offset=0"
        "&afterTimestamp=%s"
        % (str(venueId), token, str(afterTimestamp)))
         
    resp = conn.getresponse()
    print resp.status, resp.reason
    
    if (resp.status == 200) :
        return json.loads(resp.read())
    else :
        return False



def venuesTrending(lat="55.757801", lng="37.620761", radius="2000"):
    
    print "[VENUES TRENDING AT lat:%s lng:%s R:%s]" % (lat, lng, radius)

    conn = httplib.HTTPSConnection("api.foursquare.com");
    conn.request("GET",
        "/v2/venues/trending"
        "?oauth_token=%s"
        "&v=20120601"
        "&ll=%s,%s"
        "&limit=50"
        "&radius=%s"
         % (token, str(lat), str(lng), str(radius)))
    resp = conn.getresponse()
    print resp.status, resp.reason

    if (resp.status == 200) :
        return json.loads(resp.read())
    else :
        return False



def sendFriendRequest(userId) : 

    print "[SEND FRIEND REQUEST TO %s]" % userId
    
    if (uid not in friends) :
        conn = httplib.HTTPSConnection("api.foursquare.com")
        conn.request("POST", 
            "/v2/users/%s/request"
            "?oauth_token=%s" 
            % (str(userId), token))
        resp = conn.getresponse()
        print resp.status, resp.reason

        if (resp.status != 200) :
            return json.loads(resp.read())
        else:
    	    return False


   
def getFriends() :
    
    print "[USERS FRIENDS]"

    conn = httplib.HTTPSConnection("api.foursquare.com");
    url = "/v2/users/self/friends"\
        "?oauth_token=%s"\
        "&v=20120619"\
        % (tokens.tokens[1])
    
    conn.request("GET", url)   
    resp = conn.getresponse()
    
    if (resp.status == 200) :
        return json.loads(resp.read())
    else:
        return False
    

      
def checkinsLike(checkinId):  
    
    print "[LIKE %s CHECKIN]", str(checkinId)
    
    conn = httplib.HTTPSConnection("api.foursquare.com");
    conn.request("POST",
        "/v2/checkins/%s/like"
        "?oauth_token=%s"
        "&v=20120609"
        "&locale=rf"
        "&set=true"
         % (checkinId, token))
    resp = conn.getresponse()
    print resp.status, resp.reason
 
    if (resp.status == 200) :
        return json.loads(resp.read())
    else:
        return False
 
  
    
def checkinsRecent(afterTimestamp="1262325600"):

    print "[GET RECENT FRIENTDS CHECKINS]"
	
    conn = httplib.HTTPSConnection("api.foursquare.com")
    conn.request("GET",
        "/v2/checkins/recent"
        "?oauth_token=%s"
        "&limit=100"
        "&v=20120619"
        "&afterTimestamp=%s"
         % (token, str(afterTimestamp)))
    
    resp = conn.getresponse()
    print resp.status, resp.reason
    
    if (resp.status == 200) :
        return json.loads(resp.read())
    else:
        return False


 
def checkinsAddComment(checkinId, text):

    print "[ADD COMMENT '%s' TO CHECKIN %s]" % (text, checkinId)
	
    conn = httplib.HTTPSConnection("api.foursquare.com")
    params = urllib.urlencode({
        "oauth_token" : token,
        "v"           : 20120619,
        "text"        : text.encode('utf-8')})
    headers = {
        "Content-type" : "application/x-www-form-urlencoded",
        "Accept"       : "text/plain"}
    
    conn.request("POST", "/v2/checkins/%s/addcomment" % str(checkinId), params, headers)
      
    resp = conn.getresponse()
    print resp.status, resp.reason
    
    if (resp.status == 200) :
        return json.loads(resp.read())
    else:
        print resp.read()
        return False
        

 
def checkinsAdd(venueId, text='')

    print "[ADD CHECKIN AT '%s' AND SHOUT '%s']" % (venueId, text)
	
    conn = httplib.HTTPSConnection("api.foursquare.com")
    conn.request("POST",
        "/v2/checkins/add"
        "?oauth_token=%s"
        "&v=20120601"
        "&venueId=%s"
        "&broadcast=public,twitter,facebook"
        "shout=%s"
        % (token, venueId, urllib.urlencode(text.encode('utf-8')))
    resp = conn.getresponse()
    print resp.status, resp.reaso
