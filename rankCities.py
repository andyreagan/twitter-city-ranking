from geofunctions import *
from labMTsimple.speedy import *
from censusCities import *
import re

def dictify(tmpStr,wordDict):
    words = [x.lower() for x in re.findall(r"[\w\@\#\'\&\]\*\-\/\[\=\;]+",tmpStr,flags=re.UNICODE)]
    for word in words:
        if word in wordDict:
            wordDict[word] += 1
        else:
            wordDict[word] = 1

if __name__ == '__main__':            
    # year = 2012
    year = int(sys.argv[1])
    print(year)
    cities = loadCities()
    shape_ids = [cities[1].index(city) for city in census_cities]
    labMT = sentiDict('LabMT',stopVal=1.0)
    # strike all words from the dataset
    # stop_words = ["atlantic", "grand", "green", "falls", "lake", "new", "santa", "haven", "battle", "humid", "humidity", "pressure", "earthquake", "nigga", "niggaz", "niggas", "nigger"]
    # strike the non-bot words from the dataset
    # stop_words = ["atlantic", "grand", "green", "falls", "lake", "new", "santa", "haven", "battle", "nigga", "niggaz", "niggas", "nigger"]
    # strike just the n-words
    stop_words = ["nigga", "niggaz", "niggas", "nigger"]
    bot_words = ["humid", "humidity", "pressure", "earthquake",]
    strike_city_names = True
    
    city_happs_list = [0.0 for i in range(len(census_cities))]
    tweet_count_list = [0.0 for i in range(len(census_cities))]
    
    for i,city in enumerate(census_cities):
        if strike_city_names:
            # break down the city name
            city_words = [x.lower() for x in re.findall(r"[\w]+",city,flags=re.UNICODE)]
            # append them to just the n-words
            stop_words = ["nigga", "niggaz", "niggas", "nigger"]
            stop_words.extend(city_words)
        my_id = shape_ids[i]
        user_word_dict = dict()
        total_tweets = 0
        for month in range(12):
            f = open("citytweets/{0}/{1}-{2:02d}.txt".format(my_id,year,month+1),"r")
            # raw_text = f.read()
            # total_tweets += len(raw_text.split("\n"))
            for line in f:
                # total_tweets +=1
                user_id,lat,lon,tweet_text = line.split("\t")
                if user_id not in user_word_dict:
                    # initialize that user's little dictionary
                    user_word_dict[user_id] = dict()
                    user_word_dict[user_id]["count"] = 0.0
                    user_word_dict[user_id]["words"] = []
                    user_word_dict[user_id]["botCount"] = 0.0
                # fill it up
                user_word_dict[user_id]["count"] += 1.0
                # check if there were bot words in the tweets
                tweet_words = [x.lower() for x in re.findall(r"[\w\@\#\'\&\]\*\-\/\[\=\;]+",tweet_text,flags=re.UNICODE)]
                user_word_dict[user_id]["words"] += tweet_words
                for word in bot_words:
                    if word in tweet_words:
                        user_word_dict[user_id]["botCount"] += 1.0
                        break
                # end bot word search
            # end lines in file
            f.close()
            # test that it's growing (it is)
            # if 'the' in city_word_dict:
            #     print(month)
            #     print(city_word_dict['the'])
    
        # manually remove stop words (by setting frequency to 0)
        word_list = []
        for user_id in user_word_dict:
            if user_word_dict[user_id]["botCount"]/user_word_dict[user_id]["count"] < 0.15:
                total_tweets += user_word_dict[user_id]["count"]
                word_list += user_word_dict[user_id]["words"]
            else:
                pass
                # print("removing a user with these words:")
                # print(user_word_dict[user_id]["words"])
        city_word_dict = dict()
        for word in word_list:
            if word in city_word_dict:
                city_word_dict[word] += 1
            else:
                city_word_dict[word] = 1
        for word in stop_words:
            if word in city_word_dict:
                city_word_dict[word] = 0
        happs = labMT.scoreTrie(city_word_dict)
        print("{0} with happs {1} from {2} tweets".format(city,happs,total_tweets))
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

