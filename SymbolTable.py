#!/usr/bin/python
from dataclasses import dataclass, field
from typing import Any, Optional
from abc import ABC


class Type(ABC):
    def __repr__(self):
        name = f'{self.__class__.__name__.lower()}'
        params = ', '.join(str(p) if p is not None else '?' for p in self.__dict__.values())
        return name + (f'<{params}>' if self.__dict__ else '')

    def __eq__(self, other):
        # if isinstance(self, Unknown) or isinstance(other, Unknown):
        #     return True

        if isinstance(other, Union):
            return any(map(self.__eq__, other.types))
            # return any(type == other for type in self.types)

        if isinstance(self, Union):
            return other == self

        if not self.__class__ == other.__class__:
            return False

        for key in self.__dict__.keys() & other.__dict__.keys():
            param1 = self.__dict__[key]
            param2 = other.__dict__[key]
            if param1 is not None and param2 is not None and param1 != param2:
                return False

        return True


class Unknown(Type):
    pass


class Int(Type):
    pass


class Float(Type):
    pass


class String(Type):
    pass


class Range(Type):
    pass


@dataclass(eq=False, repr=False)
class Vector(Type):
    length: Optional[int] = None


@dataclass(eq=False, repr=False)
class Matrix(Type):
    rows: Optional[int] = None
    cols: Optional[int] = None

    # @property
    # def transposed(self):
    #     return self.__class__(rows=self.cols, cols=self.rows)


class Union(Type):
    def __init__(self, *types: Type):
        self.types = types

    def __repr__(self):
        return 'Union[' + ', '.join(map(repr, self.types)) + ']'


@dataclass
class Symbol(object):
    type: Type = field(default_factory=Unknown)
    value: Any = None  # None means unknown value
    readonly: bool = False  # for loop variables


@dataclass
class Scope:
    name: str = '__main__'
    parent: Optional['Scope'] = None
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
                return
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

    def getParentScope(self) -> Optional[Scope]:
        return self.parent

    def pushScope(self, name: str):
        self.current_scope = Scope(name, self.current_scope)

    def popScope(self) -> Optional[Scope]:
        current_scope = self.current_scope
        self.current_scope = current_scope.parent
        return current_scope
