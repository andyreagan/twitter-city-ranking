# accept a timestamp
# read the current date
# pump out a qsub script named by the timestamp, for the current date

import datetime
import sys
import subprocess
import time

jobs = int(subprocess.check_output("showq | grep areagan | wc -l",shell=True))
print jobs

for i in xrange(jobs,25):
    time.sleep(2)
    ctime = subprocess.check_output("date +%S.%M.%H.%d.%m.%y",shell=True).rstrip()

    f = open('currdate.txt','r')
    tmp = f.read().rstrip()
    f.close()

    date = datetime.datetime.strptime(tmp,'%Y-%m-%d')
    date += datetime.timedelta(days=1)

    f = open('currdate.txt','w')
    tmp = f.write(date.strftime('%Y-%m-%d'))
    f.close()

    # day = "10"
    # month = "09"
    # year = "08"

    qsub = '''# This job needs 1 compute node with 1 processor per node.
#PBS -l nodes=1:ppn=1
# #PBS -l pmem=4gb,pvmem=6gb
# It should be allowed to run for up to 24 hours.
#PBS -l walltime=30:00:00
# Name of job.
#PBS -N emilyKeywordScrape
# Join STDERR TO STDOUT.  (omit this if you want separate STDOUT AND STDERR)
#PBS -j oe

cd /users/a/r/areagan/fun/twitter/emily

/usr/bin/time -v gzip -cd /users/c/d/cdanfort/scratch/twitter/tweet-troll/zipped-raw/{0}.tgz | python processTweets.py {1} keywords

\\rm {2}.qsub

'''.format(date.strftime('%d.%m.%y'),date.strftime('%Y-%m-%d'),ctime)

    # print qsub
    print 'writing {}.qsub'.format(ctime)
    f = open('{}.qsub'.format(ctime),'w')
    f.write(qsub)
    f.close()

    qstatus = subprocess.check_output("qsub {}.qsub".format(ctime),shell=True).rstrip()
    print qstatus






