import os
from datetime import datetime
import shutil


def pointToCurrentFolder():
    abspath = os.path.abspath(__file__)
    dname = os.path.dirname(abspath)
    os.chdir(dname)


def getTimeStamp():
    today = str(datetime.now().strftime("%Y.%m.%d--%H.%M.%S"))
    return today


# Decorators here
import functools
import time


def timer(func):
    """Print the runtime of the decorated function"""

    @functools.wraps(func)
    def wrapper_timer(*args, **kwargs):
        start_time = time.perf_counter()  # 1
        value = func(*args, **kwargs)
        end_time = time.perf_counter()  # 2
        run_time = end_time - start_time  # 3
        print(f"Finished {func.__name__!r} in {run_time:.4f} secs")
        return value

    return wrapper_timer


def debug(func):
    """Print the function signature and return value"""

    @functools.wraps(func)
    def wrapper_debug(*args, **kwargs):
        args_repr = [repr(a) for a in args]  # 1
        kwargs_repr = [f"{k}={v!r}" for k, v in kwargs.items()]  # 2
        signature = ", ".join(args_repr + kwargs_repr)  # 3
        print(f"Calling {func.__name__}({signature})")
        value = func(*args, **kwargs)
        print(f"{func.__name__!r} returned {value!r}")  # 4
        return value

    return wrapper_debug


def repeat(_func=None, *, num_times=2):
    """repeat a function num_times times"""

    def decorator_repeat(func):
        @functools.wraps(func)
        def wrapper_repeat(*args, **kwargs):
            for _ in range(num_times):
                value = func(*args, **kwargs)
            return value

        return wrapper_repeat

    if _func is None:
        return decorator_repeat
    else:
        return decorator_repeat(_func)


def addto(instance):
    """Easy adding methods to a class instance
    ex:
    class Foo:
        def __init__(self):
            self.x = 42

    foo = Foo()
    @addto(foo)
    def print_x(self):
        print self.x

    # foo.print_x() would print "42"
    """

    def decorator(f):
        import types

        f = types.MethodType(f, instance, instance.__class__)
        setattr(instance, f.func_name, f)
        return f

    return decorator


def slow_down(_func=None, *, rate=1):
    """Sleep given amount of seconds before calling the function"""

    def decorator_slow_down(func):
        @functools.wraps(func)
        def wrapper_slow_down(*args, **kwargs):
            time.sleep(rate)
            return func(*args, **kwargs)

        return wrapper_slow_down

    if _func is None:
        return decorator_slow_down
    else:
        return decorator_slow_down(_func)


def moveFileStartWith(fileNameStartString: str, targetFolderPath: str):
    """Move file start with str to target folder path

    Args:
        fileNameStartString (str): _description_
        targetFolderPath (str): _description_
    """
    a = len(fileNameStartString)
    currentFolderPath = os.getcwd()
    for root, directories, files in os.walk(currentFolderPath):
        for f in files:
            if f[:a] == fileNameStartString:
                source = f
                destination = targetFolderPath
                shutil.move(source, destination)
                # print("Successfully move 1 file!")
