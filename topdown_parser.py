from tokenizer import tokenizer

"""
Expression
    = BinaryExprExpression BinaryOp Expression
    | Literal
    | UnaryOp Expression
    | "(" Expression ")"

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

NUMERIC_LITERAL_ID = "num"
IDENTIFIER_ID = "name"

class Symbol(object):
    def __init__(self):
        #self.lbp = 0
        self.operands = []

    def nud(self):
        raise AetherSyntaxError()

    def led(self, first):
        raise AetherSyntaxError()

    def __repr__(self):
        return "<%s: %s>" % (self.value, self.operands)

class SymbolTable(object):
    def __init__(self, tokenizer):
        self._tokenizer = tokenizer
        self._table = {}
        self._tok = None  # current token

        identity = lambda self: self
        self.symbol(IDENTIFIER_ID).nud = identity
        self.symbol(NUMERIC_LITERAL_ID).nud = identity

        # Spin up the tokenizer
        self.advance()

    def symbol(self, key, bp=None):
        sym_class = self._table.get(key)
        if not sym_class:
            class Sym(Symbol):
                pass
            sym_class = Sym
        if bp is not None:
            sym_class.lbp = bp
        self._table[key] = sym_class
        return sym_class

    def numeric_literal(self, num):
        sym = self._table[NUMERIC_LITERAL_ID]()
        sym.value = num
        sym.lbp = 0
        return sym

    def identifier(self, name):
        sym = self._table[IDENTIFIER_ID]()
        sym.value = name
        sym.lbp = 0
        return sym

    def operator(self, op):
        sym_class = self._table.get(op)
        if not sym_class:
            raise AetherSyntaxError() #"Unrecognized operator %s" % op)
        opi = sym_class()
        opi.value = op
        return opi

    def infix(self, key, bp=0):
        def led(this, first):
            this.operands.append(first)
            this.operands.append(self.expr(this.lbp))
            return this
        self.symbol(key, bp).led = led

    def infix_r(self, key, bp=0):
        def led(this, first):
            this.operands.append(first)
            this.operands.append(self.expr(this.lbp-1))
            return this
        self.symbol(key, bp).led = led

    def prefix(self, key, bp=0):
        def nud(this):
            this.operands.append(self.expr(this.lbp))
            print "this.nud: %s" % this
            return this
        self.symbol(key, bp).nud = nud

    def expr(self, bp=0):
        print "expr with bp=%s" % bp
        t = self._tok
        self.advance()
        #if not t:
            #return
        first = t.nud()
        print 'self._tok == %s' % self._tok
        print 'self._tok.lbp == %s' % self._tok.lbp
        while bp < self._tok.lbp:
            t = self._tok
            self.advance()
            first = t.led(first)
        return first

    def advance(self):
        try:
            t = self._tokenizer.next()
            if t._typ == "num":
                self._tok = self.numeric_literal(t._tok)
            elif t._typ == "name":
                self._tok = self.identifier(t._tok)
            elif t._typ == "op":
                self._tok = self.operator(t._tok)
            else:
                raise AetherSyntaxError()
        except StopIteration:
            return

if __name__ == '__main__':
    import sys

    line = sys.stdin.read()
    t = tokenizer()(line)
    symtable = SymbolTable(t)

    symtable.infix("+", 10)
    symtable.infix("*", 11)
    symtable.infix_r("^", 12)

    print symtable.expr()
