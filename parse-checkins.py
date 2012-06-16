import simplejson as json

o = open("out-checkins.csv", "w")
for i in range(0,10) :
    print "--- ", i, " ---"
    f = open("data/checkins."+str(i)+".json", "r");
    d = json.loads(f.read());
    for c in d['response']['checkins']['items']:
        row = str(c["createdAt"])               +", "+\
              str(c["venue"]["location"]["lat"])+", "+\
              str(c["venue"]["location"]["lng"])+"\n"
        o.write(row);   
o.close()