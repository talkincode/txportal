# txportal

txportal 是一个基于Python/twisted开发的 wlan portal 协议处理模块, 支持cmccv1，cmccv2，huaweiv1，huaweiv2协议。

## 安装

    pip install txportal -r requirements.txt

## AC 模拟设备

### tpsim 工具

- 参数说明

    usage: tpsim [-h] [-ph PORTAL_HOST] [-pl PORTAL_LISTEN] [-v VENDOR]
              [-e SECRET] [-p PORT] [-d] [-M] [-W]

    optional arguments:

        -h, --help            show this help message and exit
        -ph PORTAL_HOST,   --portal_host PORTAL_HOST
                             portal ip addr
        -pl PORTAL_LISTEN, --portal_listen PORTAL_LISTEN
                             portal ip addr
        -v VENDOR, --vendor VENDOR
                             portal protoal version: cmccv1,cmccv2,huaweiv1,huaweiv2
        -e SECRET, --secret SECRET
                             portal share secret
        -p PORT, --port PORT  ac port, default 2000
        -d, --debug           debug option
        -M, --master          master option
        -W, --worker          worker option


- 单进程模式

    $ tpsim -M -W -d

- 多进程模式


    $ tpsim -M -d   #启动 master 进程，master进程只启动一个

    $ tpsim -W -d   #启动 worker 进程，worker进程可以启动多个


### 通过docker进行部署

    docker run  \
     -e PORTAL_HOST=127.0.0.1 \
     -e PORTAL_VENDOR=cmccv2 \
     -e PORTAL_SECRET=secret \
      --net host index.alauda.cn/toughstruct/tpsim

### 参数说明

- PORTAL_HOST： portal服务器ip地址,可选
- PORTAL_VENDOR：portal协议版本，支持 cmccv1,cmccv2,huaweiv1,huaweiv2，默认是 cmccv2
- PORTAL_SECRET：portal与ac通信共享密钥，默认是 secret

