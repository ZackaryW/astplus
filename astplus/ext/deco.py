from functools import cached_property
from astplus.ext.arg import AstPlusArg
from astplus.ext.abstract import AstPlusInterface
import ast

class AstPlusDecoratorKwarg(AstPlusInterface):
    def items(self, unparse=True):
        for k in self.astObj:
            yield k.arg, ast.unparse(k.value) if unparse else k.value

    def keys(self):
        for k in self.astObj:
            yield k.arg

    def values(self, unparse=True):
        for k in self.astObj:
            yield ast.unparse(k.value) if unparse else k.value
        
    def __setitem__(self, key, value):
        if key in self.keys():
            self.astObj[key].value = ast.parse(value, mode="eval").body[0]
        else:
            self.astObj.append(ast.keyword(arg=key, value=ast.parse(value, mode="eval").body[0]))

    def __getitem__(self, key, unparse=True):
        for k, v in self.items(unparse=unparse):
            if k == key:
                return v
    
    def __delitem__(self, key): 
        target = None 
        for i, k in enumerate(self.astObj):
            if k.arg == key:
                target = i
                break
        if target is not None:
            self.astObj.pop(target)
    
    def __contains__(self, key):
        for k in self.astObj:
            if k.arg == key:
                return True
        return False

    def __iter__(self):
        for k in self.astObj:
            yield k.arg

    def __len__(self):
        return len(self.astObj)
        

class AstPlusDecorator(AstPlusInterface):
    def __post_init__(self):
        super().__post_init__()

        if not isinstance(self.astObj, ast.Call):
            raise Exception("astObj is not a decorator/or Call")

    @property
    def name(self):
        ast.unparse(self.astObj.func)

    @cached_property
    def kwargs(self):
        return AstPlusDecoratorKwarg(self.astObj.keywords)

    