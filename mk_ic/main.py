from mk_ic.utils import new_get_context, argumentToString, constructArgumentOutput
from icecream import ic, IceCreamDebugger


def setup():
    IceCreamDebugger._getContext = new_get_context
    IceCreamDebugger._constructArgumentOutput = constructArgumentOutput

    ic.configureOutput(
        includeContext=True,
        outputFunction=lambda s: print(s),
        argToStringFunction=argumentToString,
        prefix="Debug | ")


def install():
    from icecream import install
    setup()
    install()
