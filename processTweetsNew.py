# processTweetsNew.py
# crawl the tweets, and compute the labMT vectors around keywords
# output with daily resolution
#
# NOTES
# uses the new 15-minute compressed format
# 
# USAGE 
# gzip -cd tweets.gz | python processTweetsNew.py 2014-01-01 keywords
#  
# this will read keywords.txt and the tweets from stdin
# and save a frequency file, labMT vector in keywords/[keyword]
# for each keyword

# we'll use most of these
from json import loads
import codecs
import datetime
import re
import numpy
from labMTsimple.storyLab import *
import sys

def tweetreader(tweettext,keyWords,g):
    for i in xrange(len(keyWords)):
        if re.search(r"\b%s\b" % keyWords[i],tweettext,flags=re.IGNORECASE) is not None:
            g.write(tweettext.replace('\n',' '))
            g.write('\n')
        # ends re match test
    # ends for len(keyWords)

def gzipper(keyWords,outfile):
    f = sys.stdin
    for line in f:
        try:
            tweet = loads(line)
        except:
            print "failed to load a tweet"
        try:
            if tweet['text']:
                tweetreader(tweet['text'],keyWords,outfile)
        except:
            # print "no text"
            pass

if __name__ == '__main__':
    # load the things
    outfile = sys.argv[1]
    
    keyWords = ['climate',]
    keyWords = ['clinton','sanders','omalley','webb','chaffee','cruz','rand paul','rubio','carson','fiorina','huckabee','santorum',]
    
    g = open('rawtweets/{0}.txt'.format(outfile),'w')
    gzipper(keyWords,g)
    g.close()
    print "complete"
  







