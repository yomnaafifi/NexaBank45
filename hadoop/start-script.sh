#!/usr/bin/bash
sudo service ssh start

if
    [ ! -f ~/.makCluster ];
then
    hdfs namenode -format
    start-all.sh
    touch ~/.makCluster;
    schematool -dbType derby -initSchema;
    hdfs dfs -mkdir -p /apps/tez;
    hdfs dfs -chmod 777 /apps/tez/
    hdfs dfs -put $TEZ_HOME/share/tez.tar.gz /apps/tez
fi

start-all.sh
export HIVE_AUX_JARS_PATH=$TEZ_HOME
hiveserver2
sleep infinity
