#!/usr/bin/env python
# coding=utf-8

from twisted.internet import defer
from txportal.packet import cmcc, huawei, pktutils
from txportal.simulator.handlers import base_handler

class LogoutHandler(base_handler.BasicHandler):

    def proc_cmccv1(self, req, rundata):
        resp = cmcc.Portal.newMessage(
            cmcc.ACK_LOGOUT,
            req.userIp,
            req.serialNo,
            req.reqId,
            secret=self.secret
        )
        return resp

    
    def proc_cmccv2(self, req, rundata):
        resp = cmcc.Portal.newMessage(
            cmcc.ACK_LOGOUT,
            req.userIp,
            req.serialNo,
            req.reqId,
            secret=self.secret
        )
        return  resp

    def proc_huaweiv1(self, req, rundata):
        resp = huawei.Portal.newMessage(
            huawei.ACK_LOGOUT,
            req.userIp,
            req.serialNo,
            req.reqId,
            self.secret
        )
        return  resp

    def proc_huaweiv2(self, req, rundata):
        
        resp = huawei.PortalV2.newMessage(
            huawei.ACK_LOGOUT,
            req.userIp,
            req.serialNo,
            req.reqId,
            self.secret,
            auth=req.auth,
            chap=(req.isChap==0x00)
        )
        resp.auth_packet()

        return  resp



