class Memory:
    def __init__(self, name):
        self.name = name
        self.symbols = {}

    def has_key(self, name):
        return name in self.symbols

    def get(self, name):
        return self.symbols[name]

    def put(self, name, value):
        self.symbols[name] = value


class MemoryStack:
    def __init__(self, memory=None):
        if memory is None:
            memory = Memory('global')
        self.stack = [memory]

    def get(self, name):
        for memory in self.stack:
            if memory.has_key(name):
                return memory.get(name)
        raise RuntimeError(f'{name} not declared')

    def insert(self, name, value):
        self.stack[-1].put(name, value)

    def set(self, name, value):
        for memory in reversed(self.stack):
            if memory.has_key(name):
                memory.put(name, value)
                return
        raise RuntimeError(f'{name} not declared')

    def push(self, memory):
        self.stack.append(memory)

    def pop(self):
        self.stack.pop()
