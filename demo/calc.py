"""Simple constant expression calculator demo for tree transformation
kernel.
"""

import asp.codegen.python_ast as ast
import asp.codegen.cpp_ast as cpp_ast
import asp.codegen.ast_tools as ast_tools
from asp.util import *
import inspect
import unittest
import os

class CalcKernel(object):
    def __init__(self):
        # get text of kernel() method and parse into a Python AST
        self.kernel_src = inspect.getsource(self.kernel)
        self.kernel_ast = ast.parse(self.remove_indentation(self.kernel_src))

        self.pure_python = False
        self.pure_python_kernel = self.kernel
        
        # replace kernel with shadow version
        self.kernel = self.shadow_kernel

    def remove_indentation(self, src):
        return src.lstrip()

    def shadow_kernel(self, *args):
        if self.pure_python:
            return self.pure_python_kernel(*args)

        variants = ConvertAST().visit(self.kernel_ast)
        variant_names = ['kernel']

        from asp.jit import asp_module
        try:
            os.mkdir("cache")
        except OSError:
            pass
        mod = asp_module.ASPModule(cache_dir = "cache")
        self.set_compiler_flags(mod)
        print variants
        mod.add_function("kernel", variants, variant_names)

        # package arguments and do the call 
        myargs = [y.data for y in args]
        mod.kernel(*myargs)

    def set_compiler_flags(self, mod):
        import asp.config
        
        mod.backends["c++"].toolchain.cflags += ["-fopenmp", "-O3", "-msse3", "-Wno-unknown-pragmas"]
        if mod.backends["c++"].toolchain.cflags.count('-Os') > 0:
            mod.backends["c++"].toolchain.cflags.remove('-Os')
        if mod.backends["c++"].toolchain.cflags.count('-O2') > 0:
            mod.backends["c++"].toolchain.cflags.remove('-O2')

class ConvertAST(ast_tools.ConvertAST):
    def visit_Return(self, node):
        return cpp_ast.Call("printf", [cpp_ast.String("%d\\n"), self.visit(node.value)])

    def visit_Num(self, node):
        return cpp_ast.CNumber(node.n)

    def visit_BinOp(self, node):
        return cpp_ast.BinOp(self.visit(node.left),
                             self.visit(node.op),
                             self.visit(node.right))
      
    def visit_Add(self, node):
        return "+"

class MyKernel(CalcKernel):
    def kernel():
        return 2 + 3

class Tests(unittest.TestCase):
    def test_whole_thing(self):
        MyKernel().kernel()

if __name__ == '__main__':
    unittest.main()
