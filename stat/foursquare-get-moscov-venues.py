import time
import thread
import httplib
import simplejson as json
import client

# -*- coding: utf-8 -*-

sectors = []
threadLock = thread.allocate_lock()

# MOSCOW BOUNDS
N = 55.92578046   
E = 37.33204993 
S = 55.55701887   
W = 37.89647254

step = 100.0;
dlng = (N - S) / step
dlat = (W - E) / step

f = open('out.csv', 'w')
f.write("latitude, longitude, checkins, id, name\n")

def drange(start, stop, step):
    r = start
    while r < stop:
        yield r
        r += step

for lat in drange(S, N, dlat) :
    for lng in drange (E, W, dlng) :
        sectors.append([lat, lng])


def foursquareThread(keys) :
    # DOC: https://developer.foursquare.com/docs/venues/search
    
    while(len(sectors)):
        
        s = sectors.pop()
        
        lat = s[0]
        lng = s[1]
        for trycount in range(0, 5) :
            conn = httplib.HTTPSConnection("api.foursquare.com")
            conn.set_debuglevel(3)
            conn.request("GET",          
                "/v2/venues/search" +
                "?client_id="       + str(keys[0]) + 
                "&client_secret="   + str(keys[1]) +    
                "&v=20120601"       +
                "&limit=100"        +
                "&intent=browse"    +
                "&ne="              +str(lat     )+ "," +str(lng     )+
                "&sw="              +str(lat+dlat)+ "," +str(lng+dlng))
            resp = conn.getresponse()
            if (resp != 200) : 
                print resp.status
            
                if(resp.status == 400) :
                    sectors.append(s)    
                    sleep(60)
                    print "try", trycount
                    continue
            break
            
        d = json.loads(resp.read())
        
        threadLock.acquire()
        for v in d["response"]["venues"]:
            print v["id"], v["stats"]["checkinsCount"] 
            f.write(
                str(v['location']['lat'])       +", "+
                str(v['location']['lng'])       +", "+
                str(v["stats"]["checkinsCount"])+", "+
                str(v['id'])                    +", "+
                    v['name'].encode('utf-8')   +"\n")
        threadLock.release()                

try:
    #foursquareThread(keys2)    
    thread.start_new_thread( foursquareThread, (client.keys1,))
    thread.start_new_thread( foursquareThread, (client.keys2,))
    thread.start_new_thread( foursquareThread, (client.keys3,))
    thread.start_new_thread( foursquareThread, (client.keys4,))
except:
    print "Error: unable to start thread"
while 1 :
    pass    
    
    