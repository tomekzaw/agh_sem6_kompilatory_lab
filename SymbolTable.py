#!/usr/bin/python
from dataclasses import dataclass, field
from typing import Any, Optional


@dataclass
class Symbol(object):
    type: str = 'unknown'  # 'int', 'float', 'string', 'range', 'vector', 'matrix', 'unknown'
    params: dict = field(default_factory=dict)  # 'length', 'rows', 'cols'
    value: Any = None  # None means unknown value


@dataclass
class SymbolTable:
    name: str = '__main__'
    parent: Optional['SymbolTable'] = None
    symbols: dict = field(default_factory=dict)

    def put(self, name: str, symbol: Symbol) -> None:
        if name in self.symbols:
            raise KeyError
        self.symbols[name] = symbol

    def has(self, name: str) -> bool:
        return name in self.symbols

    def get(self, name: str) -> Symbol:
        if not self.has(name):
            raise KeyError
        return self.symbols[name]

    def remove(self, name: str) -> None:
        if not self.has(name):
            raise KeyError
        del self.symbols[name]

    # def getParentScope(self):
    #     return self.parent

    # def pushScope(self, name):
    #     pass

    # def popScope(self):
    #     pass
