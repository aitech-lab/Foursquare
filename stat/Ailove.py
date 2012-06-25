#!/usr/bin/python
# coding=utf-8

import sys
import thread
import time
import random
import foursquare
from tokens import ailoveToken 


foursquare.oauth_token = ailoveToken

ailoveVenues = [
    "4eef4722a69d8afe6d089c5a", # кухня
    "4bd168d977b29c74288d8c82", # офис
    "4fae41ede4b0e047b1eeff6d", # продакшен
    "4f96b8f3e4b01cb74e5ce04e", # дизайнерская
   #"4f560d36e4b0cddfc166b921", # lab
    "4fb6695ce4b0be3535decc4b", # lounge
   #"4e86d114754a5ba341cf2bfc", # conference
   #"4f670a81e4b0746beabe27ca", # большая переговорка
   #"4f57362f7b0cb98b6e1abe0c", # SEO
]

ailoveStat = open("data/Ailove.stat.csv", "a")

def collectFriendsCheckins(threadName="") :

    timestamp = str(int(time.time()) - 60*60)    
    
    while True :
    
        print "[RECENT FRIENDS CHECKINS]"
        
        recent = foursquare.checkinsRecent(timestamp)
        try:
            if recent :            
                for checkin in recent['response']['recent'] :
                    print checkin['id'], checkin['user']['firstName'].encode('utf-8') 
                    ailoveStat.write(str(checkin))
                
                    # 1% chance to like
                    if random.randint(0, 100) == 33 :
                        foursquare.checkinsLike(checkin['id'])
        except Exception:
            f = open("Ailove.Error.log", "a")
            f.write(str(recent))
            f.close()
                   
        friendsTimestamp = str(int(time.time()))
        sys.stdout.flush()
        print "sleeping 5 min"
        time.sleep(60)


def checkAiloveVenues(threadName="") :

    timestamp = str(int(time.time()) - 60*60) 
     
    while True :
    
        print "[CHECK AILOVE CHECKINS]"
        
        for venue in ailoveVenues :
            print "[VENUE %s]" % venue
            herenow = foursquare.venueHereNow(venue, timestamp)
            try:
                if herenow :
                    print "here now", herenow['response']['hereNow']['count']
                    for item in herenow['response']['hereNow']['items']:
                        print item['user']['id']
                        print 'relationship' in item['user'] 
                        if 'relationship' not in item['user'] :
                            foursquare.sendFriendRequest(item['user']['id'])
            except Exception:
                f = open("Ailove.Error.log", "a")
                f.write(str(herenow))
                f.close()

        timestamp = str(int(time.time()) - 30)
        sys.stdout.flush()
        # sleep 5 mins
        time.sleep(60)
      

thread.start_new_thread( collectFriendsCheckins, ("thread1",))
thread.start_new_thread( checkAiloveVenues     , ("thread2",))
 
while True :
    time.sleep(600)
    
    
