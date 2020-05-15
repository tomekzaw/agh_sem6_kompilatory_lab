#!/usr/bin/python
from dataclasses import dataclass, field
from typing import Any, Optional


@dataclass
class Symbol(object):
    type: str = 'unknown'  # 'int', 'float', 'string', 'range', 'vector', 'matrix', 'unknown'
    params: dict = field(default_factory=dict)  # 'length', 'rows', 'cols', 'loop_variable'
    value: Any = None  # None means unknown value


@dataclass
class Scope:
    name: str = '__main__'
    parent: Optional['SymbolTable'] = None
    symbols: dict = field(default_factory=dict)


@dataclass
class SymbolTable:
    current_scope: Scope = field(default_factory=Scope)

    def has(self, name: str) -> bool:
        scope = self.current_scope
        while scope is not None:
            if name in scope.symbols:
                return True
            scope = scope.parent
        return False

    def put(self, name: str, symbol: Symbol) -> None:
        self.current_scope.symbols[name] = symbol

    def update(self, name: str, symbol: Symbol) -> None:
        scope = self.current_scope
        while scope is not None:
            if name in scope.symbols:
                scope.symbols[name] = symbol
            scope = scope.parent
        raise KeyError

    def get(self, name: str) -> Symbol:
        scope = self.current_scope
        while scope is not None:
            if name in scope.symbols:
                return scope.symbols[name]
            scope = scope.parent
        raise KeyError

    def remove(self, name: str) -> None:
        scope = self.current_scope
        while scope is not None:
            if name in scope.symbols:
                del scope.symbols[name]
            scope = scope.parent
        raise KeyError

    # def getParentScope(self):
    #     return self.parent

    def pushScope(self, name: str):
        self.current_scope = Scope(name, self.current_scope)

    def popScope(self):
        parent = self.current_scope.parent
        if parent is None:
            raise
        del self.current_scope
        self.current_scope = parent
