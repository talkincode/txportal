FROM index.alauda.cn/toughstruct/tough-pypy:kiss
MAINTAINER jamiesun <jamiesun.net@gmail.com>

RUN pypy -m pip install https://github.com/talkincode/txportal/archive/master.zip
ADD supervisord.conf /etc/supervisord.conf

EXPOSE 2000/udp

CMD ["/usr/local/bin/supervisord","-c","/etc/supervisord.conf"]

