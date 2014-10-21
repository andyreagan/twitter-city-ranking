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
        splitline = line.rstrip().split("\t")
        tweettext = splitline[2]
        tweetcoor = splitline[0]
        userid = splitline[1]
        valence,fvec = emotion(tweettext,labMT,shift=True,happsList=labMTvector)
        indices = [(str(i)+" ")*e for i, e in enumerate(fvec) if e != 0]
        g.write(str(userid)+"\t")
        latlon = tweetcoor[1:-1].split(',')
        g.write(str(latlon[1].lstrip())+"\t"+str(latlon[0])+"\t")
        g.write("".join(indices).rstrip())
        g.write("\n")


            
