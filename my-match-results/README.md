Here is another match.

This one, I differed a bit from what I think Lewis (and Morgan?) did.
Didn't block some city-name based words from the everywhere, but just blocked all of the city name words from it's individual score.
So, city name words like this for each city:
```
            city_words = [x.lower() for x in re.findall(r"[\w]+",city,flags=re.UNICODE)]
            stop_words = ["nigga", "niggaz", "niggas", "nigger"]
            stop_words.extend(city_words)
```
and the blocked list for everywhere was just the n-words, from above.


Still filtered bots with more than 15% of:
```
    bot_words = ["humid", "humidity", "pressure", "earthquake",]
```