#!/usr/bin/env python
# coding=utf-8
import sys,os
from twisted.internet import protocol
import msgpack
from txzmq import ZmqEndpoint, ZmqFactory, ZmqPushConnection, ZmqPullConnection
from twisted.internet import reactor, defer
from txportal.packet import cmcc, huawei, pktutils
from txportal.simulator.handlers import (
    auth_handler, 
    chellenge_handler, 
    base_handler, 
    reqinfo_handler,
    logout_handler
)
from twisted.logger import Logger
import functools,time

def timecast(func):
    @functools.wraps(func)
    def warp(*args,**kargs):
        _start = time.clock()
        result = func(*args,**kargs)
        print "%s cast %.6f second"%(func.__name__,time.clock()-_start)
        return result
    return warp


class TpSimMaster(protocol.DatagramProtocol):
    logger = Logger()
    def __init__(self):
        self.pusher = ZmqPushConnection(ZmqFactory(), ZmqEndpoint('bind', 'ipc:///tmp/tpsim-message'))
        self.logger.info("init TpSimMaster pusher : %s " % (self.pusher))

    def datagramReceived(self, datagram, (host, port)):
        message = msgpack.packb([datagram, host, port])
        self.pusher.push(message)
        

ACError = base_handler.ACError

class TpSimWorker(protocol.DatagramProtocol):
    def __init__(self, config, logger=None):
        self.config = config
        self.logger = logger or Logger()
        self.debug = self.config.get("debug",True)
        self.vendor = self.config.get("vendor",'cmccv2')
        self.secret = str(self.config.get("secret",'secret'))
        self.rundata = {"challenges":{}}

        self.ac_handlers = {
            cmcc.REQ_CHALLENGE : chellenge_handler.ChellengeHandler(self.config,self.logger),
            cmcc.REQ_AUTH      : auth_handler.AuthHandler(self.config,self.logger),
            cmcc.REQ_INFO      : reqinfo_handler.ReqInfoHandler(self.config,self.logger),
            cmcc.AFF_ACK_AUTH  : base_handler.EmptyHandler(self.config,self.logger),
            cmcc.ACK_NTF_LOGOUT: base_handler.EmptyHandler(self.config,self.logger),
            cmcc.NTF_HEARTBEAT : base_handler.EmptyHandler(self.config,self.logger),
            cmcc.REQ_LOGOUT    : logout_handler.LogoutHandler(self.config,self.logger),
        }
        self.puller = ZmqPullConnection(ZmqFactory(), ZmqEndpoint('connect', 'ipc:///tmp/tpsim-message'))
        self.puller.onPull = self.process
        reactor.listenUDP(0, self)
        self.logger.info("init TpSimWorker puller : %s " % (self.puller))

    def sendtoPortald(self, msg):
        portal_addr = (self.config.get('portal_host','127.0.0.1'), int(self.config.get('portal_listen',50100)))
        if self.debug:
            self.logger.debug(":: Send Message to Portal Listen %s: %s" % (portal_addr, repr(msg)))
        self.transport.write(str(msg), portal_addr)

    def parse(self, datagram, (host, port)):
        
        if self.vendor in ('cmccv1', 'cmccv2'):
            return cmcc.Portal(secret=self.secret, packet=datagram, source=(host, port))
        elif 'huaweiv1' in self.vendor:
            return huawei.Portal(secret=self.secret, packet=datagram, source=(host, port))
        elif 'huaweiv2' in self.vendor:
            return huawei.PortalV2(secret=self.secret, packet=datagram, source=(host, port))
        else:
            raise ACError("vendor {0} not support".format(self.vendor))
    @timecast
    def process(self, message):
        try:
            datagram, host, port =  msgpack.unpackb(message[0])
            request = self.parse(datagram, (host, port))
            if self.debug:
                self.logger.debug(":: Received portal packet from %s:%s: %s" % (host, port, repr(request)))
            # import pdb;pdb.set_trace()
            handler = self.ac_handlers[request.type]
            resp = handler.process(request,self.rundata)
            if resp:
                self.transport.write(str(resp), (host, port))
                if self.debug:
                    self.logger.debug(":: Send response to %s:%s: %s" % (host, port, repr(resp)))

        except Exception as err:
            self.logger.error(':: Dropping invalid packet from %s: %s' % ((host, port), str(err)))
            import traceback
            traceback.print_exc()


def run_master(config):
    master = TpSimMaster()
    reactor.listenUDP(int(config.get('port',2000)), master)

def run_worker(config):
    master = TpSimWorker(config)



