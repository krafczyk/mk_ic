from inspect import getframeinfo
from os.path import realpath, basename
import executing


# Install our own context getter for icecream 2.1.3
def new_get_context(self, callFrame, callNode):
    frameInfo = getframeinfo(callFrame)
    lineNumber = callNode.lineno
    parentFunction = executing.Source.executing(callFrame).code_qualname()

    filepath = (realpath if self.contextAbsPath else basename)(frameInfo.filename)
    return filepath, lineNumber, parentFunction
