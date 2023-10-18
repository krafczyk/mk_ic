from mk_ic.utils import new_get_context
from icecream import ic, IceCreamDebugger


def setup():
    IceCreamDebugger._getContext = new_get_context

    ic.configureOutput(
        includeContext=True,
        outputFunction=lambda s: print(s),
        prefix="Debug | ")


def install():
    from icecream import install
    setup()
    install()
