
import typing
import ast

class AstWrapperBuilder:
    def __init__(self, base):
        self._base = base
        self._baseType = type(base)

    def __getattribute__(self, name: str):
        getted = getattr(self._base.astObject, name)

        if isinstance(getted, ast.AST):
            return self._baseType(getted, self._base.astObject)

        if isinstance(getted, typing.Iterable) and all(isinstance(x, ast.AST) for x in getted):
            getted_type = type(getted)
            return getted_type([self._baseType(x, self._base.astObject) for x in getted])
            
        return getted
