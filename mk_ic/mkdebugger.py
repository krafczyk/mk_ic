from inspect import getframeinfo
from os.path import realpath, basename
import executing

import icecream


class MKIceCreamDebugger(icecream.IceCreamDebugger):
    # Install our own context getter for icecream 2.1.3
    def _getContext(self, callFrame, callNode):
        frameInfo = getframeinfo(callFrame)
        lineNumber = callNode.lineno
        parentFunction = executing.Source.executing(callFrame).code_qualname()

        filepath = (realpath if self.contextAbsPath else basename)(frameInfo.filename)
        return filepath, lineNumber, parentFunction

    def _constructArgumentOutput(self, prefix, context, pairs):
        def argPrefix(arg):
            return '%s: ' % arg

        pairs = [(arg, self.argToStringFunction(val)) for arg, val in pairs]
        # For cleaner output, if <arg> is a literal, eg 3, "string", b'bytes',
        # etc, only output the value, not the argument and the value, as the
        # argument and the value will be identical or nigh identical. Ex: with
        # ic("hello"), just output
        #
        #   ic| 'hello',
        #
        # instead of
        #
        #   ic| "hello": 'hello'.
        #
        pairStrs = [
            val if icecream.isLiteral(arg) else (argPrefix(arg) + val)
            for arg, val in pairs]

        allArgsOnOneLine = self._pairDelimiter.join(pairStrs)
        multilineArgs = len(allArgsOnOneLine.splitlines()) > 1

        contextDelimiter = self.contextDelimiter if context else ''
        allPairs = prefix + context + contextDelimiter + allArgsOnOneLine
        firstLineTooLong = len(allPairs.splitlines()[0]) > self.lineWrapWidth

        if multilineArgs or firstLineTooLong:
            # ic| foo.py:11 in foo()
            #     multilineStr: 'line1
            #                    line2'
            #
            # ic| foo.py:11 in foo()
            #     a: 11111111111111111111
            #     b: 22222222222222222222
            fix_empty_strings = lambda s: " " if len(s) == 0 else s
            def is_single_string(s):
                result = False
                f, l = s[0], s[-1]
                if f == '"' and l == '"':
                    result = True
                elif f == "'" and l == "'":
                    result = True
                return result
            if context:
                lines = [prefix + context]
                for arg, value in pairs:
                    if is_single_string(arg):
                        lines += [(len(prefix) * ' ') + fix_empty_strings(value)]
                    else:
                        lines += [ icecream.format_pair(len(prefix) * ' ', arg, fix_empty_strings(value))]
            # ic| multilineStr: 'line1
            #                    line2'
            #
            # ic| a: 11111111111111111111
            #     b: 22222222222222222222
            else:
                arg_lines = []
                for arg, value in pairs:
                    if is_single_string(arg):
                        arg_lines += [fix_empty_strings(value)]
                    else:
                        arg_lines += [icecream.format_pair('', arg, fix_empty_strings(value))]

                lines = icecream.indented_lines(prefix, '\n'.join(arg_lines))
        # ic| foo.py:11 in foo()- a: 1, b: 2
        # ic| a: 1, b: 2, c: 3
        else:
            lines = [prefix + context + contextDelimiter + allArgsOnOneLine]

        return '\n'.join(lines)


mkic = MKIceCreamDebugger()
