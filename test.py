from twisted.internet import reactor
from pyxl import register
from twisted.python import log
import sys

cl = register.RegisteringClient('pakassd','linjab.cz', 'jab','pyca', 5222, reactor)
log.startLogging(sys.stdout)
cl.connect()
reactor.run()
