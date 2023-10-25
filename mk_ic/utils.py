import icecream
import executing


@icecream.singledispatch
def argumentToString(obj):
    if type(obj) is str:
        return obj
    else:
        s = icecream.DEFAULT_ARG_TO_STRING_FUNCTION(obj)
        s = s.replace('\\n', '\n')  # Preserve string newlines in output.
        return s


def get_qualname(frame):
    return executing.Source.executing(frame).code_qualname()


def pytest_wrapper_elimination(frame):
    func_name = get_qualname(frame)
    return 'pytest_pyfunc_call' == func_name
