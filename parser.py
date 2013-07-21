from tokenizer import tokenizer

"""
Expression
    = PrimaryExpr BinaryOp Expression
    | PrimaryExpr

PrimaryExpr
    = UnaryOp Expression
    | "(" Expression ")"
    | Literal

Literal
    = NUMBER
    | STRING
    | ATOM

UnaryOp
    = "-"

BinaryOp
    = "+" | "-" | "*" | "/"
"""

class AetherSyntaxError(Exception):
    pass

sym = None
getsym = None

class Token(object):
    def __init__(self, type, value):
        self.type = type
        self.value = value

    def __str__(self):
        return object.__str__(self) + "t: %s; v: %s" % (self.type, self.value)

NUMBER = 1
STRING = 2

def map_sym(sym):
    if sym._typ == "num":
        return Token(NUMBER, sym._tok)
    if sym._typ == "str":
        return Token(STRING, sym._tok)
    if sym._typ == "op":
        return Token(sym._tok, sym._tok)
    return sym

class ASTNumber(object):
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return "<ASTNumber: %s>" % self.value

class ASTString(object):
    def __init__(self, value):
        self.value = value

class ASTUnary(object):
    def __init__(self, op, operand):
        self.op = op
        self.operand = operand

class ASTBinary(object):
    def __init__(self, op, left, right):
        self.op = op
        self.operands = [left, right]

    def __str__(self):
        return "<ASTBinary: %s>" % (" %s " % self.op).join(str(x) for x in self.operands)

def accept(x):
    if hasattr(sym, "_tok") and sym._tok == x:
        getsym()
        return True

def expect(x):
    if not x:
        raise AetherSyntaxError()
    getsym()
    return x

def primary_expr():
    op = unary_op()
    if op:
        getsym()
        operand = expect(expr())
        return ASTUnary(op, operand)

    if accept("("):
        result = expect(expr())
        expect(")")
        return result

    return literal()

def expr():
    left = expect(primary_expr())
    if left:
        op = binary_op()
        if op:
            getsym()
            right = expect(expr())
            return ASTBinary(op, left, right)
        return left

def literal():
    #print "Parsing literal with %s" % sym
    if sym.type == NUMBER:
        return ASTNumber(sym.value)
    elif sym.type == STRING:
        return ASTString(sym.value)
    elif sym.type == ATOM:
        return ASTAtom(sym.value)

def unary_op():
    #print "Parsing unary op with %s" % sym
    if sym.type == "-":
        return "-"

def binary_op():
    #print "Parsing bin op with %s" % sym
    if sym.type == "+":
        return "+"
    elif sym.type == "-":
        return "-"
    elif sym.type == "*":
        return "*"
    elif sym.type == "/":
        return "/"

if __name__ == '__main__':
    import sys

    line = sys.stdin.read()
    t = tokenizer()(line)

    def f():
        global sym
        try:
            sym = map_sym(t.next())
            #print "Sym = %s" % sym
        except StopIteration:
            return
    getsym = f

    getsym()
    print expect(expr())
