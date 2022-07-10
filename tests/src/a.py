import functools
import inspect
from slugify import slugify

def func1(a=1, b=2, c=3):
    print(a, b, c)

def deco1(func):
    def wrapper(*args, **kwargs):
        print('deco1')
        return func(*args, **kwargs)
    return wrapper

def deco2(*a, **k):
    def wrapper(func):
        @functools.wraps(func)
        def inner(*args, **kwargs):
            print('deco2')
            kwargs.update(k)
            return func(*args, **kwargs)
        return inner
    return wrapper

@deco1()
@deco2(a=3, b=4, c=5)
def func2(x, a, b=2, c=3, *k, **kw):
    print(a, b, c)

class cls1:
    clsvar1 = 1

    def __init__(self, a=1, b=2, c=3):
        print(a, b, c)

    def func1(self, a=1, b=2, c=3):
        print(a, b, c)

    async def func2(self, a=1, b=2, c=3):
        print(a, b, c)