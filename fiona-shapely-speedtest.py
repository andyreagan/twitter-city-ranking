# load all of the geometries
import fiona
from shapely.geometry import Point,Polygon,MultiPolygon
from shapely import speedups
speedups.enable()

# we'll use most of these
from json import loads
import codecs
import datetime
# import re
# import numpy
# from labMTsimple.storyLab import *
import sys

def loadCities():
    c = fiona.open('shapefiles/cb_2013_us_ua10_500k.shp','r')
    polygonList = []
    nameList = []
    polygonCount = 0
    multiPolygonCount = 0
    for city in list(c):
        nameList.append(city['properties']['NAME10'])
        if city['geometry']['type'] == 'Polygon':
            polygonCount += 1
            coordinates = city['geometry']['coordinates']
            polygonList.append(Polygon(coordinates[0]))
        elif city['geometry']['type'] == 'MultiPolygon':
            multiPolygonCount += 1
            coordinates = city['geometry']['coordinates']
            coordinates_w_holes = [(tuple(c[0]),()) if len(c) == 1 else (tuple(c[0]),(c[1:])) for c in coordinates]
            polygonList.append(MultiPolygon(coordinates_w_holes))
        else:
            raise('unknown geometry ' % city['geometry']['type'])
    print('done loading')
    return polygonList,nameList

def cityID(polygonList,pt):
    for i,city in enumerate(polygonList):
        if city.contains(pt):
            return i
    return -1

def gzipper(polygonList,nameList,outfile):
    lineCount = 0
    tweetCount = 0
    geoCount = 0
    geoLocatedCount = 0
    f = sys.stdin
    for line in f:
        lineCount += 1
        try:
            tweet = loads(line)
            tweetCount +=1 
        except:
            print("failed to load a tweet")
        geo_tweet_bool = False
        myCityCoords = []
        try:
            if tweet['coordinates']:
                myCityCoords = tweet['coordinates']['coordinates']
                geo_tweet_bool = True
            elif tweet['geo']:
                myCityCoords = tweet['geo']['coordinates']
                geo_tweet_bool = True
        except:
            pass
        if geo_tweet_bool:
            geoCount += 1
            myPt = Point(myCityCoords)
            myCityID = cityID(polygonList,myPt)
            if myCityID > -1:
                # print(nameList[myCityID])
                geoLocatedCount += 1
                f = codecs.open('citytweets/{0}/{1}.txt'.format(myCityID,outfile),'a','utf8')
                f.write("{0}\t{1}\t{2}\t".format(tweet['user']['id'],myCityCoords[0],myCityCoords[1]))
                # tweettext = unicode(tweet['text'])
                # f.write(tweet['text']) # .replace('\n',' ').replace('\t',' '))
                f.write(tweet['text'].replace('\n',' ').replace('\t',' '))
                f.write("\n")
                f.close()
            else:
                pass
    print('read {0} lines, {1} tweets, and classified {3} of {2} geotweets'.format(lineCount,tweetCount,geoCount,geoLocatedCount))

if __name__ == '__main__':
    date = datetime.datetime.strptime(sys.argv[1],'%Y-%m-%d')
    polygonList,nameList = loadCities()
    gzipper(polygonList,nameList,date.strftime('%Y-%m'))
    


