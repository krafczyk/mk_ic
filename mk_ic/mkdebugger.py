from inspect import getframeinfo
from os.path import realpath, basename
from mk_ic.utils import get_qualname

import icecream


class MKIceCreamDebugger(icecream.IceCreamDebugger):
    def __init__(self, show_stack=False, frame_filters=None, **kwargs):
        super().__init__(**kwargs)
        self.show_stack = show_stack
        self.frame_filters = frame_filters

    def _formatContext(self, callFrame, callNode):
        filename, lineNumber, func_ctx = self._getContext(
            callFrame, callNode)

        def add_parens(s):
            if s != '<module>':
                return f"{s}()"
            else:
                return s

        func_ctx = list(map(add_parens, func_ctx))
        # Bottom of the list is the most recent function
        func_ctx = list(reversed(func_ctx))

        context_prefix = f'{filename}:{lineNumber} in '
        context = [ f"{context_prefix}{func_ctx[0]}"]
        for func in func_ctx[1:]:
            context += [ (len(context_prefix) * ' ') + func ]
        return context

    # Install our own context getter for icecream 2.1.3
    def _getContext(self, callFrame, callNode):
        frameInfo = getframeinfo(callFrame)
        lineNumber = callNode.lineno
        if self.show_stack:
            func_ctx = [get_qualname(callFrame)]
            frame = callFrame.f_back
            while frame is not None:
                if self.frame_filters is not None:
                    # Check all filters, break if one matches
                    filter_matched = False
                    for fil in self.frame_filters:
                        if fil(frame):
                            filter_matched = True
                            break
                    if filter_matched:
                        break
                func_ctx += [get_qualname(frame)]
                frame = frame.f_back
        else:
            func_ctx = [get_qualname(callFrame)]

        filepath = (realpath if self.contextAbsPath else basename)(frameInfo.filename)
        return filepath, lineNumber, func_ctx

    def configureOutput(self, frame_filters=None, **kwargs):
        if len(kwargs) > 0:
            super().configureOutput(**kwargs)
        self.frame_filters = frame_filters

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

        if not context or len(context) == 1:
            # We can attempt a one line output
            oneline_context = context[0]
        
            contextDelimiter = self.contextDelimiter if oneline_context else ''
            allPairs = prefix + oneline_context + contextDelimiter + allArgsOnOneLine
            firstLineTooLong = len(allPairs.splitlines()[0]) > self.lineWrapWidth

            if not firstLineTooLong and not multilineArgs:
                # ic| foo.py:11 in foo()- a: 1, b: 2
                # ic| a: 1, b: 2, c: 3

                lines = [prefix + oneline_context + contextDelimiter + allArgsOnOneLine]
                return '\n'.join(lines)

        fix_empty_strings = lambda s: " " if len(s) == 0 else s
        def is_single_string(s):
            result = False
            f, l = s[0], s[-1]
            if f == '"' and l == '"':
                result = True
            elif f == "'" and l == "'":
                result = True
            return result

        # ic| foo.py:11 in foo()
        #     multilineStr: 'line1
        #                    line2'
        #
        # ic| foo.py:11 in foo()
        #     a: 11111111111111111111
        #     b: 22222222222222222222
        if context:
            lines = [prefix + context[0]]
            for line in context[1:]:
                lines += [len(prefix) * ' ' + line]
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

        return '\n'.join(lines)


mkic = MKIceCreamDebugger()
mkics = MKIceCreamDebugger(show_stack=True)
