from mk_ic.mkdebugger import mkic, mkics
from mk_ic.utils import argumentToString
import icecream


def setup():
    mkic.configureOutput(
        includeContext=True,
        outputFunction=print,
        argToStringFunction=argumentToString,
        prefix="MKIC | ")

    mkics.configureOutput(
        includeContext=True,
        outputFunction=print,
        argToStringFunction=argumentToString,
        prefix="MKICS | ")


try:
    builtins = __import__('__builtin__')
except ImportError:
    builtins = __import__('builtins')


def install(ic='ic', ics='ics'):
    setup()
    setattr(builtins, ic, mkic)
    setattr(builtins, ics, mkics)


def uninstall(ic='ic', ics='ics'):
    delattr(builtins, ic)
    delattr(builtins, ics)
