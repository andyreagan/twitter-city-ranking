from geofunctions import *
from labMTsimple.speedy import *
from censusCities import *
import re

cities = loadCities()
shape_ids = [cities[1].index(city) for city in census_cities]
year = 2011
labMT = sentiDict('LabMT',stopVal=1.0)
# stop_words = ["atlantic", "grand", "green", "falls", "lake", "new", "santa", "haven", "battle", "humid", "humidity", "pressure", "earthquake", "nigga", "niggaz", "niggas", "nigger"]
stop_words = ["atlantic", "grand", "green", "falls", "lake", "new", "santa", "haven", "battle", "nigga", "niggaz", "niggas", "nigger"]

def dictify(tmpStr,wordDict):
    words = [x.lower() for x in re.findall(r"[\w\@\#\'\&\]\*\-\/\[\=\;]+",tmpStr,flags=re.UNICODE)]
    for word in words:
        if word in wordDict:
            wordDict[word] += 1
        else:
            wordDict[word] = 1

city_happs_list = [0.0 for i in range(len(census_cities))]
tweet_count_list = [0.0 for i in range(len(census_cities))]

for i,city in enumerate(census_cities):
    print(city)
    my_id = shape_ids[i]
    city_word_dict = dict()
    total_tweets = 0
    for month in range(12):
        f = open("citytweets/{0}/{1}-{2:02d}.txt".format(my_id,year,month+1),"r")
        # raw_text = f.read()
        # total_tweets += len(raw_text.split("\n"))
        raw_text = ""
        for line in f:
            total_tweets +=1
            raw_text += line.split("\t")[3]
        dictify(raw_text,city_word_dict)
        f.close()
        # test that it's growing (it is)
        # if 'the' in city_word_dict:
        #     print(month)
        #     print(city_word_dict['the'])

    # manually remove stop words (by setting frequency to 0)
    for word in stop_words:
        if word in city_word_dict:
            city_word_dict[word] = 0
    happs = labMT.scoreTrie(city_word_dict)
    print(happs)
    print(total_tweets)
    city_happs_list[i] = happs
    tweet_count_list[i] =  total_tweets

print("sorting")
indexer = sorted(range(len(census_cities)),key=lambda k: city_happs_list[k], reverse=True)
sorted_cities = [(census_cities[i],city_happs_list[i],tweet_count_list[i],shape_ids[i]) for i in indexer]

print("writing out file")
f = open("{0}-list.txt".format(year),"w")
i = 0
for x in sorted_cities:
    city,happs,count,shapeID = x
    i+=1
    f.write("{0}: {1} with happs {2} from {3} tweets (ID={4})\n".format(i,city,happs,count,shapeID))
f.close()
print("done")

