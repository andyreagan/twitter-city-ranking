# this scripts submits a bunch of jobs
# that break the files up into minutes
YEAR=2014
MONTH=01
for DAY in 0{1..9} {10..31}
do
  export DATE=$YEAR.$MONTH.$YEAR
  echo ${DATE}
  sleep 1
  qsub -V breakintominutes.qsub
done
MONTH=02
for DAY in 0{1..9} {10..28}
do
  export DATE=$YEAR.$MONTH.$YEAR
  echo ${DATE}
  sleep 1
  qsub -V breakintominutes.qsub
done
MONTH=03
for DAY in 0{1..9} {10..31}
do
  export DATE=$YEAR.$MONTH.$YEAR
  echo ${DATE}
  sleep 1
  qsub -V breakintominutes.qsub
done
MONTH=04
for DAY in 0{1..9} {10..15}
do
  export DATE=$YEAR.$MONTH.$YEAR
  echo ${DATE}
  sleep 1
  qsub -V breakintominutes.qsub
done