import re
import codecs
from sys import argv

if __name__ == '__main__':
  eventFolder = '/users/a/r/areagan/fun/twitter/unilever/{}'.format("keywords")
  f = codecs.open('/users/a/r/areagan/fun/twitter/unilever/keywords.txt'.format(eventFolder),'r','utf8')
  keyWords = [line.rstrip().lower() for line in f]
  f.close()
  del(keyWords[-1])
  del(keyWords[-1])
  
  # check these are the right keywords!
  print keyWords

  folderNames = ['{0}/{1}/tweets'.format(eventFolder,re.sub('&','and',re.sub('\'','',re.sub('\s','-',keyword)))) for keyword in keyWords]
  print folderNames

  teststrings = ["ben and jerry'szz ice cream foodie","great klondike","i like ben & jerry's with chocolate on food"]

  # try to match
  for teststring in teststrings:
      print "-"*40
      print teststring
      print "word matches:"
      raw_text = [x.lower().lstrip("?';:.$%&()\\!*[]{}|\"<>,^-_=+").rstrip("@#?';:.$%&()\\!*[]{}|\"<>,^-_=+") for x in re.split('\s|--',teststring,flags=re.UNICODE)]
      for word in raw_text:
          for keyword in keyWords:
              if keyword == word:
                  print keyword

      print "regex matches:"
      for keyword in keyWords:
          if re.search(r"\b%s\b" % keyword,teststring) is not None:
              print keyword



