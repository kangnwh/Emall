
pid=`ps -ef|grep -i "python ./run.py"|cut -f 3 -d' '`
for id in $pid;do
kill -9 $id
done;

nohup python ./run.py emall &
nohup python ./run.py supplier &