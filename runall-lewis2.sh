# run for the most recent stuff, using pull tweets

YEAR=14
MONTH=04
for DAY in {15..30}
do
  export DATE=$DAY.$MONTH.$YEAR
  export PLDATE=20${YEAR}-${MONTH}-${DAY}
  echo ${DATE}
  sleep 1
  qsub -V run-lewis2.qsub
done
YEAR=14
MONTH=05
for DAY in 0{1..9} {10..31}
do
  export DATE=$DAY.$MONTH.$YEAR
  export PLDATE=20${YEAR}-${MONTH}-${DAY}
  echo ${DATE}
  sleep 1
  qsub -V run-lewis2.qsub
done
YEAR=14
MONTH=06
for DAY in 0{1..9} {10..30}
do
  export DATE=$DAY.$MONTH.$YEAR
  export PLDATE=20${YEAR}-${MONTH}-${DAY}
  echo ${DATE}
  sleep 1
  qsub -V run-lewis2.qsub
done
YEAR=14
MONTH=07
for DAY in 0{1..9} {10..31}
do
  export DATE=$DAY.$MONTH.$YEAR
  export PLDATE=20${YEAR}-${MONTH}-${DAY}
  echo ${DATE}
  sleep 1
  qsub -V run-lewis2.qsub
done
YEAR=14
MONTH=08
for DAY in 0{1..9} {10..31}
do
  export DATE=$DAY.$MONTH.$YEAR
  export PLDATE=20${YEAR}-${MONTH}-${DAY}
  echo ${DATE}
  sleep 1
  qsub -V run-lewis2.qsub
done
YEAR=14
MONTH=09
for DAY in 0{1..9} 10
do
  export DATE=$DAY.$MONTH.$YEAR
  export PLDATE=20${YEAR}-${MONTH}-${DAY}
  echo ${DATE}
  sleep 1
  qsub -V run-lewis2.qsub
done
