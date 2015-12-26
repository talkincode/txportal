#!/usr/bin/env python
# coding=utf-8

from twisted.internet import protocol
from twisted.internet import reactor, defer
from txportal.packet import cmcc, huawei
from txportal.packet.pktutils import hexdump
from twisted.logger import Logger
import time
import six

class Vendor:

    def __init__(self, name, mod, proto):
        self.name = name
        self.mod = mod
        self.proto = proto


class PortalClient(protocol.DatagramProtocol):

    vendors = {
        'cmccv1'  : Vendor('cmccv1', cmcc, cmcc.Portal),
        'cmccv2'  : Vendor('cmccv2', cmcc, cmcc.Portal),
        'huaweiv1': Vendor('huaweiv1', huawei, huawei.Portal),
        'huaweiv2': Vendor('huaweiv2', huawei, huawei.PortalV2),
    }

    def __init__(self, secret, timeout=10, debug=True, log=None, vendor='cmccv2'):
        self.secret = six.b(secret)
        self.log = log or Logger()
        self.timeout = timeout
        self.debug = debug
        self.vendor = PortalClient.vendors.get(vendor)
        reactor.listenUDP(0, self)

    def close(self):
        if self.transport is not None:
            self.transport = None
            self.port.stopListening()

    def onError(self, err):
        self.log.err('Packet process error：%s' % str(err))
        self.close()

    def onResult(self, resp):
        reactor.callLater(0.001, self.close,)
        return resp

    def sendto(self, req, (host,port) ):
        if self.debug:
            # print ":: Hexdump >> %s" % hexdump(str(req),len(req))
            self.log.info("Start send packet To AC (%s:%s) >> %s"%(host,port,repr(req)))
        
        self.transport.write(str(req),(host,port))
        self.deferrd = defer.Deferred()
        self.deferrd.addCallbacks(self.onResult,self.onError)
        return self.deferrd

    def datagramReceived(self, datagram, (host, port)):
        try:
            resp = self.vendor.proto(packet=datagram,secret=self.secret)
            if self.debug:
                self.log.info(":: Received <%s> packet from AC %s >> %s " % (self.vendor.name, (host, port), repr(resp)))
            self.deferrd.callback(response)
        except Exception as err:
            self.log.error('Invalid Response packet from %s: %s' % ((host, port), str(err)))
            self.deferrd.errback(response)


def send_auth(secret, timeout=10, debug=True, log=None, vendor='cmccv2', data=None, host=None, port=2000):
    return PortalClient(secret, timeout, debug, log, vendor).sendto(data, (host,port))











