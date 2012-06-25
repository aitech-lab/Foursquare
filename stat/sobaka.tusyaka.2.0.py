#!/usr/bin/python
# coding=utf-8

import httplib
import sys
sys.path.append('lib/python')

import simplejson as json
import time
from tokens import dogToken 
import random
import foursquare
import thread


foursquare.oauth_token = dogToken

lat, lng        = "55.757801", "37.620761"
recentTimestamp = str(int(time.time())-60*5) # 5 min 
searchFriends   = False
startTime       = int(time.time())


checkinedAlready = []
randomComments = {
    '4bf58dd8d48988d103941735':  # Дом (частный)
     [u"Гав?", u"А что у нас на ужин?", u"Позовешь меня в гости?", u"Я приду в гости?", u"Открывай, я уже под дверью!", u"Я сейчас приду, повисеть на люстре..."],
    '4bf58dd8d48988d1f9941735': # Продовольственный магазин
     [u"Гав?", u"Возмешь мне колбасы? Докторской! Две!", u"Захватишь печенек?", u"Кассирша общитывает, БДИ!", u"А мне возьми ящик ред-була... И резиновых мишек!", u"И чипсов не забудь! Мне крабовый лейс!"],
    '4bf58dd8d48988d16d941735': # Кафе
     [u"Гав?", u"А мне мороженку!", u"Если я задержусь - слопай мою порцию!", u"Хочу фисташек!", u"Закажи мне 'Тропическое наслаждение' с шоколадной крошкой! Я буду скоро.", u"Не оборачивайся, я по соседним столиком!"],
    '4bf58dd8d48988d163941735': # Парк
     [u"Гав?", u"Я тоже люблю гулять!", u"Tут где-то есть скворешник...", u"Деревья и кусты - моя страсть!", u"A я тебя только что видела!"] 
    }


def addRandomComment(checkinId, categoryId) :
    print "\tADD RANDOM COMMENT"
    if str(categoryId) in randomComments :
        foursquare.checkinsAddComment(checkinId, randomComments[str(categoryId)][random.randint(0, len(randomComments)-1)])
    


def checkFriendsCheckins(threadName="") :
    
    global recentTimestamp

    while True :
        print "[CHECK FRIENDS CHECKINS]"
        recent = foursquare.checkinsRecent(recentTimestamp)
        if recent :            
            for checkin in recent['response']['recent'] :
                print checkin['id']
                # 10% chance to comment
                if random.randint(0, 100) > 90 :
                    checkinId  = str(checkin['id'])
                    categories = checkin['venue']['categories']
                    foursquare.checkinsLike(checkinId)
                    if len(categories) > 0 :
                        addRandomComment(checkinId, categories[0]['id'])
                           
        recentTimestamp = str(int(time.time()))

        print "sleeping 10 min"
        time.sleep(300)



def findNewPlaceToCheckin(threadName=""):
    
    global lat, lng
    global checkinedAlready
    global startTime

    while True:
        print "[FIND NEW PLACE CHECKINS]"
        # SEARCHING TREND CHEKCIN AND FIENDING   
        trending = foursquare.venuesTrending(lat, lng)
        if trending:
            for venue in trending['response']['venues']:
                lat = str(venue['location']['lat'])
                lng = str(venue['location']['lng'])
                print venue['id'], venue['hereNow']['count'], lat, lng  
            
                if venue['id'] not in checkinedAlready :
                
                    checkin = foursquare.checkinsAdd(venue['id'])
                    checkinedAlready.append(venue['id'])
                
                    # 10% chance to find new friend
                    if searchFriends and random.randint(0, 100) > 90 : 
                        herenow = foursquare.venueHereNow(venue['id'])
                        if herenow :
                            print "here now",herenow['response']['hereNow']['count']
                
                            for item in herenow['response']['hereNow']['items']:
                                print item['id'], item['type'], item['user']['id'], item['user']['firstName'] 
                                foursquare.sendFriendRequest(item['user']['id'])
                                break          
                    break # from venues 
        
        # reset day
        if (int(time.time()) - startTime) > 60*60*24 :
            checkinedAlready = []
            startTime = int(time.time())

        print "sleeping 15-60 min"
        time.sleep(random.randint(300,1800))



thread.start_new_thread( findNewPlaceToCheckin, ("thread1",))
thread.start_new_thread( checkFriendsCheckins , ("thread2",))

while True :
    time.sleep(300)
