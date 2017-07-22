#!/usr/bin/env python
import sys
from twitter import *
import datetime
import time

# your twitter consumer and access information goes here
# note: these are garbage strings and won't work
apiKey = '***'
apiSecret = '***'
accessToken = '***'
accessTokenSecret = '***'

timelist = []


def authenticate():
    apiobject = Twitter(auth = OAuth(accessToken, accessTokenSecret ,apiKey ,apiSecret ))
    return apiobject

def newTweet(apiobject):
    #twitter = authenticate()
    twitter = apiobject
    tweetStr = "Intrusion detected at : " + str(datetime.datetime.now())
    twitter.statuses.update(status = tweetStr)
    print("updated status: %s" % tweetStr)

def sendMessage(apiobject,phnum):
    #twitter = authenticate()
    twitter = apiobject
    user = "AnkamManikanta"
    twitter.direct_messages.new(screen_name = user, text="Hi there Mania , I got a request from " + phnum )

def findCommand(apiobject):

    #twitter = authenticate()
    global timelist
    twitter = apiobject
    user = "AnkamManikanta"
    results = twitter.statuses.user_timeline(screen_name = user, count=1)
    for status in results:
        if("#rpi6191_takerest" in status["text"]):
            time1 = status["created_at"]
            print(timelist)
            if not (time1 in timelist):
                timelist.append(time1)
                print("tag present")
                #return time1,True
                return True
            else:
                #return time1,False
                return False

        else:
            print("tag absent")
            #return 0,False
            return False

        #get time1 from status["created_at"]
