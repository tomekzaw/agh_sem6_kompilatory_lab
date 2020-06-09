from dataclasses import dataclass, field
from typing import List, Dict, Any


@dataclass
class Memory:
    name: str
    symbols: Dict[str, Any] = field(default_factory=dict)

    def has_key(self, name):
        return name in self.symbols

    def get(self, name):
        return self.symbols[name]

    def put(self, name, value):
        self.symbols[name] = value


@dataclass
class MemoryStack:
    stack: List[Memory] = field(default_factory=lambda: [Memory('global')])

    def get(self, name):
        for memory in self.stack:
            if memory.has_key(name):  # noqa
                return memory.get(name)
        raise KeyError(f'{name} not found')

    def insert(self, name, value):
        self.stack[-1].put(name, value)

    def update(self, name, value):
        for memory in reversed(self.stack):
            if memory.has_key(name):  # noqa
                memory.put(name, value)
                return
        raise KeyError(f'{name} not found')

    def set(self, name, value):
        try:
            self.update(name, value)
        except KeyError:
            self.insert(name, value)

    def push(self, memory):
        self.stack.append(memory)

    def pop(self):
        self.stack.pop()
