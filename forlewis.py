# we'll use most of these
from json import loads
import codecs
import datetime
import sys
from labMTsimple.storyLab import *

if __name__ == '__main__':
    lang = 'english'
    # load in the labMT stuff
    labMT,labMTvector,labMTwordList = emotionFileReader(stopval=0.0,fileName='labMT2'+lang+'.txt',returnVector=True)

    d = sys.argv[1]
    date = datetime.datetime.strptime(d,'%d.%m.%y')
    g = open('lewis/{0}.txt'.format(date.strftime('%y%m%d')),'w')
             
    f = sys.stdin
    for line in f:
        try:
            tweet = loads(line)
        except:
            print "failed to load a tweet"
        try:
            if tweet['text']:
                valence,fvec = emotion(tweet['text'],labMT,shift=True,happsList=labMTvector)
                indices = [(str(i)+" ")*e for i, e in enumerate(fvec) if e != 0]
                g.write(str(tweet['id'])+"\t")
                # print tweet['coordinates']['coordinates']
                # print str(tweet['coordinates']['coordinates'])[1:-1].split(',')
                latlon = str(tweet['coordinates']['coordinates'])[1:-1].split(',')
                g.write(str(latlon[1].lstrip())+"\t"+str(latlon[0])+"\t")
                g.write("".join(indices).rstrip())
                g.write("\n")
        except:
            print "something else failed"
            


            
