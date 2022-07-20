# ast-plus

## install from source

```
python -m pip install git+https://github.com/ZackaryW/astplus.git
```

## documentation

1. creating the wrapper (from module)
```py

from astplus import AstWrapper

wrapper = AstWrapper.fromModule(target_module_string)
```

2. loop through all functions and its keyword arguments

```py

for func in wrapper.visitor.visit_FunctionDef():
    # iterating through each function node
    func : ast.FunctionDef

    # use AstPlusArg to easily extract keyword arguments
    argPlus = AstPlusArg.fromFunc(func)
    for k, v in argPlus.kwargItems():
        
        if k == "some func worth looking at":
            argPlus[k] = some_other_value

```

