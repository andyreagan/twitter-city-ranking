YEAR=14
MONTH=01
for DAY in 0{1..9} {10..31}
do
  export DATE=$DAY.$MONTH.$YEAR
  echo ${DATE}
  sleep 1
  qsub -V run-lewis.qsub
done
MONTH=02
for DAY in 0{1..9} {10..28}
do
  export DATE=$DAY.$MONTH.$YEAR
  echo ${DATE}
  sleep 1
  qsub -V run-lewis.qsub
done
MONTH=03
for DAY in 0{1..9} {10..31}
do
  export DATE=$DAY.$MONTH.$YEAR
  echo ${DATE}
  sleep 1
  qsub -V run-lewis.qsub
done
MONTH=04
for DAY in 0{1..9} {10..14}
do
  export DATE=$DAY.$MONTH.$YEAR
  echo ${DATE}
  sleep 1
  qsub -V run-lewis.qsub
done
