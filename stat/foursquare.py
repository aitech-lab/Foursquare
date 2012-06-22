# coding=utf-8

import urllib
import httplib
import os
import sys
import simplejson as json

oauth_token = ""
debug = True



def response(resp):
    
    if debug : print resp.status, resp.reason
    
    if (resp.status == 200) :
        return json.loads(resp.read())
    else:
        if debug : print resp.read()
        return False



def venueHereNow(venueId, afterTimestamp="1262325600"):
	
    print "[VENUES %s HERE NOW]" % str(venueId)
    
    conn = httplib.HTTPSConnection("api.foursquare.com");
    conn.request("GET",
        "/v2/venues/%s/herenow"
        "?oauth_oauth_token=%s"
        "&v=20120619"
        "&limit=500"
        "&offset=0"
        "&afterTimestamp=%s"
        % (str(venueId), oauth_token, str(afterTimestamp)))
         
    return response(conn.getresponse())
   


def venuesTrending(lat="55.757801", lng="37.620761", radius="2000"):
    
    print "[VENUES TRENDING AT lat:%s lng:%s R:%s]" % (lat, lng, radius)

    conn = httplib.HTTPSConnection("api.foursquare.com");
    conn.request("GET",
        "/v2/venues/trending"
        "?oauth_oauth_token=%s"
        "&v=20120601"
        "&ll=%s,%s"
        "&limit=50"
        "&radius=%s"
         % (oauth_token, str(lat), str(lng), str(radius)))
    
    return response(conn.getresponse())
   


def sendFriendRequest(userId) : 

    print "[SEND FRIEND REQUEST TO %s]" % userId
    
    conn = httplib.HTTPSConnection("api.foursquare.com")
    conn.request("POST", 
        "/v2/users/%s/request"
        "?oauth_oauth_token=%s" 
        % (str(userId), oauth_token))

    return response(conn.getresponse())
   

   
def getFriends() :
    
    print "[USERS FRIENDS]"

    conn = httplib.HTTPSConnection("api.foursquare.com");
    url = "/v2/users/self/friends"\
        "?oauth_oauth_token=%s"\
        "&v=20120619"\
        % (oauth_tokens.oauth_tokens[1])
    
    conn.request("GET", url)   
    return response(conn.getresponse())
   

      
def checkinsLike(checkinId):  
    
    print "[LIKE %s CHECKIN]" % str(checkinId)
    
    conn = httplib.HTTPSConnection("api.foursquare.com");
    conn.request("POST",
        "/v2/checkins/%s/like"
        "?oauth_oauth_token=%s"
        "&v=20120609"
        "&locale=rf"
        "&set=true"
         % (checkinId, oauth_token))
    return response(conn.getresponse())
   

    
def checkinsRecent(afterTimestamp="1262325600"):

    print "[GET RECENT FRIENTDS CHECKINS]"

    conn = httplib.HTTPSConnection("api.foursquare.com")
    conn.request("GET",
        "/v2/checkins/recent"
        "?oauth_oauth_token=%s"
        "&limit=100"
        "&v=20120619"
        "&afterTimestamp=%s"
         % (oauth_token, str(afterTimestamp)))
    
    return response(conn.getresponse())
   

 
def checkinsAddComment(checkinId, text):

    print "[ADD COMMENT '%s' TO CHECKIN %s]" % (text, checkinId)

    conn = httplib.HTTPSConnection("api.foursquare.com")
    params = urllib.urlencode({
        "oauth_oauth_token" : oauth_token,
        "v"           : 20120619,
        "text"        : text.encode('utf-8')})
    headers = {
        "Content-type" : "application/x-www-form-urlencoded",
        "Accept"       : "text/plain"}
    
    conn.request("POST", "/v2/checkins/%s/addcomment" % str(checkinId), params, headers)
      
    return response(conn.getresponse())

   

def checkinsAdd(venueId, text=''):

    print "[ADD CHECKIN AT '%s' AND SHOUT '%s']" % (venueId, text)

    conn = httplib.HTTPSConnection("api.foursquare.com")
    conn.request("POST",
        "/v2/checkins/add"
        "?oauth_oauth_token=%s"
        "&v=20120601"
        "&venueId=%s"
        "&broadcast=public,twitter,facebook"
        "shout=%s"
        % (oauth_token, venueId, urllib.urlencode(text.encode('utf-8'))))
    return response(conn.getresponse())
   
    
