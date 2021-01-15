FROM ubuntu:16.04
MAINTAINER Recar "recar@recar.xyz"
RUN sed -i 's/archive.ubuntu.com/mirrors.ustc.edu.cn/g' /etc/apt/sources.list
RUN apt-get update && apt-get install -y python3
RUN apt-get update && apt-get install -y python-pip
RUN apt-get install -y vim
RUN apt-get install -y libmysqld-dev
RUN apt-get install -y supervisor
ADD ./ /root/
RUN pip install -r /root/requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple
ADD server.conf /etc/supervisor/conf.d/
CMD ["/usr/bin/supervisord", "-n", "-c", "/etc/supervisor/supervisord.conf"]