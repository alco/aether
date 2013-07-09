# -*- coding: utf-8 -*-

import re
ops = ["=>>", "=>", "->>", "->",
       "•", "+", "-", "*", "/", "^", "∘",
       "=", "<(", ")>", "<[", "]>", "<<", ">>",
       "==", "≠", "≤", "≥", "<", ">",
       "(", ")", "❨", "❩", "[", "]", "{", "}",
       ".", ",", ":", ";", "&", "$", "!", "?"]
ops_re = "|".join(map(re.escape, ops))
token_re = re.compile(
    r"""[ \t]*(?:
        ( \d+ )                           # integer number
      | ( [a-zA-Z_][a-zA-Z0-9_]*['!?]? )  # identifier
      | ( // )                            # a comment
      | ( %s )                            # valid operators
      | ( " )                             # string literal delimiter
      | ( \n )                            # newline char
      | (.)                               # remaining trash
    )""" % ops_re, re.VERBOSE)


class TokenizerError(Exception):
    pass

class Token(object):
    def __init__(self, tok):
        self._tok = tok

    def __str__(self):
        return "<Token '%s'>" % self._tok

def escape(char):
    assert len(char) == 1
    if char == "n":
        return "\n"
    elif char == "t":
        return "\t"
    elif char == "\\":
        return "\\"
    elif char == "\"":
        return "\""
    raise TokenizerError("Unhandled escape sequence %s" % char)

def extract_string(program, pos):
    """Scan through the string until a closing quote is found"""
    string = ""
    while pos < len(program):
        if program[pos] == '\\':
            pos += 1
            if pos == len(program):
                break
            string += escape(program[pos])
        elif program[pos] == '"':
            break
        else:
            string += program[pos]
        pos += 1
    # end while

    if pos == len(program):
        raise TokenizerError("Reached end of input when looking for a closing quote")
    pos += 1
    return string, pos

def ignore_comment(program, pos):
    """Ignores remaining characters on current line"""
    while pos < len(program):
        if program[pos] == '\n':
            break
        pos += 1
    return pos


def tokenizer():
    def tokenize(program):
        pos = 0
        line_pos = 0
        line = 1
        while True:
            match = token_re.search(program, pos)
            if not match:
                break
            pos = match.end()

            number, name, comment, operator, quote, newline, trash = match.groups()
            if comment:
                pos = ignore_comment(program, pos)
                continue

            elif number:
                tok = Token(number)
                yield tok

            elif operator:
                tok = Token(operator)
                yield tok

            elif name:
                tok = Token(name)
                yield tok

            elif quote:
                string, pos = extract_string(program, pos)
                tok = Token(string)
                yield tok

            elif newline:
                line_pos = pos + 1
                line += 1

            else:
                raise TokenizerError("Unexpected token '%s'" % trash)
            # end if
        # end for
    #end def
    return tokenize

if __name__ == '__main__':
    import sys

    toker = tokenizer()
    line = sys.stdin.read()

    for tok in toker(line):
        print tok
