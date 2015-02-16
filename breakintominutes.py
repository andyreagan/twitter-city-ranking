# processTweetsNew.py
# crawl the tweets, and compute the labMT vectors around keywords
# output with daily resolution
#
# NOTES
# uses the new 15-minute compressed format
# 
# USAGE 
# gzip -cd tweets.gz | python minutelyChopper.py
#  
# this will read the tweets from stdin
# and save them in minutely files

# we'll use most of these
from json import loads
import codecs
import datetime
import sys
import os

def chop():
    f = sys.stdin
    for line in f:
        try:
            tweet = loads(line)
        except:
            print "failed to load a tweet"
        try:
            if tweet['created_at']:
                d = datetime.datetime.strptime(tweet['created_at'],'%a %b %d %H:%M:%S +0000 %Y')-datetime.timedelta(hours=5)
                # newer folder format
                g = open('minutely/{0}/{1}'.format(d.strftime('%Y-%m-%d'),d.strftime('twitter.%S.%M.%H.%d.%y.json')),'a')
                # g = open('minutely/{0}/{1}'.format(d.strftime('%d.%m.%y'),d.strftime('twitter.%S.%M.%H.%d.%y.json')),'a')
                g.write(line)
                g.close()
        except:
            # print "no text"
            pass

    f.close()

def makedirectories(year):
    d = datetime.datetime(year,1,1)
    e = datetime.datetime(year+1,1,1)
    while d < e:
        if not os.path.isdir('minutely/{0}'.format(d.strftime('%Y-%m-%d'))):
            print 'making directory minutely/{0}'.format(d.strftime('%Y-%m-%d'))
            os.mkdir('minutely/{0}'.format(d.strftime('%Y-%m-%d')))
        else:
            print 'directory minutely/{0} exists'.format(d.strftime('%Y-%m-%d'))
        d += datetime.timedelta(days=1)

def renameraw(year):
    d = datetime.datetime(year,1,1)
    e = datetime.datetime(year+1,1,1)
    while d < e:
        if os.path.isfile('zipped-raw/{0}.geo.json'.format(d.strftime('%d.%m.%y'))):
            print 'zipped-raw/{0}.geo.json exists'.format(d.strftime('%d.%m.%y'))
            print 'move to zipped-raw/{0}.geo.json'.format(d.strftime('%Y-%m-%d'))
            os.rename('zipped-raw/{0}.geo.json'.format(d.strftime('%d.%m.%y')),'zipped-raw/{0}.geo.json'.format(d.strftime('%Y-%m-%d')))
        d += datetime.timedelta(days=1)


if __name__ == '__main__':
    # makedirectories(2014)
    # renameraw(2014)
    chop()







