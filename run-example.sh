/usr/bin/time -v gzip -cd /users/c/d/cdanfort/scratch/twitter/tweet-troll/zipped-raw/${DATE}/${DATE}-${HOUR}-${MINUTE}.gz | python fiona-shapely-speedtest.py ${DATE}
