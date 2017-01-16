
pid=`ps -ef|grep -i "python ./run.py"|cut -f 3 -d' '`
for id in $pid;do
    p=`ps -fp $id`
    echo "Kill\r\n $p ..."
    kill -9 $id
    if [ $? -eq 0 ];then
        echo "Kill successfully"
    else
        echo "Kill failed"
    fi;
done;

nohup python ./run.py emall &
nohup python ./run.py supplier &