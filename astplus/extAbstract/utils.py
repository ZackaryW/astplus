import typing
from astplus.extAbstract import AstPlusUniversal
import inspect
import functools

def ensureProperty(creationMethod : typing.Callable):
    def decorator(func):
        # check creationMethod in AstPlusUniversal class
        
        @functools.wraps(func)
        def wrapper(self, *args, **kwargs):
            # get caller name
            obj = getattr(self, f"_{func.__name__}", None)

            if not (hasattr(self, f"_{func.__name__}") and isinstance(obj, AstPlusUniversal)):
                newattr = creationMethod(self.astObj)
                self._setattr(f"_{func.__name__}", newattr)

            return func(self, *args, **kwargs)
        
        return wrapper
    return decorator