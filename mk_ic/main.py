from mk_ic.mkdebugger import mkic
from mk_ic.utils import argumentToString
import icecream


def setup():
    mkic.configureOutput(
        includeContext=True,
        outputFunction=lambda s: print(s),
        argToStringFunction=argumentToString,
        prefix="Debug | ")


try:
    builtins = __import__('__builtin__')
except ImportError:
    builtins = __import__('builtins')


def install(ic='ic'):
    setup()
    setattr(builtins, ic, mkic)


def uninstall(ic='ic'):
    delattr(builtins, ic)
