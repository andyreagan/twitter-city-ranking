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

def tweetreader(tweettext,keyWords,freqList,labMT,labMTvector,labMTfreqList):
    for i in xrange(len(keyWords)):
        if re.search(r"\b%s\b" % keyWords[i],tweettext) is not None:
            # print "found "+keyWords[i]
            freqList[i] += 1
            # find labMT words and add to labMT vector
            valence,fvec = emotion(tweettext,labMT,shift=True,happsList=labMTvector)
            labMTfreqList[i] += numpy.array(fvec)
        # ends re match test
    # ends for len(keyWords)

def gzipper(freqList,labMTfreqList,keyWords):
    lang = 'english'
    # load in the labMT stuff
    labMT,labMTvector,labMTwordList = emotionFileReader(stopval=0.0,fileName='labMT2'+lang+'.txt',returnVector=True)

    f = sys.stdin
    for line in f:
        try:
            tweet = loads(line)
        except:
            print "failed to load a tweet"
        try:
            if tweet['text']:
                tweetreader(tweet['text'],keyWords,freqList,labMT,labMTvector,labMTfreqList)
        except:
            # print "no text"
            pass

if __name__ == '__main__':
    # load the things
    datestring = sys.argv[1]
    eventName = sys.argv[2]
  
    # read in more things
    eventFolder = '/users/a/r/areagan/fun/twitter/emily/{}'.format(eventName)
    f = codecs.open('/users/a/r/areagan/fun/twitter/emily/{}.txt'.format(eventName),'r','utf8')
    keyWords = [line.rstrip().lower() for line in f]
    f.close()
  
    # check these are the right keywords!
    print "the keywords are"
    print keyWords
  
    # folder names replace [& with and, ' with nothing, spaces with -]
    folderNames = ['{0}/{1}'.format(eventFolder,re.sub('&','and',re.sub('\'','',re.sub('\s','-',keyword)))) for keyword in keyWords]
    print folderNames
  
    # format date
    date = datetime.datetime.strptime(datestring,'%Y-%m-%d')
    
    # freqList will store everything
    # [keyword][minute][labMTindex]
    # freqList = [[[0 for i in xrange(10222)] for i in xrange(1440)] for key in keyWords]
    labMTfreqList = [numpy.zeros(10222) for key in xrange(len(keyWords))]
    freqList = [0.0 for key in xrange(len(keyWords))]
    # fname = date.strftime('/users/c/d/cdanfort/scratch/twitter/tweet-troll/zipped-raw/%d.%m.%Y.tgz')
    # print fname
    gzipper(freqList,labMTfreqList,keyWords)
  
    print "complete"
  
    # dump this to the screen in case something goes wrong
    # print freqList
    # print labMTfreqList
  
    for i in xrange(len(keyWords)):
        f = open('{0}/{1}-frequency-{2}.csv'.format(folderNames[i],date.strftime('%Y-%m-%d'),i),'w')
        f.write('{0:.0f}\n'.format(freqList[i]))
        f.close()
  
        f = open('{0}/{1}-word-vector-{2}.csv'.format(folderNames[i],date.strftime('%Y-%m-%d'),i),'w')
        f.write('{0:.0f}'.format(labMTfreqList[i][0]))
        for j in xrange(1,len(labMTfreqList[i])):
            f.write(',{0:.0f}'.format(labMTfreqList[i][j]))
        f.write('\n')
        f.close()







