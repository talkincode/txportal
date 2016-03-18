#!/usr/bin/env python
# coding=utf-8

from twisted.internet import defer
from txradius import client
from toughlib import logger, dispatch
import functools

class ACError(BaseException):
    pass


class BasicHandler:
    def __init__(self, config, logger=None):
        self.config = config
        self.logger = logger
        self.secret = str(self.config.get("secret",'secret'))
        self.vendor = str(self.config.get("vendor",'vendor'))

    def process(self, req, rundata):
        if 'cmccv1' in self.vendor:
            return self.proc_cmccv1(req, rundata)
        elif 'cmccv2' in self.vendor:
            return self.proc_cmccv2(req, rundata)
        elif 'huaweiv1' in self.vendor:
            return self.proc_huaweiv1(req, rundata)
        elif 'huaweiv2' in self.vendor:
            return self.proc_huaweiv2(req, rundata)
        else:
            raise ACError("vendor {0} not support".format(self.vendor))


    def proc_cmccv1(self, req, rundata):
        raise ACError("does not support")

    def proc_cmccv2(self, req, rundata):
        raise ACError("does not support")

    def proc_huaweiv1(self, req, rundata):
        raise ACError("does not support")

    def proc_huaweiv2(self, req, rundata):
        raise ACError("does not support")


class EmptyHandler(BasicHandler):

    def process(self, req, rundata):
        self.logger.error("do nothing for {0}".format(repr(req)))
        return None