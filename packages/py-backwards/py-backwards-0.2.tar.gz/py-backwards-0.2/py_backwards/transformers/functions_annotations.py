from typed_ast import ast3 as ast
from .base import BaseTransformer


class FunctionsAnnotationsTransformer(BaseTransformer):
    target = (2, 7)

    def visit_arg(self, node: ast.arg) -> ast.arg:
        node.annotation = None
        return self.generic_visit(node)  # type: ignore

    def visit_FunctionDef(self, node: ast.FunctionDef):
        node.returns = None
        return self.generic_visit(node)  # type: ignore
