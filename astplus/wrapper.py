import ast
import inspect
import typing
from astplus.creator import AstCreator
from astplus.wrapMaker import AstWrapperBuilder
from astplus.visitor import AstVisitor

class AstWrapperMeta(type):
    """
    metaclass used to create singleton instances of AstWrapper
    """

    _instances : typing.Dict[ast.AST, 'AstWrapper'] = {}
    _parents : typing.Dict['AstWrapper', 'AstWrapper'] = {}
    def __call__(cls, *args, **kwargs):
        if len(args) + len(kwargs) >= 1:
            astc = args[0] if len(args) == 1 else  kwargs.get('astc', None)

        if not isinstance(astc, ast.AST):
            raise TypeError(f"{astc} is not an AST")

        if astc in cls._instances:
            return cls._instances[astc]

        parent = kwargs.get('parent', None)

        if parent is not None and not isinstance(parent, AstWrapper):
            raise TypeError(f"{parent} is not an AstWrapper")

        
        astw = super().__call__(*args, **kwargs)

        if parent is not None:
            cls._parents[astw] = parent

        cls._instances[astc] = astw
        return astw

    @classmethod
    def blowUp(cls, delAll : bool = False):
        if delAll:
            for astc in cls._instances:
                del cls._instances[astc]
        cls._instances = {}

    @classmethod
    def blowChildren(cls, astw : 'AstWrapper'):
        for child, parent in cls._parents.items():
            if parent == astw:
                del cls._parents[child]    

class AstWrapper(metaclass=AstWrapperMeta):
    """
    wrapper object for simplified ast manipulation
    """

    def __init__(self, astc : ast.AST, parent : 'AstWrapper' = None) -> None:
        self._ast = astc
        self._parent = parent
        self._wrapper = AstWrapperBuilder(self)
        self._visitor = None

    @property
    def astObject(self):
        return self._ast

    @property
    def sourcelines(self):
        return ast.unparse(self._ast).split('\n')

    @property
    def wrap(self):
        return self._wrapper

    @property
    def visitor(self):
        if self._visitor is None:
            self._visitor = AstVisitor(self.astObject)

        return self._visitor

    def __del__(self):
        self.__class__.blowChildren(self)

    def builtinTransform(self, transformer : typing.Union[ast.NodeTransformer, type]):
        if isinstance(transformer, type) and issubclass(transformer, ast.NodeTransformer):
            transformer = transformer()
        if not isinstance(transformer, ast.NodeTransformer):
            raise TypeError(f"{transformer} is not a NodeTransformer")

        self._ast = transformer.visit(self._ast)
        self.__class__.blowChildren(self)
        self._visitor = None

    @classmethod
    def fromAst(cls, astc : ast.AST, parent : 'AstWrapper' = None):
        return cls(astc, parent)

    @classmethod
    def fromSource(cls, source : str):
        return cls(ast.parse(source))

    @classmethod
    def fromFile(cls, filepath : str):
        with open(filepath, 'r') as f:
            return cls.fromSource(f.read())
        
    @classmethod
    def fromModule(cls, module_str : str):
        exc = None
        try:
            import importlib
            module = importlib.import_module(module_str)
            astObj = ast.parse(inspect.getsource(module))
            return cls.fromAst(astObj)
        except Exception as e:
            exc = e

        try:
            module_str = module_str.replace('.', '/')
            with open(module_str + '.py', 'r') as f:
                source = f.read()
            return cls.fromSource(source)
        except Exception as a:
            print(a)
            raise exc

        