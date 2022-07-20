from functools import cached_property
from astplus.ext.arg import AstPlusArg
from astplus.ext.abstract import AstPlusInterface
import ast

class AstPlusFunc(AstPlusInterface):
    def __post_init__(self):
        super().__post_init__()

        if not isinstance(self.astObj, (ast.FunctionDef, ast.AsyncFunctionDef)):
            raise Exception("astObj is not FunctionDef")

    @property
    def name(self):
        return self.astObj.name

    @name.setter
    def name(self, value):
        self.astObj.name = value

    @cached_property
    def kwargs(self):
        return AstPlusArg.fromFunc(self.astObj)

    @property
    def decorators(self):
        return self.astObj.decorator_list
