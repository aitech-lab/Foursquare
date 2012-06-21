#!/usr/bin/python
# coding=utf-8

import httplib
import sys
sys.path.append('lib/python')

import simplejson as json
import time
import token
import random
import foursquare

foursquare.token = "YYVGOD3L1YAUHAMUQBBCN22UQMC1F1I51ZPRJFGX2ENMDDTR"

lat, lng = "55.757801", "37.620761"

while 1 :
   
    trending = foursquare.venuesTrending(lat, lng)
    if trending:
        for venue in trending['response']['venues']:
            lat = str(venue['location']['lat'])
            lng = str(venue['location']['lng'])
            print venue['id'], venue['hereNow']['count'], lat, lng, venue['name']
            
            foursquare.checkinsAdd(venue['id'])
            
            herenow = foursquare.venueHereNow(venue['id'])
            if herenow :
                print "here now",herenow['response']['hereNow']['count']
                
                for item in herenow['response']['hereNow']['items']:
                    print item['id'], item['type'], item['user']['id'], item['user']['firstName'] 
                    foursquare.sendFriendRequest(item['user']['id'])
                    
                    break
                    
                             
            break
            #if(v['id'] not in checkin_ids) :
            #    checkin_ids.add(v['id'])
            #    checkin_file.write(v['id']+"\n")
            #    conn.request("POST",
            #        "/v2/checkins/add"
            #        "?oauth_token=%s"
            #       "&v=20120601"
            #       "&venueId=%s"
            #        "&broadcast=public,twitter,facebook"
            #        % (token.token, v['id']))
            #    resp = conn.getresponse()
            #    print resp.status, resp.reason
            #    d = resp.read();
            #    # print d
    
    # sleep 10 min
    print "sleeping 15-60 min"
    time.sleep(random.randint(900,3600))
