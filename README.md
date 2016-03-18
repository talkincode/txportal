# txportal

txportal 是一个基于Python/twisted开发的 wlan portal 协议处理模块, 支持cmccv1，cmccv2，huaweiv1，huaweiv2协议。

## 安装

    pip install txportal -r requirements.txt

## AC 模拟设备

### tpsim 工具

- 参数说明


    usage: tpsim [-h] [-ph PORTAL_HOST] [-pl PORTAL_LISTEN] [-v VENDOR]
              [-e SECRET] [-p PORT] [-d] [-M] [-W] [-f FORK]

        optional arguments:

        -h, --help            show this help message and exit
        -ph PORTAL_HOST, --portal_host PORTAL_HOST
                             portal ip addr
        -pl PORTAL_LISTEN, --portal_listen PORTAL_LISTEN
                             portal ip addr
        -v VENDOR, --vendor VENDOR
                             portal protoal version:
                             cmccv1,cmccv2,huaweiv1,huaweiv2
        -e SECRET, --secret SECRET
                             portal share secret
        -p PORT, --port PORT  ac port, default 2000
        -d, --debug           debug option
        -M, --master          run master
        -W, --worker          run worker
        -f FORK, --fork FORK  worker fork num


- 运行模拟进程启动4个 worker 子进程处理消息

    $ tpsim -M -d -f 4
 


