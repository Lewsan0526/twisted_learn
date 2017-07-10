#!/usr/bin/env python
# -*- coding: utf-8 -*-
# author:lewsan

'''
https://likebeta.gitbooks.io/twisted-intro-cn/zh/p18.html
'''

from twisted.internet import defer

import traceback


def got_results(res):
    print 'we got:', res
    traceback.print_stack()


# d = defer.DeferredList([])
#
# d.addCallback(got_results)

d1 = defer.Deferred()
d2 = defer.Deferred()
d = defer.DeferredList([d1, d2])
d.addCallback(got_results)
d1.callback('d1 result')
d2.callback('d2 result')
