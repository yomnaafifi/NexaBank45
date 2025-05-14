FROM ubuntu:22.04 AS hadoop_python

RUN apt update && apt install -y openjdk-8-jdk python3 pip python3-venv ssh sudo
RUN pip install dotenv faker fastparquet logger pandas pyarrow watchdog
RUN addgroup hadoop
RUN adduser --disabled-password --ingroup hadoop hadoop

ENV HADOOP_HOME=/usr/local/hadoop TEZ_HOME=/usr/local/tez HIVE_HOME=/usr/local/hive
ENV PATH=$PATH:$HADOOP_HOME/bin:$HADOOP_HOME/sbin:$TEZ_HOME/bin:/usr/local/hive/bin

ADD https://dlcdn.apache.org/hadoop/common/hadoop-3.3.6/hadoop-3.3.6.tar.gz /tmp
RUN tar -xzf /tmp/hadoop-3.3.6.tar.gz -C /usr/local && \
    rm /tmp/hadoop-3.3.6.tar.gz && \
    mv /usr/local/hadoop-3.3.6 $HADOOP_HOME && \
    chown -R hadoop:hadoop $HADOOP_HOME

ADD https://dlcdn.apache.org/tez/0.10.4/apache-tez-0.10.4-bin.tar.gz /tmp
RUN tar -xzf /tmp/apache-tez-0.10.4-bin.tar.gz -C /usr/local && \
    rm /tmp/apache-tez-0.10.4-bin.tar.gz && \
    mv /usr/local/apache-tez-0.10.4-bin $TEZ_HOME && \
    chown -R hadoop:hadoop $TEZ_HOME

RUN echo "root:123" | chpasswd && \
    echo 'hadoop ALL=(ALL:ALL) NOPASSWD:ALL' >> /etc/sudoers

USER hadoop:hadoop
RUN ssh-keygen -t rsa -P '' -f ~/.ssh/id_rsa && \
    cat ~/.ssh/id_rsa.pub >> ~/.ssh/authorized_keys && \
    chmod og-wx ~/.ssh/authorized_keys

WORKDIR /home/hadoop
RUN mkdir /home/hadoop/codes && \
    sudo chmod -R 777 /home/hadoop/codes

ADD --chown=hadoop:hadoop https://dlcdn.apache.org/hive/hive-4.0.1/apache-hive-4.0.1-bin.tar.gz /usr/local
RUN sudo tar -xzf /usr/local/apache-hive-4.0.1-bin.tar.gz -C /usr/local && \
    sudo mv /usr/local/apache-hive-4.0.1-bin $HIVE_HOME && \
    sudo chown -R hadoop:hadoop $HIVE_HOME && \
    sudo rm /usr/local/apache-hive-4.0.1-bin.tar.gz

COPY --chown=hadoop:hadoop --chmod=777 start-script.sh .
ENTRYPOINT [ "./start-script.sh" ]
