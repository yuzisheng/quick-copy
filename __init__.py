# -*- coding: utf-8 -*-

def classFactory(iface):
    from .quick_copy import QuickCopy
    return QuickCopy(iface)
