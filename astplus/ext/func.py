from astplus.ext.arg import AstPlusArg
from astplus.extAbstract import AstPlusInterface
import ast
from astplus.extAbstract.utils import ensureProperty

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

    @property
    @ensureProperty(AstPlusArg.fromFunc)
    def kwargs(self):
        return self._kwargs

    @property
    def decorators(self):
        return self.astObj.decorator_list
