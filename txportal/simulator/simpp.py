#!/usr/bin/pypy
from twisted.internet import utils
from twisted.internet import protocol
import os

class SimProtocol(protocol.ProcessProtocol):
    
    def __init__(self):
        self.parent_id = os.getpid()

    def connectionMade(self):
        print "tpsim worker created!"
        print "master pid = %s" % self.parent_id
        print "worker pid = %s" % self.transport.pid

    def outReceived(self, data):
        pass

    def errReceived(self, data):
        print "error", data

    def processExited(self, reason):
        print "worker exit %s, status %d" % (self.transport.pid, reason.value.exitCode,)

    def processEnded(self, reason):
        print "%s worker ended, status %d" % (self.transport.pid, reason.value.exitCode,)
        print "quitting"
    

