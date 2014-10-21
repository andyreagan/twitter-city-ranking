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

if __name__ == '__main__':
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
                # g = open('minutely-raw/{0}/{1}'.format(d.strftime('%Y-%m-%d'),d.strftime('twitter.%S.%M.%H.%d.%y.json')),'a')
                g = open('minutely-raw2/{0}/{1}'.format(d.strftime('%d.%m.%y'),d.strftime('twitter.%S.%M.%H.%d.%y.json')),'a')
                g.write(line)
                g.close()
        except:
            # print "no text"
            pass

    f.close()







