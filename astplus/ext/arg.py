from dataclasses import dataclass
import typing
from astplus.creator import AstCreator
from astplus.ext.abstract import AstPlusInterface, AstPlusUniversal
import ast

@dataclass(frozen=True)
class AstPlusArg(AstPlusInterface):
    astObj: ast.arguments

    def __post_init__(self):
        if not isinstance(self.astObj, ast.arguments):
            raise Exception("astObj is not arguments")
    
    def addArg(self, key):
        self.astObj.args.insert(self.xlen, ast.arg(arg=key))

    @property
    def xlen(self):
        len1 = len(self.astObj.args) if self.astObj.args else 0
        len2 = len(self.astObj.defaults) if self.astObj.defaults else 0
        xlen = len1 - len2
        return xlen

    def getIndex(self, key, default=None):
        """
        get index of arg in arguments
        """
        for i, x in enumerate(self.astObj.args):
            if x.arg == key:
                return i
        return default

    def getDefaultIndex(self, key):
        for i, x in enumerate(self.astObj.args):
            if x.arg == key:
                return i - self.xlen
        
        return None
        
    def keys(self):
        for x in self.astObj.args:
            yield x.arg

    def kwargValues(self):
        for x in self.astObj.defaults:
            yield x.value

    def argKeys(self):
        for i, x in enumerate(self.astObj.args):
            if i < self.xlen:
                yield x.arg
            else:
                break

    def kwargKeys(self):
        for i, x in enumerate(self.astObj.args):
            if i < self.xlen:
                continue
            yield x.arg

    def kwargItems(self):
        for i, x in enumerate(self.astObj.args):
            if i < self.xlen:
                continue
            
            yield x.arg, self.astObj.defaults[i - self.xlen]

    def __contains__(self, key):
        for k in self.keys():
            if k == key:
                return True
        return False

    def __setitem__(self, key, value):
        index = self.getDefaultIndex(key)
        args = AstCreator.create_new_args(**{key: value})
        if index is None:
            self.astObj.args.extend(args.args)
            self.astObj.defaults.extend(args.defaults)
        else:
            self.astObj.defaults[index] = args.defaults[0]
            

    def __getitem__(self, key):
        for k, v in self.kwargItems():
            if k == key:
                return v

        raise KeyError(key)

    def __delitem__(self, key):
        keyindex = self.getIndex(key)
        if keyindex is None:
            raise KeyError(key)

        self.astObj.args.pop(keyindex)

        defaultindex = self.getDefaultIndex(key)
        if defaultindex is None:
            return

        self.astObj.defaults.pop(defaultindex)

    @classmethod
    def fromFunc(cls, func : typing.Union[ast.FunctionDef, ast.AsyncFunctionDef]) -> 'AstPlusArg':
        if not isinstance(func, (ast.FunctionDef, ast.AsyncFunctionDef)):
            raise Exception("func is not FunctionDef")
        func : ast.FunctionDef
        args : ast.arguments = func.args

        if args is None:
            return None

        return cls(args, func)

    