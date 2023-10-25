import icecream


@icecream.singledispatch
def argumentToString(obj):
    if type(obj) is str:
        return obj
    else:
        s = icecream.DEFAULT_ARG_TO_STRING_FUNCTION(obj)
        s = s.replace('\\n', '\n')  # Preserve string newlines in output.
        return s
