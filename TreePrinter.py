import AST


def addToClass(cls):
    def decorator(func):
        setattr(cls, func.__name__, func)
        return func
    return decorator


def iprint(string, indent):
    print('|  ' * indent + string)


class TreePrinter:
    @addToClass(AST.Node)
    def printTree(self, indent=0):
        raise Exception('printTree not defined in class ' + self.__class__.__name__)

    @addToClass(AST.Program)
    def printTree(self, indent=0):
        self.instructions.printTree(indent)

    @addToClass(AST.Instructions)
    def printTree(self, indent=0):
        for instruction in self.instructions:
            instruction.printTree(indent)

    # @addToClass(AST.EmptyInstruction)
    # def printTree(self, indent=0):
    #     pass

    @addToClass(AST.If)
    def printTree(self, indent=0):
        iprint('IF', indent)
        self.condition.printTree(indent + 1)
        iprint('THEN', indent)
        self.instruction_then.printTree(indent + 1)
        if self.instruction_else is not None:
            iprint('ELSE', indent)
            self.instruction_else.printTree(indent + 1)

    @addToClass(AST.For)
    def printTree(self, indent=0):
        iprint('FOR', indent)
        self.variable.printTree(indent + 1)
        self.range_.printTree(indent + 1)
        self.instruction.printTree(indent + 1)

    @addToClass(AST.Range)
    def printTree(self, indent=0):
        iprint('RANGE', indent)
        self.start.printTree(indent + 1)
        self.end.printTree(indent + 1)

    @addToClass(AST.While)
    def printTree(self, indent=0):
        iprint('WHILE', indent)
        self.condition.printTree(indent + 1)
        self.instruction.printTree(indent + 1)

    @addToClass(AST.Condition)
    def printTree(self, indent=0):
        iprint(self.op, indent)
        self.left.printTree(indent + 1)
        self.right.printTree(indent + 1)

    @addToClass(AST.Break)
    def printTree(self, indent=0):
        iprint('BREAK', indent)

    @addToClass(AST.Continue)
    def printTree(self, indent=0):
        iprint('CONTINUE', indent)

    @addToClass(AST.Return)
    def printTree(self, indent=0):
        iprint('RETURN', indent)
        if self.value is not None:
            self.value.printTree(indent + 1)

    @addToClass(AST.Print)
    def printTree(self, indent=0):
        iprint('PRINT', indent)
        for arg in self.args:
            arg.printTree(indent + 1)

    @addToClass(AST.Assignment)
    def printTree(self, indent=0):
        iprint(self.op, indent)
        self.left.printTree(indent + 1)
        self.right.printTree(indent + 1)

    @addToClass(AST.Variable)
    def printTree(self, indent=0):
        iprint(self.name, indent)

    @addToClass(AST.Reference)
    def printTree(self, indent=0):
        iprint('REF', indent)
        self.variable.printTree(indent + 1)
        for index in self.indices:
            index.printTree(indent + 1)

    @addToClass(AST.BinExpr)
    def printTree(self, indent=0):
        iprint(self.op, indent)
        self.left.printTree(indent + 1)
        self.right.printTree(indent + 1)

    @addToClass(AST.UnaryExpr)
    def printTree(self, indent=0):
        iprint({
            '-': 'NEGATE',
            "'": 'TRANSPOSE',
        }.get(self.op, self.op), indent)
        self.expr.printTree(indent + 1)

    @addToClass(AST.Constant)
    def printTree(self, indent=0):
        iprint(str(self.value), indent)

    # @addToClass(AST.Matrix)
    # def printTree(self, indent=0):
    #     iprint('MATRIX', indent)
    #     # iprint('VECTOR', indent)
    #     for row in self.rows:
    #         # iprint('VECTOR', indent)
    #         for element in row:
    #             element.printTree(indent + 1)

    @addToClass(AST.Vector)
    def printTree(self, indent=0):
        iprint('VECTOR', indent)
        for element in self.elements:
            element.printTree(indent + 1)

    @addToClass(AST.MatrixSpecialFunction)
    def printTree(self, indent=0):
        iprint(self.__class__.__name__.lower(), indent)
        self.rows.printTree(indent + 1)
        if self.cols is not None:
            self.cols.printTree(indent + 1)

    @addToClass(AST.Error)
    def printTree(self, indent=0):
        iprint('ERROR', indent)
