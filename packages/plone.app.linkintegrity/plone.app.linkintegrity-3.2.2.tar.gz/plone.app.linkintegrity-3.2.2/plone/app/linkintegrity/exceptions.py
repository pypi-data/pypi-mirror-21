# -*- coding: utf-8 -*-
from OFS.ObjectManager import BeforeDeleteException
from zope.interface import Interface
from zope.interface import implementer


class ILinkIntegrityNotificationException(Interface):
    """ an exception indicating a prevented link integrity breach """


@implementer(ILinkIntegrityNotificationException)
class LinkIntegrityNotificationException(BeforeDeleteException):
    """ an exception indicating a prevented link integrity breach """

    def __str__(self):
        args = self.args
        if args and isinstance(args, tuple):
            return repr(args[0])
        return super(LinkIntegrityNotificationException, self).__str__()
